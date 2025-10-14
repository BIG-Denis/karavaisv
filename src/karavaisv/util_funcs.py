# functuons for printing rendering info

def print_render_info_start(filename: str) -> None:
    if filename is not None:
        print(f"Info: Started rendering '{filename}'...")
    else:
        print("Info: Started rendering...")


def print_render_info_end(filename: str, ellapsed_time: float) -> None:
    if filename is not None:
        print(f"Info: Rendering of '{filename}' completed in {ellapsed_time:.2f} seconds.")
    else:
        print(f"Info: Rendering completed in {ellapsed_time:.2f} seconds.")


# functions for reading source files

def read_params_from_yaml(filepath: str) -> dict:
    import yaml

    with open(filepath, 'r') as file:
        parameters = yaml.safe_load(file)

    return parameters


def read_source_from_file(filepath: str) -> str:
    with open(filepath, 'r') as file:
        source_code = file.read()

    return source_code
