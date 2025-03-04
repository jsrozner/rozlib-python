import os
import pprint
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from pprint import pp
from typing import Dict, Any

from nltk.corpus import BNCCorpusReader
from libs.utils import str_starts_with_punct
from typing import List


class SafeDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Key '{key}' already exists in the dictionary and cannot be overwritten.")
        super().__setitem__(key, value)

def _xml_to_dict_simple(
        element: ET.Element,
        stop_key: str | None = None
) -> Dict[str, Any]:
    """
    Recursively converts an XML element and its children into a simplified dictionary.

    Each element potentially has
    - text -> will be represented as _text: val
    - attributes (a dict) -> will be entered directly as a dict from key to values
    - children (a list of subelements) -> will be keyed by the tag of the children

    So for example:
    root_dict: {
        '_text': 'text_value',
        'attr1': 'attr1_val',
        'child_tag1': [Element]  // a list of elements of this tag (same structure, recursive)
        'child_tag2': [Element]  // same
    }

    Args:
        element (ET.Element): The root XML element.
        stop_key: When encountered, parsing will stop

    Returns:
        Dict[str, Any]: A straightforward dictionary representation of the XML element.
    """
    # do not allow overwriting of keys (concern is that 'text' key could be duplicated)
    result = SafeDict()

    if element.text:
        text = element.text.strip() if element.text and element.text.strip() else None
        if text:
            result['_text'] = text

    # note that tag will be included in children; though root node tag will be missing, unless we differentiate
    # tag becomes the key for the children list
    # if element.tag:
    #     result['_tag'] = element.tag

    # element.attrib is a dictionary; we add all of them
    if element.attrib:
        result.update(element.attrib)

    # tail should be None or empty string
    if element.tail and element.tail.strip():
        raise Exception(f"has tail!! {element.tail}")

    # Process child elements recursively
    # Element has a List of subelements ("children"), potentially
    # Each child has a "tag" that names the element type
    # There may be multiple children of a given type
    # The dict has a key entry for each child type that maps to a List of the children
    if list(element):
        # To store multiple elements with the same tag
        children = {}   # maps child.tag => List[Element]
        for child in element:
            if child.tag == stop_key:
                # print(f"Stopping parse at {stop_key}")
                break

            # stop key not needed if you don't expect the key to occur outside of root
            child_dict = _xml_to_dict_simple(child)

            # If the child tag already exists, make sure it's a list and append
            if child.tag in children:
                if not isinstance(children[child.tag], list):
                    children[child.tag] = [children[child.tag]]
                children[child.tag].append(child_dict)
            else:
                children[child.tag] = child_dict

        result.update(children)


    return result

