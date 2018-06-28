# SoundVizualiser
## A small audio visualizer script that runs on python
The script sends the output volume of goes to your speakers and sends it to a arduino,
right now i do not have a WS2812b led strip but that is coming shortly. For now i made small test setup
that will represent the way the led strip would work.

## Libraries
I am using a fork of PyAudio with the integration of PortAudio. This fork works with the new WASAPI protocol from new windows versions.
With this WASAPI protocol you can enable loopback end listen to your speakers and get data from it.

[PyAudio with PortAudio](https://github.com/intxcc/pyaudio_portaudio)

Use the example echo script from the PyAudio/PortAudio fork and run it at least once to check which
device index you need to use to listen to audio from the speakers.

