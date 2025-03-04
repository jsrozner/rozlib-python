import logging
import warnings
from typing import List

import torch

def get_device_mps():
    if not torch.backends.mps.is_available():
        raise Exception("no mps")
    return torch.device('mps')

def get_device(assert_mps_or_gpu=True):
    """
    Returns the best available device (GPU or CPU), and prints available GPUs.
    Checks for:
      - CUDA (NVIDIA GPUs)
      - MPS (Apple Silicon GPU)
    """
    if torch.cuda.is_available():
        # Print available CUDA devices
        num_gpus = torch.cuda.device_count()
        logging.info(f"CUDA is available. {num_gpus} GPU(s) detected:")
        for i in range(num_gpus):
            logging.info(f"  - GPU {i}: {torch.cuda.get_device_name(i)}")
        return torch.device('cuda')

    elif torch.backends.mps.is_available():
        # If MPS (Apple Silicon) is available
        logging.info("MPS is available (Apple Silicon GPU).")
        return torch.device('mps')

    if assert_mps_or_gpu:
        raise Exception("neither cuda nor mps available")
    else:
        # Fallback to CPU
        logging.warning("No GPU found. Using CPU.")
        return torch.device('cpu')

# todo(low): might not need this; might interact with our other rounding
# (should round in the dataclass?)
def round_tensor(tensor: torch.Tensor, decimals: int = 3) -> float | List[float]:
    warnings.warn(f"Round_tensor is being called. Avoid using this in actual 'production' code")
    if tensor.dim() == 0:
        return round(tensor.item(), decimals)
    elif tensor.dim() == 1:
        return [round(x, decimals) for x in list(tensor)]
    else:
        raise Exception("invalid dim")

def torch_fill_diagonal(orig_tensor: torch.Tensor, fill_with: torch.Tensor):
    """
    In place writes fill_with to the diagonal of orig_tensor
    """
    if len(orig_tensor.shape) != 2:
        raise Exception("Expects orig_tensor of 2D")
    if orig_tensor.shape[0] != orig_tensor.shape[1]:
        raise Exception("orig tensor is not square")
    if fill_with.shape[0] != orig_tensor.shape[0]:
        raise Exception("fill tensor length does not match size of orig_tensor")
    orig_tensor[range(len(fill_with)), range(len(fill_with))] = fill_with
