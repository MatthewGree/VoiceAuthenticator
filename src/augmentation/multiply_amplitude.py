import os
from pathlib import Path
import random
import numpy as np
from pydub import AudioSegment

def multiply_amplitude(source_file_path: Path, target_file_path: Path):
    multipliers = [25, 1, 0.04]
    audio = AudioSegment.from_file(source_file_path)
    multiplier = random.choice(multipliers)
    # Convert multiplier to decibels
    gain_in_db = 20 * np.log10(multiplier)
    augmented_audio = audio.apply_gain(gain_in_db)
    augmented_audio.export(target_file_path, format='wav')
