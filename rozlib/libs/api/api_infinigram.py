import time
from typing import NamedTuple, List

import requests

gpt_idx = 'v4_piletrain_llama'
query_type = 'count'
rate_limit_err = "Too Many Requests"

class InfinigramResult(NamedTuple):
    approx: bool
    count: int
    latency: float
    token_ids: List[int]
    tokens: List[str]

# @cachetools.func.lru_cache(maxsize=4000)
def check_infinigram(
        query_ngram: str,
        retries: int = 5,
        sleep_time = 0.2
) -> InfinigramResult:
    payload = {
        'index': gpt_idx,
        'query_type': query_type,
        'query': query_ngram
    }
    tries = 0
    while tries < retries:
        tries += 1
        try:
            result = requests.post('https://api.infini-gram.io/', json=payload).json()
            if result.get('message') == rate_limit_err:
                # print(f"rate limit {sleep_time}")
                time.sleep(sleep_time)
                sleep_time *= 2
                continue
            return InfinigramResult(**result)
        except Exception as e:
            print("except")
            continue

    raise Exception("Unable to process")

