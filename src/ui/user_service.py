import os
import pickle
from typing import List

import logging


class UserService:
    def __init__(self):
        self.all_user_path: str = "photos/user_photos"
        self.user_processed_photo_filename = "processed_photo.jpg"
        self.user_embedding_filename = "user_embedding.pkl"
        self._logger = logging.getLogger(self.__class__.__name__)

    def register_user(self, nickname: str, photo_path: str) -> None:
        user_path = self.__get_user_data_path(nickname)
        self.__save_authentication_data(photo_path, user_path)

    def login_user(self, nickname: str, photo_path: str) -> bool:
        user_path: str = self.__get_user_data_path(nickname)
        return self.__verify_authentication_data(photo_path, user_path)

    def __get_user_data_path(self, nickname: str) -> str:
        user_path: str = os.path.join(self.all_user_path, nickname)
        os.makedirs(user_path, exist_ok=True)
        return user_path

    def __save_authentication_data(self, original_photo_path: str, user_data_path: str) -> None:
        processed_photo_path = os.path.join(user_data_path, self.user_processed_photo_filename)
        embedding_path = os.path.join(user_data_path, self.user_embedding_filename)
        #processed_image = preprocess_image(original_photo_path)
        #cv2.imwrite(processed_photo_path, processed_image)
        #embedding: List[float] = DeepFace.represent(img_path=processed_image, model_name='OpenFace')[0]['embedding']
        #pickle.dump(embedding, open(embedding_path, "wb"))

    def __verify_authentication_data(self, original_photo_path: str, user_data_path: str) -> bool:
        embedding_path = os.path.join(user_data_path, self.user_embedding_filename)
        #processed_image = preprocess_image(original_photo_path)
        #login_embedding: List[float] = DeepFace.represent(img_path=processed_image, model_name='OpenFace')[0][
        #    'embedding']
        #correct_embedding: List[float] = pickle.load(open(embedding_path, "rb"))
        #distance = verification.find_distance(correct_embedding, login_embedding, distance_metric='cosine')
        #if distance < 0.1:
        #    self._logger.info(f"Data verified, embedding distance is {distance}")
        #    return True
        #else:
        #    self._logger.info(f"Data verification failed, embedding distance is {distance}")
        #    return False
        return True
