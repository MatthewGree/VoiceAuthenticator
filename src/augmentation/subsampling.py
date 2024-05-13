from pathlib import Path
import soundfile as sf
import os

def subsampling_audio(source_audio_file_path: Path, target_audio_file_path: Path, interval:int):
    """
    Subsamples audio files from the given path.

    Parameters:
        audio_file_path (str): path to the audio file,
        interval (int): the subsampling interval, which defines that every interval-th value from the original sound recording is retained.
    """
    
    audio, samplerate = sf.read(source_audio_file_path)
    audio_subsampled = audio[::interval]

    sf.write(file=target_audio_file_path, data=audio_subsampled, samplerate=samplerate//interval)