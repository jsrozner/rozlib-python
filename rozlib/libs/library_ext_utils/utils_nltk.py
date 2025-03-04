from dataclasses import dataclass

from nltk import TreebankWordTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from typing import List, Tuple

_detokenizer = TreebankWordDetokenizer()
_tokenizer = TreebankWordTokenizer()

@dataclass
class WordWithSpan:
    word: str
    span_start: int
    span_end: int

def get_word_spans_in_sent(
        text: str,
        words: List[str]
) -> List[WordWithSpan]:
    """
    For each word in words, get the original spans in the text.
    Tokenize text and retrieve tokens with their spans.

    Args:
        text (str): The original text.

    Returns:
        List[WordWithSpan]: List of tokens with (start, end) positions.
    """
    spans: List[WordWithSpan] = []
    index = 0
    for w in words:
        start = text.find(w, index)
        end = start + len(w)
        spans.append(WordWithSpan(w, start, end))
        index = end
    return spans

def get_token_spans(text: str) -> List[WordWithSpan]:
    """
    Tokenize text and retrieve tokens with their spans.

    Args:
        text (str): The original text.

    Returns:
        List[Tuple[str, Tuple[int, int]]]: List of tokens with (start, end) positions.
    """
    tokens = _tokenizer.tokenize(text)

    spans = get_word_spans_in_sent(text, tokens)

    return spans

@dataclass
class DetokenizedWord:
    word: str
    orig_offset: Tuple[int, int]
    new_offset: Tuple[int, int]

def detokenize_with_spans(text: str) -> Tuple[str, List[DetokenizedWord]]:
    """
    Map the tokens in the original text to the spans in the detokenized text.

    Args:
        text (str): The original text.

    Returns:
        Tuple[str, List[Tuple[str, Tuple[int, int]]]:
            - str that is the tokenized then detokenized input string
            - List of tuples of words back to their original offsets
    """
    original_spans = get_token_spans(text)
    original_tokens = [w.word for w in original_spans]

    # Detokenize using NLTK
    detokenized_text = _detokenizer.detokenize(original_tokens)

    # Map detokenized tokens to original spans
    all_words = []
    current_index = 0
    for token in original_tokens:
        if token in detokenized_text[current_index:]:
            start = detokenized_text.find(token, current_index)
            end = start + len(token)
            original_span = next((w.span_start, w.span_end) for w in original_spans if w.word == token)
            all_words.append(
                DetokenizedWord(
                    token,
                    original_span,
                    (start, end)
                ))
            current_index = end
        else:
            raise Exception(f"Warning: Token '{token}' not found in detokenized text.")
            # # Optionally add fallback logic, like skipping the token or assigning a placeholder span
            # detokenized_spans.append((token, (-1, -1)))
    return detokenized_text, all_words
