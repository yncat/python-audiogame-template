# -*- coding: utf-8 -*-
#BGT-ish Sound_lib wrapper
#Original author: Carter Temm
#Edited by Yukio Nozawa <personal@nyanchangames.com>
# License: GPL V2.0 (See copying.txt for details)

import math
import sound_lib
import sound_lib.output
import sound_lib.sample
from sound_lib import stream
o=sound_lib.output.Output()


class sound():
	def __init__(self):
		self.handle=None
		self.freq=44100
		self.paused=False

	def stream(self,filename=""):
		if self.handle:
			self.close()
#end close previous
		self.handle =stream.FileStream(file=filename)
		self.freq=self.handle.get_frequency()

	def load(self,sample=None):
		if self.handle:
			self.close()
#end close previous
		self.handle =sound_lib.sample.SampleBasedChannel(sample)
		self.freq=self.handle.get_frequency()

	def play(self,pan=0,vol=0,pitch=100):
		self.handle.looping=False
		self.handle.play()
		return self

	def setPaused(self,p):
		if self.paused==p: return
		if not self.playing and p: return
		self.paused=p
		if p:
			self.handle.pause()
		else:
			self.handle.play()
		#end pause or unpause
	#end setPaused

	def play_looped(self):
		self.handle.looping=True
		self.handle.play()

	def stop(self):
		if self.handle and self.handle.is_playing:
			self.handle.stop()
			self.handle.set_position(0)

	def fadeout(self, fadetime):
		"""The faded sound might be kept playing internally. Make sure that you call stop() before fading in or playing again. Fading will be performed by BASS's internal thread, so playing this instance after calling fadeout() may sound strangely."""
		if self.handle and self.handle.is_playing:
			self.handle.slide_attribute("volume",0,fadetime)

	@property
	def volume(self):
		if not self.handle:
			return False
		return round(math.log10(self.handle.volume)*20)
	@volume.setter
	def volume(self,value):
		if not self.handle:
			return False
		self.handle.set_volume(10**(float(value)/20))

	@property
	def pitch(self):
		if not self.handle:
			return False
		return (self.handle.get_frequency()/self.freq)*100

	@pitch.setter
	def pitch(self, value):
		if not self.handle:
			return False
		self.handle.set_frequency((float(value)/100)*self.freq)

	@property
	def pan(self):
		if not self.handle:
			return False
		return self.handle.get_pan()*100

	@pan.setter
	def pan(self, value):
		if not self.handle:
			return False
		self.handle.set_pan(float(value)/100)

	@property
	def playing(self):
		if self.handle is None:
			return False
		try:
			s=self.handle.is_playing
		except BassError:
			return False
		#end try
		return s

	def close(self):
		if self.handle:
			self.handle.free()

class oneShotInstance(object):
	def __init__(self):
		self.sample=None
		self.channel=None

	def play(self,path,pan,vol,pitch):
		self.sample=sound_lib.sample.Sample(path)
		self.channel=sound()
		self.channel.load(self.sample)
		self.channel.volume=vol
		self.channel.pan=pan
		self.channel.pitch=pitch
		self.channel.play()
		return self.channel

	def getPlayState(self):
		return self.channel.playing

#helper functions
def playOneShot(sample, pan=0, vol=0, pitch=100):
	if isinstance(sample,str):
		return _playOneShotFile(sample,pan,vol,pitch)
	#end file
	s=sound()
	s.load(sample)
	s.pan=pan
	s.volume=vol
	s.pitch=pitch
	s.play()
	return s

#end playOneShot
oneshots=[None]*100

def _playOneShotFile(path,pan,vol,pitch):
	global oneshots
	i=0
	found=-1
	for i in range(100):
		if oneshots[i] is None:
			oneshots[i]=oneShotInstance()
			found=i
			break
		#end oneShotInstance creation
		if oneshots[i].getPlayState() is False:
			found=i
			break
		#end blank
	#end for
	if found==-1:
		return None
	#end
	return oneshots[i].play(path,pan,vol,pitch)