def xml_file_to_dict(
        file_path: str,
        stop_key: str | None = None
) -> Dict[str, Any]:
    """
    Converts an XML file into a dictionary.

    Args:
        file_path (str): Path to the XML file.

    Returns:
        Dict[str, Any]: A dictionary representation of the XML file.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    return _xml_to_dict_simple(root, stop_key)

@dataclass
class BNCFileInfo:
    file_id_full: str
    file_id: str
    file_path: str

    edition: str
    extent: str
    source_desc: Dict[str, Any]
    title_stmt: str
    profile_text_class: str
    profile_text_class_code: Dict[str, Any]

    sent_ct: int

    def __init__(self, root_dir: str, file_path_from_root: str):
        self.file_id_full = file_path_from_root
        self.file_id = self._get_file_id()

        file_path = Path(root_dir) / file_path_from_root
        self.file_path = str(file_path.resolve())

        xml_dict = xml_file_to_dict(self.file_path, stop_key="wtext")

        teiHeader = xml_dict['teiHeader']
        self.edition = teiHeader['fileDesc']['editionStmt']['edition']['_text']
        self.extent = teiHeader['fileDesc']['extent']['_text']
        self.source_desc = teiHeader['fileDesc']['sourceDesc']['bibl']
        self.title_stmt = teiHeader['fileDesc']['titleStmt']['title']['_text']
        self.profile_text_class = teiHeader['profileDesc']['textClass']['catRef']['targets']
        self.profile_text_class_code = teiHeader['profileDesc']['textClass']['classCode']

        self.sent_ct = self._get_sent_ct()

        if not self.file_id == xml_dict['{http://www.w3.org/XML/1998/namespace}id']:
            expected = xml_dict['{http://www.w3.org/XML/1998/namespace}id']
            print(self.file_id_full)
            pp(xml_dict)
            raise Exception(f"{self.file_id} is not {expected}")

    def _get_sent_ct(self) -> int:
        """
        Structure:
        'extent': {'_text': '3792 tokens; 3827 w-units; '
                                                '178 s-units'},
        """
        extent_split = self.extent.split(' ')
        cts = [extent_split[i] for i in [0, 2, 4]]
        cts_ints = [int(x) for x in cts]
        return cts_ints[2]

    def _get_file_id(self):
        # of form 'A/A4/A4W.xml'
        end = self.file_id_full.split("/")[-1]
        return end.split(".")[0]


class BNCFileWrapper:
    def __init__(self, root: str, file_path_from_root: str):
        self.info: BNCFileInfo = BNCFileInfo(root, file_path_from_root)

        self.root = root
        self.file_path_from_root = file_path_from_root

    def sentences(self) -> List[List[str]]:
        root, file = os.path.split(Path(self.root)/self.file_path_from_root)

        bnc_reader = BNCCorpusReader(
            root=root,
            fileids=file
        )
        return bnc_reader.sents()

    def sent_ct(self):
        return self.info.sent_ct


# todo: we might have been able to simply add spaces everywhere and then run a library to fix it all

# todo: how do we want to handle quotes, etc across multiple sentences
def bnc_corpus_sent_join(sent: List[str], print_warnings=False, raise_on_invalid=False):
    def _warn(warn_str: str):
        if print_warnings:
            print(warn_str)

    has_warn = False
    full_sent = ""

    # allow look back during parsing
    # normally we do add space before
    do_not_add_space_before_on_next_word = False

    for i, w in enumerate(sent):
        # reset the space tracker
        skip_space_this_iter = do_not_add_space_before_on_next_word
        do_not_add_space_before_on_next_word = False

        if len(w) == 0:
            _warn("WARN: length is 0")
            continue

        # just a normal non-punct word - normally gets a preceding space
        if not str_starts_with_punct(w):
            # e.g. if we had My friend (John)
            if skip_space_this_iter:
                full_sent += w
            else:
                full_sent += " " + w
            continue

        # so the str starts with punctuation

        # is it a punct + another character? -- it should be one of the following
        if str_starts_with_punct(w) and len(w) > 1:
            # only acceptable multipunct
            if w in ["..", "...", "...."]:
                _warn("WARN: ellipsis")
                has_warn = True
                full_sent += w
                do_not_add_space_before_on_next_word = True

            # check for bad formatting
            # sometimes the dash is not set off from following word
            elif w[0] in ["-", "—"]:
                # assert skip_space_this_iter is False, f"{w} starts with apostrophe but expects to skip space\n {sent}"
                _warn(f"WARN: badly formatted: {w}\n")
                has_warn = True
                full_sent += " " + w[0] + " " + w[1:]
            # otherwise, we expect, eg. (do, 'nt) or ($5)
            else:
                # decimals, pos/neg number, apostrophe, dollar sign
                if w[0] not in [
                    ".", "'", "$", "+", "-",
                    "/"     # maybe poetry - allow /<word>
                ]:
                    print(f"{w} starts with punct but length > 1\n{sent}")
                    if raise_on_invalid:
                        raise Exception
                if skip_space_this_iter:
                    _warn(f"aposrophe or dollar sign (idx ${i} but should skip space this iter \n{sent}")
                    has_warn = True
                full_sent += w

        # otherwise it should be punct only (and starts with punct)

        # some punctuation needs to be appended without space
        elif w[0] in [
            ",", ":", ";", ".", "?", "!", ")", "]",
            "'", "’", "%"
        ]:
            full_sent += w

        # this punct should be on its own and gets a space before but no space after
        elif w[0] in ["(", "[", "‘",
                      "$"]: # okay for the $ sign to be on its own (usually occurs with the following string)
            full_sent += " " + w
            # don't add space before
            do_not_add_space_before_on_next_word = True

        # space before and after (normal)
        elif w[0] in ["-","—", "&", "/", "+", "*", "=", "<", ">"]:
            full_sent += " " + w

        else:
            print(sent)
            print(f"unrecognized {w}")
            if raise_on_invalid:
                raise Exception

    if has_warn and print_warnings:
        print(full_sent)
        print("\n")

    return full_sent

def process_corpus_file(bnc_file: BNCFileWrapper, output_dir: Path):
    """
    Open input_file (a BNC corpus file, xml), and write each sentence
    to one line at output_dir/<file_id>
    """
    all_lines = []
    for s in bnc_file.sentences():
        sent = bnc_corpus_sent_join(s)
        all_lines.append(sent)
    out_file = output_dir / f"{bnc_file.info.file_id}.txt"
    with open(out_file, "w") as out_file:
        for l in all_lines:
            out_file.write(f"{l}\n")


# todo(low): this can probably be deleted
# gpt written
def pprint_limited(d: dict, max_depth: int, current_depth: int = 0) -> None:
    """
    Pretty-prints a dictionary up to a given level of nesting.

    Args:
        d (dict): The dictionary to pretty-print.
        max_depth (int): The maximum depth to print.
        current_depth (int): The current depth in the dictionary (used internally for recursion).
    """
    # Initialize a pretty printer
    pp = pprint.PrettyPrinter(indent=4)

    # If current depth exceeds max depth, print '...'
    if current_depth > max_depth:
        print("..." if isinstance(d, dict) else repr(d))
        return

    # If the current depth is within the limit, print the dictionary or sub-keys
    if isinstance(d, dict):
        print("{")
        for key, value in d.items():
            print(" " * (current_depth + 1) * 2, end="")
            print(repr(key) + ": ", end="")
            if isinstance(value, dict):
                pprint_limited(value, max_depth, current_depth + 1)
            # else:
            #     pp.pprint(value)
        print(" " * current_depth * 2 + "}")
    else:
        pp.pprint(d)
