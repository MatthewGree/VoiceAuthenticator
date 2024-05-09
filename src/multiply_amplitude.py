import os
import random
import numpy as np
from pydub import AudioSegment

def multiply_amplitude(file_path):
    multipliers = [25, 1, 0.04]
    audio = AudioSegment.from_file(file_path)
    multiplier = random.choice(multipliers)
    # Convert multiplier to decibels
    gain_in_db = 20 * np.log10(multiplier)
    augmented_audio = audio.apply_gain(gain_in_db)

    base, ext = os.path.splitext(file_path)
    new_file_path = f"{base}_multiplied_amplitude{ext}"
    augmented_audio.export(new_file_path, format='wav')
