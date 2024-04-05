import argparse, os, csv
from Bio import SeqIO


def output_log_table(filename: str, old_names: list, output_filename: str) -> None:
    with open(output_filename, "w", newline="") as csvfile:
        fieldnames = ["seq_lengh_AA", "new_name", "old_name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i, record in enumerate(SeqIO.parse(filename, "fasta")):
            seq_length_AA = len(record.seq.replace("-", ""))
            new_name = record.name
            old_name = old_names[i]
            writer.writerow(
                {
                    "old_name": old_name,
                    "new_name": new_name,
                    "seq_lengh_AA": seq_length_AA,
                }
            )
    print("Log table written to", output_filename)


def translate_name(name: str, map: dict) -> str:
    name_parts = name.split("_")

    for part in name_parts:
        for key, value in map.items():
            if key in part:
                return value
            else:
                continue
    return name


def check_tardigrade(name: str, map: dict) -> bool:
    for key, value in map.items():
        if value in name:
            return True
    return False


def make_name(name_part: str, index: int, protein_name: str) -> str:
    return f">{name_part}-i{index}-{protein_name}"


def process_lines(lines: list, protein_name: str) -> list:

    TRANSLATION_MAP = {
        "RvY": "tRv",
        "BV898": "tHe",
        "GFGY": "tPr",
        "GFGZ": "tMi",
        "DN": "tMp",
        "TRINITY": "tEt",
        "Richtersius": "tRc",
        "Echiniscoides": "tEs",
    }

    occurences = {}
    parsed_lines = []
    for line in lines:
        if line.startswith(">"):
            name_part = translate_name(line, TRANSLATION_MAP)

            if check_tardigrade(name_part, TRANSLATION_MAP):
                if name_part in occurences:
                    occurences[name_part] += 1
                    parsed_lines.append(
                        make_name(name_part, occurences[name_part], protein_name)
                    )
                else:
                    occurences[name_part] = 1
                    parsed_lines.append(
                        make_name(name_part, occurences[name_part], protein_name)
                    )
            else:
                parsed_lines.append(line)
        else:
            parsed_lines.append(line)

    return parsed_lines


def get_protein_name(filename) -> str:
    protein_name = filename.split("_")[0]
    return protein_name


def write(output_folder: str, output_filename: str, content: list) -> None:
    with open(os.path.join(output_folder, output_filename), "w") as f:
        f.write("\n".join(content))

        print(f"File {output_filename} written.")

    return None


def get_old_names(content: list) -> list:
    old_names = []
    for line in content:
        if line.startswith(">"):
            old_names.append(line.lstrip(">"))
    return old_names


def parse(input_folder: str, output_folder: str, overwrite: bool) -> None:
    for filename in os.listdir(input_folder):
        output_filename = filename.split(".")[0] + "_renamed.txt"
        filename_path = os.path.join(input_folder, filename)
        output_filename_path = os.path.join(output_folder, output_filename)

        if not overwrite and os.path.exists(
            os.path.join(output_folder, output_filename)
        ):
            print(f"File {output_filename} already exists, skipping.")
            continue

        with open(os.path.join(input_folder, filename), "r") as f:
            content = f.read()
            content = content.splitlines()
            old_names = get_old_names(content)

            parsed_lines = process_lines(content, get_protein_name(filename))
            write(output_folder, output_filename, parsed_lines)

        log_table_name = os.path.join(
            output_folder, filename.split(".")[0] + "_log.csv"
        )
        output_log_table(
            output_filename_path,
            old_names,
            log_table_name,
        )

    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse aligned sequence files.")
    parser.add_argument("input_folder", type=str, help="The input folder path")
    parser.add_argument("output_folder", type=str, help="The output folder path")
    parser.add_argument(
        "--not_overwrite", action="store_false", help="Do not overwrite existing files"
    )

    args = parser.parse_args()

    if args.not_overwrite:
        print("args.overwrite:", args.not_overwrite)
        confirm = input(
            "Running with overwrite set to True. Existing files will be overwritten. Are you sure? (y/n): "
        )
        if confirm.lower() != "y":
            print("Aborting.")
            return

    # make parse and write separate file and import it here
    parse(args.input_folder, args.output_folder, args.not_overwrite)


if __name__ == "__main__":
    main()
