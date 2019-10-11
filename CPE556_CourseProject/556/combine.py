#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer."""

import argparse
import locale
import logging
import signal
import sys
import serial
import time
import binascii

from aiy.assistant.grpc import AssistantServiceClientWithLed
from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient
import aiy.voice.tts

def volume(string):
    value = int(string)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError('Volume must be in [0...100] range.')
    return value

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('turn on the light',
                'turn off the light',
                'blink the light',
                'repeat after you',
                'device on',
                'something else',
                'goodbye')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    parser.add_argument('--volume', type=volume, default=100)
    args = parser.parse_args()
    
    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    ser=serial.Serial('/dev/ttyUSB0',115200,timeout=1)
    ser.flushInput()
    with Board() as board:
        assistant = AssistantServiceClientWithLed(board=board,
                                                  volume_percentage=args.volume,
                                                  language_code=args.language)
        while True:
            logging.info('Press button to start conversation...')
            board.button.wait_for_press()
            logging.info('Conversation started!')
            to_say=('how may i help you')
            aiy.voice.tts.say(to_say)
            if hints:
                logging.info('Say something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Say something.')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if text is None:
                logging.info('You said nothing.')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()
            if 'turn on the light' in text:
                board.led.state = Led.ON
            elif 'turn off the light' in text:
                board.led.state = Led.OFF
            elif 'blink the light' in text:
                board.led.state = Led.BLINK
            elif 'repeat after you' in text:
                to_repeat = text.replace('repeat after you','', 1)
                aiy.voice.tts.say(to_repeat)
            elif 'turn on device' in text:
                print('Device turned on successfully')
                ser.write(str.encode('on'))
                ser.flushInput()
            elif 'goodbye' in text:
                ser.write(str.encode('off'))
                ser.flushInput()
                break
            elif 'something else' in text:
                assistant.conversation()

        ser.close()
if __name__ == '__main__':
    main()
