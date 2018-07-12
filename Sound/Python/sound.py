import pyaudio
import audioop
import time
import serial
import threading
from pynput.keyboard import Key, Listener
from win10toast import ToastNotifier

class SoundAnalyzer:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.RECORD_SECONDS = 60
        self.windowsNotification = ToastNotifier()
        self.max_volume = 4500
        self.oldtime = time.time()
        self.stopped = False
        

    def volTo256Range(self, rms):
        return int(rms / self.max_volume * 64) 

    def StartAnalyzing(self):
        self.thread = threading.Thread(name='Analyze', target=self.analyzeSound)
        self.thread.setDaemon(True)
        self.thread.start()

    def StopAnalyzing(self):
        self.shouldAnalyze = False

    def setStop(self):
        if not self.stopped:
            self.stopped = True
            self.showIdleNotification()
        else:
            self.stopped = False
            self.showStartNotification()

    def getStop(self):
        return self.stopped

    def showStartNotification(self):
        self.windowsNotification.show_toast("Starting...",
                   "Starting sound analyzing!",
                   icon_path="soundicon.ico",
                   duration=2,
                   threaded=True)
        
    def showIdleNotification(self):
        self.windowsNotification.show_toast("Idle...",
                   "Now in Idle Mode!",
                   icon_path="soundicon.ico",
                   duration=2,
                   threaded=True)
       
    def openArduinoSerial(self):
        self.arduinoSerial = serial.Serial('COM5', 9600)
    
    def resetMaxVolume(self):
        self.max_volume = 4500

    def analyzeSound(self):
        self.openArduinoSerial()
        self.shouldAnalyze = True
        p = pyaudio.PyAudio()
        device_info = p.get_device_info_by_index(6)

        stream = p.open(format = pyaudio.paInt16,
                        channels = 8,
                        rate = int(device_info["defaultSampleRate"]),
                        input = True,
                        frames_per_buffer = 512,
                        input_device_index = device_info["index"],
                        as_loopback = True)

        while self.shouldAnalyze:
            time.sleep(0.01667)
            data = stream.read(self.CHUNK)
            rms = audioop.rms(data, 2)
            if(rms > self.max_volume):
                self.max_volume = rms
            if(time.time() - self.oldtime > 600):
                self.oldtime = time.time()
                self.resetMaxVolume()

            rms = self.volTo256Range(rms)
            data = bytes([int(rms)])
            self.arduinoSerial.write(data)

        stream.stop_stream()
        stream.close()
        p.terminate()
        self.arduinoSerial.close()

SA = SoundAnalyzer()
SA.StartAnalyzing()

def on_press(key):
    if(key == Key.pause):
        if not SA.getStop():
            SA.setStop()
            SA.StopAnalyzing()
        else:
            SA.StartAnalyzing()
            SA.setStop()
            
with Listener(on_press=on_press) as listener:
    listener.join()