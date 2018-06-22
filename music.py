# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 15:20:47 2018

@author: Sandesh
"""


import os
import vlc
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
url='https://youtu.be/iSUT1jJVTu0'
emotion=0
ip="http://codeglobal.in/wp-content/uploads/2018/06/songs/list.txt"

#r=requests.get(ip)

import requests
from random import shuffle
import re
import speech_recognition as sr

r=sr.Recognizer()
m = sr.Microphone()
def record_audio():
  print("A moment of silence, please...")
  with m as source:
    r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
  print("speak: ")
  with m as source: audio = r.listen(source,timeout=3)
  print("Got it! Now to recognize it...")
  value = r.recognize_google(audio)
  print(value)
  return value
 
class play_song:
    def __init__(self,ip):
        self.ip=ip
        self.player=self.set_player()
        
    def set_player(self):
      u=requests.get(self.ip)
      new_list=[]
      source=self.ip[:-9]    
      instance=vlc.Instance()
      MediaList = instance.media_list_new()
      for l in u.iter_lines():
        l=l.decode('utf-8')
        #MediaList.add_media(instance.media_new(source+'/'+re.findall('[0-9A-Za-z].mp3',l)[0]))
        new_list.append(re.match('(.*?).mp3',l).group())
      shuffle(new_list)
      for l in new_list:
          MediaList.add_media(instance.media_new(source+'/'+l))

      p=instance.media_list_player_new()
      p.set_media_list(MediaList)
      return p
    def play_next(self):
        if(self.player.next()!=0):
            self.player.stop()
            self.player=self.set_player()
            self.player.next()
        
    def stop(self):
        self.player.stop()
    def pause(self):
        self.player.pause()
    def play(self):
        self.player.play()

'''if __name__=='__main__':
    value=record_audio()
    if(value=='play song'):
        p=play_song(ip)
        p.play_next()
    '''
       