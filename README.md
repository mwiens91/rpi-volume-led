[![Python version](https://img.shields.io/badge/python-3.5%20|%203.6%20|%203.7-blue.svg)](https://github.com/mwiens91/rpi-volume-led)

# rpi-volume-led

Light up an LED with your Raspberry Pi's audio output! We ([Tyler
Trinh](https://github.com/bvtrinh) + [Matt
Wiens](https://github.com/mwiens91)) used a Raspberry Pi (RPi) 3 model
B, with Ubuntu MATE running as the OS. Likely this will work on older
(and newer, once they're out) RPis, too.

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

Wire up a breadboard as shown below, making sure that the longer end of
the LED is in the same row as the resistor (which should be around 270
ohms).  In the left column of the RPi pins, starting from the bottom,
the third pin is ground and the sixth pin powers the LED, and is
identified as pin 12 from within the program.

![Breadboard Wiring](https://i.imgur.com/viCKkxp.jpg)

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

You can also specify multiple pins using the `-p` option.

## Running it

To run the program normally run

```
sudo ./rpi_volume_led
```

and hit `enter` whenever you're done to tell the program to clean up and exit.

## See also

[rpi-led-lightshow](https://github.com/mwiens91/rpi-led-lightshow),
which is an expanded version of this project.
