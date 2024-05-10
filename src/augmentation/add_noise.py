import os
import numpy as np
from pydub import AudioSegment
import soundfile as sf

def add_noise_from_file(audio_file_path, noise_file_path = '../data/labrador-barking.wav'):
    audio = AudioSegment.from_file(audio_file_path)
    noise = AudioSegment.from_file(noise_file_path)

    max_amplitude = max(audio.get_array_of_samples())
    noise = noise - 20 * np.log10(2 * max(noise.get_array_of_samples()) / max_amplitude)
    audio_with_noise = audio.overlay(noise)

    base, ext = os.path.splitext(audio_file_path)
    new_file_path = f"{base}_with_noise{ext}"
    audio_with_noise.export(new_file_path, format='wav')


def add_gaussian_noise(audio_file_path:str, loc:float = 0.0, scale:float = 1.0):
    """
    Adds gaussian noise to audio.

    Parameters:
        audio_file_path (str): path to the audio file,
        loc (float): mean of the distribution,
        scale (float): standard deviation of the distribution
    """

    audio, samplerate = sf.read(audio_file_path)
    noise = np.random.normal(loc=loc, scale=scale, size=audio.shape[0])

    max_amplitude_audio = max(np.abs(audio)).item()
    max_amplitude_noise = max(np.abs(noise)).item()

    reduced_noise = noise * (max_amplitude_audio / (2 * max_amplitude_noise)) # noise with an amplitude of half the maximum amplitude of the base audio

    audio_noise = audio + reduced_noise

    base, ext = os.path.splitext(audio_file_path)
    new_file_path = f"{base}_gaussian_noise_loc_{loc}_scale_{scale}{ext}"

    sf.write(file=new_file_path, data=audio_noise, samplerate=samplerate)