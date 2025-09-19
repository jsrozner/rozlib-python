import csv
import difflib
import json
import os
from pathlib import Path
from pprint import pp
from typing import Type, Dict, Any, TypeVar, List, Union
import dataclasses
from dataclasses import fields, MISSING
from typing import Type, TypeVar, List, Any
import csv

T = TypeVar('T', bound=dataclasses.dataclass)

def from_dict(cls: Type[T], dict_obj: Dict[str, Any]) -> T:
    """
    Recursively converts a dictionary to a dataclass.

    Args:
        cls: The dataclass type to convert to.
        dict_obj: The dictionary containing the data.

    Returns:
        An instance of the dataclass with the dictionary values populated.
    """
    # try:
    fieldtypes = {f.name: f.type for f in fields(cls)}
    try:
        return (
            cls(**{f: from_dict(fieldtypes[f], dict_obj[f])
            if isinstance(dict_obj[f], dict)
            else dict_obj[f]
                   for f in dict_obj}))
    except TypeError as e:
        print(f"While processing to class {cls}:")
        pp(fieldtypes)
        pp(dict_obj)
        raise(e)
    # except TypeError:
    #     return dict_obj

def _write_dataclass_to_json_file(obj: dataclasses.dataclass, file_path: Path)\
        -> None:
    """
    Converts a dataclass to a dictionary and writes it to a JSON file.

    Args:
        obj: The dataclass instance to be written.
        file_path: Path to the output JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(dataclasses.asdict(obj), f, indent=4)


def _diff_files(file1: Path, file2: Path) -> List[str]:
    """
    Compares two files and prints a diff highlighting the differences.

    Args:
        file1: Path to the first file.
        file2: Path to the second file.
    """
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

        diff = difflib.unified_diff(
            f1_lines,
            f2_lines,
            fromfile=str(file1),
            tofile=str(file2)
        )
        return list(diff)

def diff_dataclasses(o1, o2) -> bool:
    """
    Diff o1 and o2.
    Returns:
        bool: True if o1 and o2 are the same.

    Approach:
        Write both objects as dicts to file
        Read in and diff the files
    """
    path1 = Path("") / "o1.temp"
    path2 = Path("") / "o2.temp"
    _write_dataclass_to_json_file(o1, path1)
    _write_dataclass_to_json_file(o2, path2)

    diff = _diff_files(path1, path2)

    if len(diff) > 0:
        print("\n".join(diff))

    # todo(low): maybe want to preserve for later if there is a diff
    # delete files
    os.remove(path1)
    os.remove(path2)

    return len(diff) == 0


# todo: should parse fields automatically - rename to indicate this function does strings only
def read_csv_to_dataclass(cls: Type[T], file_path: str | Path) -> List[T]:
    """
    Reads a CSV file and converts its rows into a list of dataclass instances.

    Args:
        cls (Type[T]): The dataclass type to instantiate.
        file_path (str): Path to the input CSV file.

    Returns:
        List[T]: List of dataclass instances.
    """
    # Get field names from the dataclass
    field_names = {f.name for f in fields(cls)}
    # print(field_names)

    # Read from the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Ensure only valid fields are passed to the dataclass
        # ret_list = []
        # for row in reader:
        #     d = {}
        #     for k,v in row.items():
        #         if not k in field_names:
        #             print(f"{k} not in fieldnames")
        #             continue
        #         d[k] = v
        #     c = cls(**d)
        #     pp(c)
        #     ret_list.append(c)
        #
        # return ret_list
        return [cls(**{k: v for k, v in row.items() if k in field_names}) for row in reader]

def write_dataclass_to_csv(data: List[T], file_path: str) -> None:
    """
    Writes a list of dataclass instances to a CSV file.

    Args:
        data (List[T]): List of dataclass instances of type T.
        file_path (str): Path to the output CSV file.
    """
    # Extract field names from the dataclass
    fieldnames = [field.name for field in data[0].__dataclass_fields__.values()]

    # Write to the CSV file
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(dataclasses.asdict(item))
