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

BOW_MOTOR = 17   #front
PORT_MOTOR = 24  #left
STARBOARD_MOTOR = 1
STERN_MOTOR = 25

buzzer_bow = Buzzer(BOW_MOTOR)
buzzer_port = Buzzer(PORT_MOTOR)
buzzer_star = Buzzer(STARBOARD_MOTOR)
buzzer_stern = Buzzer(STERN_MOTOR)

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
        if(dir < 45 or dir >= 315):
            buzzer_bow.on()
            sleep(1)
            buzzer_bow.off()
        elif(225 < dir <= 315):
            buzzer_port.on()
            sleep(1)
            buzzer_port.off()
        elif(135 < dir <= 225):
            buzzer_stern.on()
            sleep(1)
            buzzer_stern.off()
        elif(45 < dir <= 135):
            buzzer_star.on()
            sleep(1)
            buzzer_star.off()

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
