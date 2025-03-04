from functools import lru_cache

import spacy
from spacy.tokens import Token

nlp = spacy.load('en_core_web_trf')
def spacy_explain_all(model = nlp):
    for label in model.get_pipe("parser").labels:
        print(label, " -- ", spacy.explain(label))
    for label in model.get_pipe("tagger").labels:
        print(label, " -- ", spacy.explain(label))

class NLPWithCache:
    def __init__(self, model_name="en_core_web_trf"):
        print(f"Initialized NLP with model name {model_name} and cache")
        self.nlp = spacy.load(model_name)

    @lru_cache
    def __call__(self, sent: str):
        return self.nlp(sent)

def get_child_with_dep(token: Token, dep_label: str):
    matching = []
    for child in token.children:
        if child.dep_ == dep_label:
            matching.append(child)

    if len(matching) == 0:
        return None
    if len(matching) > 1:
        raise Exception("more than one match")
    return matching[0]

def spacy_print_tokens(nlp, sentence: str):
    # Process the sentence
    doc = nlp(sentence)

    # Extract Universal Dependency labels and head-dependent relationships
    for token in doc:
        print(f"Word: {token.text}")
        print(f"  Dependency Label (dep_): {token.dep_}")
        print(f"  Head: {token.head.text}")
        print(f"  Head POS: {token.head.pos_}")
        print(f"  Syntactic Relation: {token.head.text} <-[{token.dep_}]- {token.text}")
        print(list(token.subtree))
