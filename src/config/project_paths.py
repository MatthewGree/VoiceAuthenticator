from pathlib import Path
from typing import Literal
import os


def get_project_root_path() -> Path:
    return Path(__file__).resolve().parents[2]

def __get_data_path() -> Path:
    return get_project_root_path() / "data"


def get_model_save_dir(model_name: str) -> Path:
    return get_project_root_path() / "pretrained_models" / model_name


def get_data_file_path(data_file: str) -> Path:
    generated_path = __get_data_path() / "generated"
    generated_path.mkdir(parents=True, exist_ok=True)
    return generated_path / data_file


def get_voxceleb1_metadata_path() -> Path:
    return __get_data_path() / "vox1_vox1_meta.csv"


def get_voxceleb2_metadata_path() -> Path:
    return __get_data_path() / "vox2_vox2_meta.csv"


def get_voxceleb_path(split: Literal["train", "test"]) -> Path:
    split_discriminator = "dev" if split == "train" else "test"
    return __get_data_path() / f"vox1_{split_discriminator}_wav"


def get_voxceleb2_path() -> Path:
    return __get_data_path() / "vox2_test" / "mp4"

def get_voxceleb2_wav_path() -> Path:
    return __get_data_path() / "vox2_test" / "wav"

def create_wav_dir_if_not_exists(id_path: Path):
    wav_path = os.path.join(get_voxceleb2_wav_path(), id_path)
    os.makedirs(os.path.join(wav_path, id_path), exist_ok=True)


