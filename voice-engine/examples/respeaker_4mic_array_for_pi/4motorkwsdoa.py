"""
Search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.

for ReSpeaker 4 Mic Array for Raspberry Pi
"""

import sys
import time
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA

from gpiozero import Buzzer
from time import sleep

#signal output pins

RightPin = 16
FrontPin = 26
BackPin = 24
LeftPin = 23

Fmotor = Buzzer(FrontPin)
Lmotor = Buzzer(LeftPin)
Rmotor = Buzzer(RightPin)
Bmotor = Buzzer(BackPin)

def main():
    src = Source(rate=16000, channels=4)
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    kws = KWS(model='Cecilia.pmdl', sensitivity=0.5, verbose=True)
    doa = DOA(rate=16000)

    src.link(ch0)
    ch0.link(kws)
    src.link(doa)
    

    def on_detected(keyword):
        dir = doa.get_direction()
        print('detected {} at direction {}'.format(keyword, dir))

        if(315 <= dir or dir < 45):
            Fmotor.on()
            print("Front")
        elif(45 <= dir < 135):
            Rmotor.on()
            print("Right")
        elif(135 <= dir < 225):
            Bmotor.on()
            print("Back")
        elif(225 <= dir < 315):
            Lmotor.on()
            print("Left")
        time.sleep(1)
        Fmotor.off()
        Lmotor.off()
        Rmotor.off()
        Bmotor.off()
    kws.set_callback(on_detected)

    src.recursive_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()

    # wait a second to allow other threads to exit
    time.sleep(1)


if __name__ == '__main__':
    main()
