# Maya Python Plugin Test Example

## Introduction

This repository is designed to guide individuals with no or little experience in using pytest and mocks to test Maya Python plugins. The testing framework provided here leverages pytest, a powerful tool for writing and executing tests in Python. This guide assumes that you are working with Maya 2022.5 or superior, but the principles are applicable to other versions with some adjustments.

## Requirements

- **Maya 2022.5**: The tests are created and tested on Maya 2022.5. Compatibility with older versions is not guaranteed.
- **Pytest**: A Python testing tool required to run the tests in this repository.

## Installation

### Installing Pytest

To install pytest, follow these steps:

1. Open your terminal.
2. Navigate to the `maya[version]/bin` folder. Replace `[version]` with your actual Maya version number.
3. Run the command: `mayapy -m pip install pytest`
4. To verify the installation, run: `mayapy -m pip list` and check if pytest is listed.

### Setting Environment Variables

To run the tests, it's advised to add the `mayapy` folder to your system's environment variables. But it can be run using the maya full path as well. Here are the instructions for Windows, macOS, and Linux:

#### Windows

1. Search for "Environment Variables" in the Start menu and select "Edit the system environment variables."
2. In the System Properties window, click on "Environment Variables."
3. Under System Variables, find the `Path` variable and select it. Click "Edit."
4. Click "New" and add the path to your `mayapy` folder.
5. Click "OK" on all windows to save your changes.

#### macOS

1. Open Terminal.
2. Edit your shell profile file (e.g., `~/.bash_profile`, `~/.zshrc`, etc.) using a text editor.
3. Add the following line: `export PATH="/path/to/mayapy:$PATH"`. Replace `/path/to/mayapy` with the actual path to your `mayapy` folder.
4. Save the file and close the editor.
5. In Terminal, run `source ~/.bash_profile` (or the equivalent file you edited) to apply the changes.

#### Linux

1. Open Terminal.
2. Edit your shell profile file (e.g., `~/.bashrc`, `~/.zshrc`, etc.) using a text editor.
3. Add the following line: `export PATH="/path/to/mayapy:$PATH"`. Replace `/path/to/mayapy` with the actual path to your `mayapy` folder.
4. Save the file and close the editor.
5. In Terminal, run `source ~/.bashrc` (or the equivalent file you edited) to apply the changes.

## Running Tests

To run your tests, use the following command in the terminal:

```bash
mayapy -m pytest [name of the file]
```

For example, to test the `test_center_point_node.py` file, you would run:

```bash
mayapy -m pytest -s tests/unit/test_center_point_node.py
```
