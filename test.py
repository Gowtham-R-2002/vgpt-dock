import pyaudio

p = pyaudio.PyAudio()

print("Available input devices:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Input Device {i}: {info['name']}")

p.terminate()
