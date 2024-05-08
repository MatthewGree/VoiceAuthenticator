from pathlib import Path
from typing import List, Tuple

import torch
import torch.nn.functional as F
import torchaudio
from speechbrain.inference.speaker import EncoderClassifier
from torchaudio.transforms import Resample


def __pad_2d_tensors(tensors: List[torch.Tensor]) -> List[torch.Tensor]:
    max_rows = max(tensor.size(0) for tensor in tensors)
    max_cols = max(tensor.size(1) for tensor in tensors)

    padded_tensors = [
        F.pad(
            tensor,
            (0, max_cols - tensor.size(1), 0, max_rows - tensor.size(0)),
            "constant",
            0
        ) for tensor in tensors
    ]
    return padded_tensors


def __load_audio_files(audio_paths: List[Path], sample_rate: int) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    returns a tuple of tensors
    [audio_batch[batch_size, channel, time], relative_lengths[batch_size]]
    """
    audio_list = []
    lengths = []

    for path in audio_paths:
        # waveform - (channel, time)
        waveform, orig_sample_rate = torchaudio.load(path)
        if orig_sample_rate != sample_rate:
            resampler = Resample(orig_freq=orig_sample_rate, new_freq=sample_rate)
            waveform = resampler(waveform)
        audio_list.append(waveform)
        lengths.append(waveform.shape[1])

    # Find the maximum length
    max_length = max(lengths)

    # Pad sequences and stack into a single tensor
    padded_audio_list = __pad_2d_tensors(audio_list)
    audio_batch = torch.stack(padded_audio_list, dim=0)

    # Normalize lengths by maximum length to get relative lengths
    relative_lengths = torch.tensor(lengths) / max_length

    return audio_batch, relative_lengths


def create_speechbrain_embedding(model: EncoderClassifier, audio_path: Path, sample_rate=16000) -> torch.Tensor:
    signal = __load_audio_files([audio_path], sample_rate)[0].squeeze(dim=0)
    embedding = model.encode_batch(signal)
    squeezed_embedding = embedding.squeeze().cpu()
    return squeezed_embedding


def batch_create_speechbrain_embedding(model: EncoderClassifier, audio_paths: List[Path],
                                       sample_rate=16000) -> List[torch.Tensor]:
    if len(audio_paths) == 0:
        return []
    elif len(audio_paths) == 1:
        return [create_speechbrain_embedding(model, audio_paths[0], sample_rate)]
    batch, wav_lens = __load_audio_files(audio_paths, sample_rate=sample_rate)
    embeddings = model.encode_batch(wavs=batch, wav_lens=wav_lens).cpu()
    assert len(embeddings.shape) >= 2, \
        f"Expected embeddings to have at least two dimensions, got shape: {embeddings.shape}"
    assert embeddings.shape[0] == len(audio_paths), \
        f"Batch size found {embeddings.shape[0]} does not equal the number of audio paths: {len(audio_paths)}"

    tensor_list = [row for row in embeddings]
    return tensor_list
