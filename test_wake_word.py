import pvporcupine
import pyaudio

# Replace with your actual access key
access_key = "k7i1JbJo74k4031rIsdVy7RKf5iH60DlN9h1f97zr1Q6eiGV6hseaA=="

# Path to the keyword files
keyword_paths = [
    r'D:\Desktop_BUD-E\hey-buddy_en_windows_v3_0_5.ppn',
    r'D:\Desktop_BUD-E\stop-buddy_en_windows_v3_0_5.ppn'
]

# Initialize Porcupine
porcupine = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)

# Initialize PyAudio
pa = pyaudio.PyAudio()

# Open audio stream
stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for wake words...")

try:
    while True:
        # Read audio data
        pcm = stream.read(porcupine.frame_length)
        # Process audio data
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print(f"Detected keyword: {keyword_paths[keyword_index]}")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()