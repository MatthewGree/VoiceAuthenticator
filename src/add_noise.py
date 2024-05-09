import os
import numpy as np
from pydub import AudioSegment

def add_noise_to_audio(audio_file_path, noise_file_path = '../data/labrador-barking.wav'):
    audio = AudioSegment.from_file(audio_file_path)
    noise = AudioSegment.from_file(noise_file_path)

    max_amplitude = max(audio.get_array_of_samples())
    noise = noise - 20 * np.log10(2 * max(noise.get_array_of_samples()) / max_amplitude)
    audio_with_noise = audio.overlay(noise)

    base, ext = os.path.splitext(audio_file_path)
    new_file_path = f"{base}_with_noise{ext}"
    audio_with_noise.export(new_file_path, format='wav')
