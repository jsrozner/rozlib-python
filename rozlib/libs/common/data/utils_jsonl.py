import dataclasses
import json
from dataclasses import asdict
from pathlib import Path
from typing import List, Type, TypeVar, Generator, Dict

from rozlib.libs.common.data.utils_dataclass import from_dict

# from libs.common.data.utils_dataclass import from_dict

# todo(low): typing
T = TypeVar('T', bound=dataclasses.dataclass)

def dump_dict_jsonl(obj: Dict, file_path: Path):
    """
    Dumps the MLMResultForSentence results into a JSONL file.

    Args:
        obj: obj that is a dataclass
        file_path: Path to the output JSONL file.
    """
    with open(file_path, 'a') as f:
        # Convert the dataclass to a dictionary
        # pp(obj_dict)
        # Write each dictionary as a JSON object (one per line)
        f.write(json.dumps(obj) + '\n')

# todo: would be better to not open/close every time
# todo: maybe add annotation of type
def dump_to_jsonl(obj: T, file_path: Path):
    """
    Dumps the obj of type T results into a JSONL file.

    Args:
        obj: obj that is a dataclass
        file_path: Path to the output JSONL file.
    """
    with open(file_path, 'a') as f:
        # Convert the dataclass to a dictionary
        obj_dict = asdict(obj)
        # pp(obj_dict)
        # Write each dictionary as a JSON object (one per line)
        f.write(json.dumps(obj_dict) + '\n')


def read_from_jsonl(file_path: Path, cls: Type[T]) -> List[T]:
    """
    Reads the MLMResultForSentence results from a JSONL file and converts them back to objects.

    Args:
        file_path: Path to the JSONL file.
        cls: the dataclass type

    Returns:
        A list of MLMResultForSentence objects.
    """
    result = []

    with open(file_path, 'r') as f:
        for line in f:
            sentence_dict = json.loads(line.strip())
            # Convert the dictionary back into an MLMResultForSentence object
            sentence_result = from_dict(cls, sentence_dict)
            result.append(sentence_result)

    return result


def read_jsonl(file_path: str | Path) -> Generator[dict, None, None]:
    """
    Reads a JSON Lines (jsonl) file line by line.

    Args:
        file_path (str): Path to the jsonl file.

    Yields:
        dict: Parsed JSON object from each line.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                yield json.loads(line)
