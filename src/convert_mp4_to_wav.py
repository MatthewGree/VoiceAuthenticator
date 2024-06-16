from moviepy.editor import VideoFileClip

def extract_audio_from_mp4(mp4_path, wav_path):
    video = VideoFileClip(mp4_path)
    audio = video.audio
    audio.write_audiofile(wav_path)
    video.close()
    audio.close()
    
    
    
    
    