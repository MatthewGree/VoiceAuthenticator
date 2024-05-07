from pathlib import Path
from typing import Dict, List, Literal, Iterable


def __retrieve_wav_paths(sample_path: Path) -> Iterable[Path]:
    content = sample_path.iterdir()
    wav_paths = filter(lambda path: path.suffix == ".wav", content)
    return wav_paths


def __wav_path_to_dict(wav_path: Path) -> Dict[str, str]:
    assert wav_path.suffix == ".wav"
    return {
        "wav_path": str(wav_path),
    }


def __sample_paths_to_wav_paths(sample_paths: Iterable[Path]) -> Iterable[Path]:
    wav_paths = []
    for sample_path in sample_paths:
        wav_paths.extend(__retrieve_wav_paths(sample_path))
    return wav_paths


def __id_path_to_annotation_dicts(id_path: Path) -> Iterable[Dict[str, str]]:
    assert id_path.is_dir()
    sample_paths = id_path.iterdir()
    wav_paths = __sample_paths_to_wav_paths(sample_paths)
    wav_dicts = list(map(lambda wav_path: __wav_path_to_dict(wav_path), wav_paths))
    user_id = id_path.stem
    for wav_dict in wav_dicts:
        wav_dict["user_id"] = user_id
    return wav_dicts


def data_path_to_annotation_list(data: Path, split: Literal["train", "test"]) -> List[Dict[str, str]]:
    assert data.is_dir()
    result_list = []
    wav_dir = data / "wav"
    assert wav_dir.is_dir()
    id_paths = wav_dir.iterdir()
    for id_path in id_paths:
        annotation_dicts = __id_path_to_annotation_dicts(id_path)
        for annotation_dict in annotation_dicts:
            annotation_dict["split"] = split
        result_list.extend(annotation_dicts)
    return result_list



