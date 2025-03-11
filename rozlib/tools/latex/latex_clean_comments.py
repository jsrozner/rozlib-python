from pathlib import Path
import sys

def remove_tex_comments(filename: str) -> None:
    input_path = Path(filename)
    output_path = input_path.with_name(f"{input_path.stem}_clean{input_path.suffix}")

    with input_path.open("r", encoding="utf-8") as infile, output_path.open("w", encoding="utf-8") as outfile:
        for line in infile:
            if not line.lstrip().startswith("%"):
                outfile.write(line)

    print(f"Cleaned file saved as: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py filename.tex")
    else:
        remove_tex_comments(sys.argv[1])