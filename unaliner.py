import argparse
import os
from typing import List

def process_lines(non_empty_lines: List[str]) -> List[str]:
    """
    Process a list of non-empty lines from a file. If a line starts with ">", it's a name and you can skip it. 
    Every line after that, until the next line with ">", is a sequence and you need to remove all trailing newlines.

    Args:
        non_empty_lines (List[str]): A list of non-empty lines from a file.

    Returns:
        List[str]: A list of processed lines.
    """
    result = []
    sequence = []
    for line in non_empty_lines:
        if line.startswith(">"):
            line = line.replace("/", "_")
            if sequence:  # if there is a sequence collected, join it and add to result
                result.append(''.join(sequence))
                sequence = []  # reset the sequence
            result.append(line)  # add the name line to the result
        else:
            sequence.append(line.strip())  # remove trailing newline and add to sequence
    if sequence:  # add the last sequence if it exists
        result.append(''.join(sequence))
    return result


def parse_and_write(input_folder: str, output_folder: str, overwrite: bool) -> None:
    for filename in os.listdir(input_folder):
        output_filename = filename.split('.')[0] + '_parsed.txt'
        if not overwrite and os.path.exists(os.path.join(output_folder, output_filename)):
            print(f"File {output_filename} already exists, skipping.")
            continue

        with open(os.path.join(input_folder, filename), 'r') as f:
            content = f.read()

        content = content.replace("-", "").splitlines()

        non_empty_lines = [line for line in content if line.strip()]
        
        parsed_lines = process_lines(non_empty_lines)

        with open(os.path.join(output_folder, output_filename), 'w') as f:
            f.write('\n'.join(parsed_lines))
        
        print(f"File {output_filename} written.")



def main() -> None:
    parser = argparse.ArgumentParser(description='Parse aligned sequence files.')
    parser.add_argument('input_folder', type=str, help='The input folder path')
    parser.add_argument('output_folder', type=str, help='The output folder path')
    parser.add_argument('--not_overwrite', action='store_false', help='Do not overwrite existing files')

    args = parser.parse_args()

    if args.not_overwrite:
        print('args.overwrite:', args.not_overwrite)
        confirm = input("Running with overwrite set to True. Existing files will be overwritten. Are you sure? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborting.")
            return

    parse_and_write(args.input_folder, args.output_folder, args.not_overwrite)

if __name__ == "__main__":
    main()