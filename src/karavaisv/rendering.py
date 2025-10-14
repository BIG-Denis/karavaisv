import re
import copy
import time

from .util_funcs import print_render_info_start, print_render_info_end


KSV_META_FLAGS: set[str] = {"if", "elif", "else", "for", "end"}
KSV_META_OPENINGS: set[str] = {"if", "for"}
KSV_META_CLOSURES: set[str] = {"end",}
KSV_META_COLONS: set[str] = {"if", "elif", "else", "for"}


def check_line_for_meta(line: str) -> str:
    if re.match(r"\s*\~\$\s*if.*\$\~.*", line):    # ksv if
        return "if"
    if re.match(r"\s*\~\$\s*elif.*\$\~.*", line):  # ksv elif
        return "elif"
    if re.match(r"\s*\~\$\s*else.*\$\~.*", line):  # ksv else
        return "else"
    if re.match(r"\s*\~\$\s*for.*\$\~.*", line):   # ksv for
        return "for"
    if re.match(r"\s*\~\$\s*end.*\$\~.*", line):   # ksv end
        return "end"
    return None


def is_meta_in_block(content: str) -> bool:
    all_lines = content.split('\n')[:-1]

    for line in all_lines:
        if check_line_for_meta(line) is not None:
            return True

    return False


def render_single_line(line: str, variables :dict) -> str:
    inline_templates: list[str] = re.findall(r"\~/.*?/\~", line)
    exec_locals: dict = variables
    templated_line: str = copy.copy(line) + '\n'

    if len(inline_templates) > 0:
        for inline_template in inline_templates:
            exec(f"templated_line = str({inline_template[3:-3]})", locals=exec_locals)
            templated_line = templated_line.replace(inline_template, exec_locals['templated_line'])

    return templated_line


def meta_to_py_line(line: str) -> str:
    converted_line: str = copy.copy(line)

    beginning_meta: list[str] = re.findall(r"^\s*\~\$\s*", line)
    trailing_meta: list[str] = re.findall(r"\s*\$\~.*$", line)
    add_colon: bool = check_line_for_meta(line) in KSV_META_COLONS

    converted_line = converted_line.replace(beginning_meta[0], '')
    converted_line = converted_line.replace(trailing_meta[0], '')

    if add_colon:
        converted_line += ':'

    return converted_line


def render_single_block(content: str, variables: dict) -> str:
    all_lines: list[str] = content.split('\n')[:-1]
    executable_content: str = ""
    executed_content: str = ""
    all_locals: dict = variables | locals()
    exec_locals: dict = locals() | all_locals
    block_contains_meta: bool = is_meta_in_block(content)

    for line in all_lines:
        if check_line_for_meta(line) is not None: # meta
            executable_content += meta_to_py_line(line)

        else:                                     # non-meta
            if block_contains_meta:
                executable_content += 4 * ' '
            executable_content += "executed_content += "
            executable_content += f'render_single_line("""{line}""", all_locals | locals())'

        executable_content += '\n'

    exec(executable_content, locals=exec_locals)
    executed_content = exec_locals['executed_content']

    return executed_content


def divide_into_blocks(content: str) -> list[str]:
    depth_level: int = 0
    ksv_blocks: list[str] = []
    line_skip: bool = False
    all_lines: list[str] = content.split('\n')[:-1]

    for i, line in enumerate(all_lines):
        meta_key: str = check_line_for_meta(line)
        line_skip = False

        if meta_key in KSV_META_OPENINGS:
            depth_level += 1
            if depth_level == 1:
                ksv_blocks.append("")

        if meta_key in KSV_META_CLOSURES:
            depth_level -= 1
            if depth_level == 0:
                ksv_blocks.append("")
                line_skip = True

        if not line_skip:
            if len(ksv_blocks) == 0:
                ksv_blocks.append("")
            ksv_blocks[-1] += line
            if (i != len(all_lines)):
                ksv_blocks[-1] += '\n'

    return ksv_blocks


def render_substring(content: str, variables: dict) -> str:
    rendered_content: str = ""
    ksv_blocks: list[str] = divide_into_blocks(content)
    ksv_blocks_count: int = len(ksv_blocks)

    if ksv_blocks_count > 1:
        for ksv_block in ksv_blocks:
            rendered_content += render_substring(ksv_block, variables)

    elif ksv_blocks_count == 1:
        rendered_content += render_single_block(ksv_blocks[0], variables)

    return rendered_content



def templated_to_executable(content: str) -> str:
    all_lines: list[str] = content.split('\n')[:-1]
    executable_content: str = "KSV_RENDERED_CONTENT = ''\n"
    depth_level: int = 0

    for line in all_lines:
        meta = check_line_for_meta(line)
        if meta is not None:
            if meta in KSV_META_OPENINGS:
                executable_content += ' ' * 4 * depth_level
                executable_content += meta_to_py_line(line) + '\n'
                depth_level += 1
            if meta in KSV_META_CLOSURES:
                depth_level -= 1
        else:
            executable_content += ' ' * 4 * depth_level
            executable_content += f"KSV_RENDERED_CONTENT += render_single_line('''{line}''', locals())\n"

    return executable_content


def execute_content(content: str, parameters: dict) -> str:
    exec_locals: dict = parameters
    exec(content, locals=exec_locals)
    rendered_content: str = exec_locals['KSV_RENDERED_CONTENT']
    return rendered_content


def render(content: str, parameters: dict, filename: str=None, logging: bool = True) -> str:
    """
    Render the given content with KaravaiSV templating engine with the provided parameters.

    This function basically is the main entry point for rendering content using the KaravaiSV templating engine.
    It takes content via a python string and renders any KaravaiSV templating syntax found within it using the provided parameters.

    Args:
        content (str): The content to be rendered.
        parameters (dict): A dictionary of parameters to be used in the rendering process.
        filename (str, optional): The name of the file being rendered, used for logging purposes.

    Returns:
        str: The rendered content as a string.
    """
    if logging:
        start_time: float = time.time()
        print_render_info_start(filename)

    executable_content: str = templated_to_executable(content)
    rendered_content: str = execute_content(executable_content, parameters)

    if logging:
        end_time: float = time.time()
        ellapsed_time: float = end_time - start_time
        print_render_info_end(filename, ellapsed_time)

    return rendered_content
