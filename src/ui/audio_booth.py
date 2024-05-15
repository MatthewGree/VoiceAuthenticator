import wave

import pyaudio
from kivy.clock import Clock
from kivy.core.text import Label
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


class AudioBooth(BoxLayout):
    def __init__(self, **kwargs):
        super(AudioBooth, self).__init__(**kwargs)
        self._audio_stream = None
        self._audio_frames = []
        self._recording = False
        self._audio_file_path = "audio/recording.wav"
        self._sample_rate = 16000  # Set the sample rate to 16000 Hz

        # Recording status label
        self._status_label = Label(text='Press "Start Recording" to begin', size_hint=(1, 0.2))
        self.add_widget(self._status_label)

        # Start recording button
        start_recording_button = Button(text='Start Recording', size_hint=(1, 0.4))
        start_recording_button.bind(on_press=self._start_recording)
        self.add_widget(start_recording_button)

        # Stop recording button
        stop_recording_button = Button(text='Stop Recording', size_hint=(1, 0.4))
        stop_recording_button.bind(on_press=self._stop_recording)
        self.add_widget(stop_recording_button)

    def _start_recording(self, _):
        if self._recording:
            return
        self._recording = True
        self._audio_frames = []
        self._status_label.text = 'Recording...'

        p = pyaudio.PyAudio()
        self._audio_stream = p.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self._sample_rate,
                                    input=True,
                                    frames_per_buffer=1024)

        Clock.schedule_interval(self._record_audio, 1.0 / 30.0)

    def _record_audio(self, _):
        if self._recording:
            data = self._audio_stream.read(1024)
            self._audio_frames.append(data)

    def _stop_recording(self, _):
        if not self._recording:
            return
        self._recording = False
        self._audio_stream.stop_stream()
        self._audio_stream.close()

        p = pyaudio.PyAudio()
        wf = wave.open(self._audio_file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self._sample_rate)
        wf.writeframes(b''.join(self._audio_frames))
        wf.close()

        self._status_label.text = 'Recording saved to {}'.format(self._audio_file_path)

    def release_audio_resources(self):
        if self._audio_stream is not None:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
