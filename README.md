# rpi-volume-led

Light up an LED with your Raspberry Pi's volume! We (Tyler Trinh + Matt Wiens)
used a Raspberry Pi (RPi) 3 model B, with Ubuntu MATE running as the OS. Likely
this will work on older (and newer, once they're out) RPis, too.

## Audio processing

Audio is captured from your computer with PyAudio, which on Ubuntu you can
install with

```
sudo apt install python3-pyaudio
```

Make sure your firmware is up to date as well. If it isn't, you might run into
audio issues (like we did). To upgrade to the latest firmware run

```
sudo rpi-update
```

If you want to test whether the audio processing works, run

```
./rpi_volume_led.py --test-pyaudio
```

and if it works you should see the RMS of your audio output being printed to the
terminal. Note that this test runs independent of the Raspberry Pi, so it
will run on any machine.

## Hooking up the LED

Wire the breadboard as shown below. Make sure that the longer end of the LED is
in the same row as the resistor. The resistor should be around 270 ohms.

![Breadboard Wiring](https://i.imgur.com/ZAfSl3F.jpg)

To test that the LED is properly connected, run

```
sudo ./rpi_volume_led.py --test-led
```

and the LED should start pulsing a few times. (Note that we need to run the
program as root now that we've started using the RPis GPIO pins.) If you
used a different pin from pin 12, say, pin 18, you can specify the number using
the `-p` option:

```
sudo ./rpi_volume_led --test-led -p 18
```

## Running it

To run the program normally run

```
sudo ./rpi_volume_led
```

and hit `enter` whenever you're done to tell the program to clean up and exit.
