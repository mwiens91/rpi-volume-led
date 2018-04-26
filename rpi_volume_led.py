#!/usr/bin/env python3
"""Light up an LED with sound on your Raspberry Pi!."""

import audioop
import argparse
import time
import sys
import pyaudio


# Program info
NAME = "rpi-volume-led"
VERSION = "0.0.1"
DESCRIPTION = "light up an LED with sound on your Raspberry Pi!"

# Audio stream settings
FRAMES_PER_BUFFER = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100    # Hz

# Duty cycle change delay for LED test
DC_CHANGE_DELAY = 0.005    # seconds

# Starting maximum volume
max_rms = 1


def main():
    """Main function for rpi-volume-led."""
    # Get runtime arguments
    runtime_args = parse_runtime_args()

    if runtime_args.test_led or not runtime_args.test_pyaudio:
        # Import stuff for the Raspberry PI GPIO
        import RPi.GPIO as GPIO

    # Pulse the LED if we're testing that
    if runtime_args.test_led:
        # Pulse the LED a few times
        pulse_LED(7, runtime_args.pin_number, runtime_args.silent)
        sys.exit(0)

    # Setup PyAudio stuff
    p = pyaudio.PyAudio()

    # Setup GPIO stuff
    if not runtime_args.test_pyaudio:
        # Setup the GPIO pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.OUT)

        # And use pulse width modulation
        pwm = GPIO.PWM(pin_number, 100) # pin number, frequency
        pwm.start(0)

    def callback(data, frame_count, time_info, status):
        """Callback function to process sound."""
        global max_rms
        rms = audioop.rms(data, 2)      # calculate volume
        max_rms = max(max_rms, rms)     # determine max volume

        # Compute duty cycle
        dc = rms / max_rms * 100 if rms < max_rms else 100

        # Change the duty cycle
        if not runtime_args.test_pyaudio:
            pwm.ChangeDutyCycle(dc)

        # Print some info
        if not runtime_args.silent:
            print("rms = %s (max = %s); dc = %s" % (rms, max_rms, dc))

        return (data, pyaudio.paContinue)

    # Open the audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=False,
                    frames_per_buffer=FRAMES_PER_BUFFFER,
                    stream_callback=callback)

    # Exit when user tells us to
    input("-" * 5 + " hit enter anytime to exit " + "-" * 5)

    # Clean up the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Clean up the Raspberry Pi GPIO
    if not runtime_args.test_pyaudio:
        pwm.stop()
        GPIO.cleanup()


def pulse_LED(repititions, pin_number, silent=False):
    """Pulse an LED connected to a RPi a few times.

    Args:
        repititions: An integer number of times an LED will be pulsed.
        pin_number: An integer specifying which GPIO pin will be used on
            the Raspberry Pi.
        silent: A boolean determining whether to supress output.
    """
    # Setup the GPIO pin
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_number, GPIO.OUT)

    # And use pulse width modulation
    pwm = GPIO.PWM(pin_number, 100) # pin number, frequency
    pwm.start(0)

    # Pulse
    for repitition in range(repititions):
        for dc in range(101):
            if not silent:
                print("dc = %s" % dc)

            pwm.ChangeDutyCycle(dc)
            time.sleep(DC_CHANGE_DELAY)
        for dc in range(100, -1, -1):
            if not silent:
                print("dc = %s" % dc)

            pwm.ChangeDutyCycle(dc)
            time.sleep(DC_CHANGE_DELAY)

    # Cleanup the Raspberry Pi GPIO
    pwm.stop()
    GPIO.cleanup()


def parse_runtime_args():
    """Parse runtime args using argparse.

    Returns:
        An object of type 'argparse.Namespace' containing the runtime
        arguments as attributes. See argparse documentation for more
        details.
    """
    parser = argparse.ArgumentParser(
            prog=NAME,
            description="%(prog)s - " + DESCRIPTION,)
    parser.add_argument(
            "-p", "--pin-number",
            type=int,
            default=12,
            help="which GPIO pin to use",)
    parser.add_argument(
            "-s", "--silent",
            help="don't output any information",
            action="store_true")
    parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s " + VERSION)
    test_option = parser.add_mutually_exclusive_group()
    test_option.add_argument(
            "--test-led",
            help="pulse the LED a few times",
            action="store_true")
    test_option.add_argument(
            "--test-pyaudio",
            help="analyze audio but don't use RPi GPIO pins",
            action="store_true")

    return parser.parse_args()


if __name__ == '__main__':
    # Run the main script
    main()
