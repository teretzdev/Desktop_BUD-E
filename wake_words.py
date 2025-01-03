import pvporcupine  # For wake word detection
import pvrecorder  # For audio recording

import subprocess  # For running system commands
import os  # For environment variables and file operations


wake_words = ["hey-buddy", "stop-buddy"]

def get_wake_words():
   return wake_words

class WakeWordEngine:
    def __init__(self, wake_words, callback):
        self.wake_words = wake_words
        self.callback = callback
        self.recorder = None
        self.engine = None

    def initialize(self):
        access_key = "k7i1JbJo74k4031rIsdVy7RKf5iH60DlN9h1f97zr1Q6eiGV6hseaA=="  # Your actual key
        keyword_paths = [f"{word}_en_windows_v3_0_11.ppn" for word in self.wake_words]
        self.engine = pvporcupine.create(access_key=access_key, keyword_paths=['hey-buddy_en_windows_v3_0_11.ppn'])
        self.recorder = pvrecorder.PvRecorder(device_index=-1, frame_length=self.engine.frame_length)
        self.recorder.start()

    def cleanup(self):
        if self.recorder:
            self.recorder.stop()
            self.recorder.delete()
        if self.engine:
            self.engine.delete()

    async def detect(self):
        try:
            while True:
                frames = self.recorder.read()
                keyword_index = self.engine.process(frames)
                if keyword_index >= 0:
                    await self.callback()
                    break  # Break loop after detection
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self.cleanup()
