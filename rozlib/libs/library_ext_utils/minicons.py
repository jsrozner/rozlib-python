from typing import List, Union

import torch
from minicons import scorer

from rozlib.libs.library_ext_utils.utils_torch import get_device


class ILMWrapper_l2r():
    def __init__(self,
                 model: Union[str, torch.nn.Module] = 'roberta-large',
                 tokenizer = None,
                 **kwargs
                 ):
        if not isinstance(model, str):
            assert tokenizer is not None, "If you provide a model, you need to provide a tokenizer"
        self.ilm = scorer.MaskedLMScorer(model, device=get_device(), tokenizer=tokenizer, **kwargs)

    def l2r(self, stimuli: List[str]):
        return self.ilm.sequence_score(stimuli, reduction = lambda x: -x.sum(0).item(), PLL_metric='within_word_l2r')
