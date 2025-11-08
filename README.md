# KaravaiSV

## What is this?

KaravaiSV is an advanced templating tool for SystemVerilog. \
It gives a developer much more abilities to parametrize design compared to classic SystemVerilog `generate` and `define` constructions. \
Last but not least it gives ability to write lint errors free code with ease.

### Why do you want to use it?

1. Write once - use everywhere. Simple module with couple of parameters gives ability to use it everywhere only slightly changing config file.
2. Flexible architecture. Let your module serve single purpose but many ways choosen design-time.
3. Speed up development. Putting same modules with different configs rather than zoo of them does not spend your time.
4. No repeated verification. Verify module once - use million of times.
5. Debug with ease. Developing a new feature and found a bug? Turn off your WIP feature with parameter and see does this bug existed before.
6. No fear to edit. Changing generation config rather than code itself leads to less _manual edits_ and followed mistakes as well.
7. Generation automatization. Automatization of project generation will become easy as pie.

## Installation

The main goal of KaravaiSV is to make everything as easy as ABC and so installation follows the same rule.

**A**: Install KaravaiSV

```bash
pip install karavaisv
```

**B**: Modify generation config for your needs

```bash
vim config/default.yaml
```

**C**: Run generate script

```bash
python generate.py
```

Ta-da! \
Now you generated project. All generated files are located somewhere here. By default all rendered conted appears in `build` folder.

## Usage

There are mainly two ways of usage KSV - CLI and generation scripts. \
Generation scripts are always preferred as they provides ability to make parameters correction checks, calculation derived parameters, etc. \
However, CLI interface still can be used for debugging and temporarily purposes.

All of the below described examples of KSV are a best practices to write a unified generating scripts. It serves purpose to make all ksv-templated project compliant with each other. \
For the compliant reasons there are strong recomendations for single modules as they are likely to be used in big projects and should be integrated with ease. \
It is highly recommended, but not a mandatory to follow this rules. \

### Recommended usage for single module

For a repository that contains single ksv-templated module the following generate script pattern is preferred.

```python
import karavaisv as ksv
# other imports if needed

# function that performs validity check on given parameters
def ksv_check_parameters(parameters):
    <...>
    assert parameters['data_width'] > 0, "data_width must be positive integer"
    <...>
    assert len(parameters['input_ports']) > 0, "module must have at least one input port"
    <...>


# function that calculates derived parameters
def ksv_calculate_derived_parameters(parameters):
    <...>
    # example parameter fifo_width equals max width of all input ports
    data_widths = [port['data_width'] for port in parameters['input_ports']]
    parameters['fifo_width'] = max(data_widths)
    <...>
    return parameters


# function that render code when runnung separately
def main():
    FILEPATH_DST = "build/output.sv"
    FILEPATH_PARAMS = "config/default.yaml"
    FILEPATH_SRC = "rtl/module.ksv"

    parameters = ksv.read_params_from_yaml(FILEPATH_PARAMS)
    source_code = ksv.read_source_from_file(FILEPATH_SRC)

    ksv_check_parameters(parameters)
    parameters = ksv_calculate_derived_parameters(parameters)

    rendered_code = ksv.render(source_code, parameters, filepath=FILEPATH)
    ksv.write_rendered_to_file(rendered_code, FILEPATH)

# python syntax construction to run main() function only when script is called explicitly
if __name__ == "__main__":
    main()
```

> Feel free to take this script into all of you project as it is good enough to deal with all the job. The only thing to be changed to accumulate your needs is a `ksv_check_parameters` and `ksv_calculate_derived_parameters` function bodies and `FILEPATH_DST`, `FILEPATH_PARAMS` and `FILEPATH_SRC` constants in `main` function (their assignment can also be moved somewhere else).

Why should you use such a big script with dividing into functions? Why not single multi-line script? \
The answer is simplicity to integrate. In case of your module is about to be used as an IP block in bigger projects, main generate script at whole project will perform a call to `ksv_check_parameters` and `ksv_calculate_derived_parameters` functions in every IP block to verify and calculate their parameters. \
Learn more and see example at the folowing paragraph.

> Described above integration ability is the reason why `main` function are separated and `if __name__ == "__main__"` are present. Other way the main function could've been executed when generate script imported.

### Recommended usage for big project

For a repository that contains massive project including submodules or simple KSV files the following generate script pattern is preferred.

TBD

> It is a common scenario when within a big project there are ksv-templated and simple sv files. There are two ways to solve this issue. \
First, you can make main part of project non-templated and requre to run KaravaiSV once to generate necceserly ksv-templated files. \
Second, preferred way, make project must always be generated via KaravaiSV and simply copy sv files to destination folder with rendered content or process them via KaravaiSV the same way it done with ksv-templated files. If sv files have no KSV syntax then they are not being affected.

### CLI interface

TBD

### Passing parameters to KSV engine

TBD

## What it can do with code?

TBD

### Supported syntax

TBD

### Usage example

TBD

### Usage with non-sv files

TBD

## Example project

TBD

## Extras

TBD

### Addition information

TBD

### Issues

TBD
