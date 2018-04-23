#!/usr/bin/python3
# -*- python -*-

import sys
sys.path += [ "/usr/share/unicsy/lib" ]

import subprocess
import time
import os
import signal
import hardware

class MediaPlayer:
    def __init__(m):
        m.player = 0
        if False:
            m.audio = "/my/tui/ofone/audio/"
            m.play_cmd = [ 'mplayer' ]
        else:
            m.audio = "/usr/share/sounds/linphone/rings/"
            m.play_cmd = [ 'aplay' ]
            if hardware.hw.d4:
                m.play_cmd += [ '-D', 'plughw:CARD=Audio,DEV=0' ]

    def playback_finished(m):
        if not m.player:
            return 1
        if m.player.poll() is None:
            return 0
        return 1

    def mediaPlay(m, file):
        if not m.playback_finished():
            m.player.send_signal(signal.SIGTERM)
        m.player = subprocess.Popen(m.play_cmd + [ file ], stdin=subprocess.PIPE)

    def mediaPlayPause(m):
        if m.player:
            m.player.send_signal(signal.SIGSTOP)

class NotifyInterface(MediaPlayer):
    def sms(m, event):
        print("Incoming SMS")
        #m.mediaPlay(m.audio+"message.mp3")
        hardware.hw.audio.mixer_ringing()
        m.mediaPlay(m.audio+"orig.wav")

    def call_incoming(m, number):
        print("Incoming call")
        #m.mediaPlay(m.audio+"ringtone.mp3")
        hardware.hw.audio.mixer_ringing()
        m.mediaPlay(m.audio+"orig.wav")

    def end_incoming(m, reason):
        print("Incoming call no longer")
        m.mediaPlayPause()

    def call_starts(m):
        hardware.hw.audio.mixer_call()

    def call_ends(m):
        hardware.hw.audio.mixer_ringing()

if __name__ == "__main__":
    m = MediaPlayer()
    m.mediaPlay(m.audio+"ringtone.mp3")
    time.sleep(5)
    m.mediaPlayPause()

