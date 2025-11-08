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

**B**: Navigate to project directory and change config

```bash
cd path/to/templated_project
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
However, CLI interface still can be used for debugging and temporarily purposes. \

### Recommended usage for single module

TBD

### Recommended usage for big project

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
