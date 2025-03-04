import re
import string
from typing import List

import toolz as tz

from rozlib.libs.library_ext_utils.utils_transformer import ROBERTA_SPACE_START_CHAR

_punctuation = string.punctuation + """‘’–"""

def contains_alpha_num(input: str) -> bool:
    return any(char.isalnum() for char in input)

def is_numeric(input: str) -> bool:
    return bool(re.match(r'^[0-9]+$', input))

def is_any_alphanumeric(input: str) -> bool:
    return input.isalpha() or is_english_alphanumeric(input)

def is_english_alphanumeric(string: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9]+$', string))

def str_starts_with_punct(input: str):
    return input[0] in _punctuation


def str_all_punct(input: str):
    return all([c in _punctuation for c in input])


def str_has_punct(input: str):
    return any([c in _punctuation for c in input])


def str_is_mixed(input: str):
    has_alpha = False
    has_punct = False
    has_num = False
    if input == "<s>" or input == "</s>":
        return False
    for c in input:
        if c.isspace():
            raise Exception(f"Unexpected space in {input}")
        elif c == ROBERTA_SPACE_START_CHAR:
            continue
        elif c.isalpha():
            has_alpha = True
        elif c.isnumeric():
            has_num = True
        elif c in _punctuation:
            has_punct = True
        #todo: we should maybe line this up with corpus_bnc character processing
        else:
            # just treat it as punct
            has_punct = True
            print(f"Unrecognized character in {input}, {c}")

    # fcn could be better if it failed fast
    if sum([has_punct, has_num, has_alpha]) != 1:
        # print(f"WARNING {input} has alpha/punct/num")
        return True
    return False

def split_and_remove_punct(input: str) -> List[str]:
    def _strip_punct_if_not_mask(x: str):
        # use startswith in case has trailing punctuation
        # todo: verify this
        if x.startswith("<mask>"):
            return "<mask>"
        # todo: should only be a special case
        elif x.startswith("<mask2>"):
            return "<mask2>"
        return x.strip(_punctuation)
    _split_and_remove_punct = tz.compose(
        list,
        # todo: make sure does not remove internal punct
        tz.curried.filter(lambda x: x != ""),
        # tz.curried.map(lambda x: x.strip(_punctuation)),
        tz.curried.map(_strip_punct_if_not_mask),
        # lambda x: x.split(" ")
        lambda x: x.split()
    )
    initial_list = _split_and_remove_punct(input)
    # print(initial_list)
    final_list = []
    # we are going to require that all strs start with alphanum (e.g. $100 -> $, 100)
    for elt in initial_list:
        if elt in ["<mask>", "<mask2>"]:
            final_list.append(elt)
            continue
        c_idx = 0
        while c_idx < len(elt) and not is_english_alphanumeric(elt[c_idx]):
            # final_list.append(elt[c_idx])
            # we just omit it, we don't keep it
            c_idx += 1
        if c_idx < len(elt):
            final_list.append(elt[c_idx:])

    # todo: check that any internal punct is only one
    return final_list


