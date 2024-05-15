import os
import pickle
from typing import List
import shutil

import logging

import torch
from speechbrain.inference import EncoderClassifier
from src.config import project_paths
from src.embedding.create_embedding import create_speechbrain_embedding
from pathlib import Path
import torch.nn.functional as F


class UserService:
    def __init__(self):
        self.__all_user_path: Path = project_paths.get_project_root_path() / "src/ui/audio/user_audios"
        self.__user_processed_audio_filename = "saved_audio.wav"
        self.__user_embedding_filename = "user_embedding.pkl"
        self._logger = logging.getLogger(self.__class__.__name__)
        self.__encoding_model = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",
                                                               savedir=project_paths.get_model_save_dir(
                                                                   "speechbrain/spkrec-ecapa-voxceleb")
                                                               )

    def register_user(self, nickname: str, audio_path: Path) -> None:
        user_path = self.__get_user_data_path(nickname)
        self.__save_authentication_data(audio_path, user_path)

    def login_user(self, nickname: str, audio_path: Path) -> bool:
        user_path: Path = self.__get_user_data_path(nickname)
        return self.__verify_authentication_data(audio_path, user_path)

    def __get_user_data_path(self, nickname: str) -> Path:
        user_path: Path = self.__all_user_path / nickname
        os.makedirs(user_path, exist_ok=True)
        return user_path

    def __save_authentication_data(self, original_audio_path: Path, user_data_path: Path) -> None:
        processed_audio_path: Path = user_data_path / self.__user_processed_audio_filename
        embedding_path: Path = user_data_path / self.__user_embedding_filename
        shutil.copyfile(original_audio_path, processed_audio_path)
        embedding: torch.Tensor = create_speechbrain_embedding(self.__encoding_model, processed_audio_path,
                                                               sample_rate=16000)
        pickle.dump(embedding, open(embedding_path, "wb"))

    def __cosine_similarity(self, tensor1: torch.Tensor, tensor2: torch.Tensor) -> float:
        # Ensure the input tensors are 1-dimensional
        if tensor1.dim() != 1 or tensor2.dim() != 1:
            raise ValueError("Both input tensors must be 1-dimensional")

        # Compute the cosine similarity
        cosine_sim = F.cosine_similarity(tensor1.unsqueeze(0), tensor2.unsqueeze(0)).item()

        return cosine_sim

    def __verify_authentication_data(self, original_audio_path: Path, user_data_path: Path) -> bool:
        embedding_path = user_data_path / self.__user_embedding_filename
        login_embedding: torch.Tensor = create_speechbrain_embedding(self.__encoding_model, original_audio_path,
                                                                     sample_rate=16000)
        correct_embedding: torch.Tensor = pickle.load(open(embedding_path, "rb"))
        similarity = self.__cosine_similarity(login_embedding, correct_embedding)
        if similarity > 0.75:
            self._logger.info(f"Data verified, embedding similarity is {similarity}")
            return True
        else:
            self._logger.info(f"Data verification failed, embedding similarity is {similarity}")
            return False
