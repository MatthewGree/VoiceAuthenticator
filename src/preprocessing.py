import noisereduce as nr
import soundfile as sf
import os
import librosa

def gaussian_noise_reduce(audio_file_path):
    """
    Reduces noise.

    Parameters:
        audio_file_path (str): path to the audio file
    """

    audio, samplerate = librosa.load(audio_file_path, sr=None)
    
    reduced_audio = nr.reduce_noise(y=audio, sr=samplerate, stationary=True)

    base, ext = os.path.splitext(audio_file_path)
    new_file_path = f"{base}_reduced_noise{ext}"

    sf.write(file=new_file_path, data=reduced_audio, samplerate=samplerate)