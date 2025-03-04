from pathlib import Path

from conllu import parse_incr


def get_data_iterator_for_file(file: Path):
    data_file = open(file, "r", encoding="utf-8")
    data = parse_incr(data_file)
    return data
