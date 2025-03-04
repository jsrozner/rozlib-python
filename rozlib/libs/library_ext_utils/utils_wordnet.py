from typing import Optional

from nltk.corpus.reader import Lemma



def lemma_to_string(x: Lemma) -> str:
    # todo: verify this works as expected
    return x.name().replace("_", " ")


def spacy_to_wordnet_pos(spacy_pos: str) -> Optional[str]:
    """
    Map a SpaCy POS tag to a WordNet POS tag.

    :param spacy_pos: SpaCy's part-of-speech tag (e.g., NOUN, VERB, etc.).
    :return: The corresponding WordNet POS tag (e.g., 'n', 'v', etc.).
    """
    if spacy_pos == 'NOUN':
        # return wn.NOUN  # 'n'
        return "noun"  # 'n'
    # todo: think about whether we want this
    elif spacy_pos == 'PROPN':
        # return wn.ADJ   # 'a'
        return "noun"
    elif spacy_pos == 'VERB':
        # return wn.VERB  # 'v'
        return "verb"  # 'v'
    elif spacy_pos == 'ADJ':
        # return wn.ADJ   # 'a'
        return "adj"
    # todo: no adverbs?
    # elif spacy_pos == 'ADV':
    #     return wn.ADV   # 'r'
    else:
        return None  # No corresponding POS in WordNet
