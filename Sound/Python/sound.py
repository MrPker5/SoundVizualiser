import pyaudio
import audioop
import time
import serial

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 60
WAVE_OUTPUT_FILENAME = "output.wav"

max_volume = 4500

ser = serial.Serial('COM4', 9600)
# total_volumes =[]

def volTo256Range(rms):
    return int(rms / max_volume * 255) 


p = pyaudio.PyAudio()
device_info = p.get_device_info_by_index(6)

stream = p.open(format = pyaudio.paInt16,
                channels = 8,
                rate = int(device_info["defaultSampleRate"]),
                input = True,
                frames_per_buffer = 512,
                input_device_index = device_info["index"],
                as_loopback = True)

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    time.sleep(0.01667)
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)
    if(rms > max_volume):
        max_volume = rms
    
    rms = volTo256Range(rms)
    print(rms)
    data = bytes([int(rms)])
    ser.write(data)


# print("max: " + str(max(total_volumes)))
stream.stop_stream()
stream.close()
p.terminate()

