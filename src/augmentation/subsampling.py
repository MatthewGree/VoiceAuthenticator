import soundfile as sf
import os

def subsampling_audio(audio_file_path:str, interval:int):
    """
    Subsamples audio files from the given path.

    Parameters:
        audio_file_path (str): path to the audio file,
        interval (int): the subsampling interval, which defines that every interval-th value from the original sound recording is retained.
    """
    
    audio, samplerate = sf.read(audio_file_path)
    audio_subsampled = audio[::interval]

    base, ext = os.path.splitext(audio_file_path)
    new_file_path = f"{base}_subsampling_{interval}{ext}"

    sf.write(file=new_file_path, data=audio_subsampled, samplerate=samplerate//interval)