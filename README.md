# Sequence File Parser

This Python script parses sequence files in a specified input directory and writes the parsed content to a specified output directory. The script can optionally overwrite existing files in the output directory.

## Usage

You can run the script from the command line as follows:

```bash
python parser.py input_folder_path output_folder_path

```

```powershell
python .\parser.py .\input_folder_path .\output_folder_path

```

Replace input_folder_path and output_folder_path with the paths to your actual input and output folders.

If you want to run the script without overwriting existing files, you can use the --not_overwrite flag:

```bash
python parser.py input_folder_path output_folder_path --not_overwrite

```

```powershell
python .\parser.py .\input_folder_path .\output_folder_path --not_overwrite

```

This will run the script and skip files that already exist in the output folder.

## Functions

The script contains the following functions:

- `process_lines(non_empty_lines: List[str]) -> List[str]` Processes a list of non-empty lines from a file. If a line starts with ">", it's a name and you can skip it. Every line after that, until the next line with ">", is a sequence and you need to remove all trailing newlines.

- `parse_and_write(input_folder: str, output_folder: str, overwrite: bool)` -> None: Parses files in the input_folder and writes the parsed content to the output_folder. If overwrite is False, the script will skip files that already exist in the output folder.

- `main() -> None:` Parses command line arguments and processes the files. If --not_overwrite is True, the script will ask for user confirmation before overwriting existing files.
