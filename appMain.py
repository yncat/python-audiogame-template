# -*- coding: utf-8 -*-
# Python audiogame template
# Application entry point
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
import constants
import globalVars
import logging
import glob
from logging import getLogger, FileHandler, Formatter
import os
import sound_lib.sample
import sound
import buildSettings
import keyCodes
import window

class Application(window.SingletonWindow):
	"""
	The game's main application class.

	Instantiate this class, call initialize method, then call run method to start the application. Other methods are internally used and should not be called from outside of the class.
	"""
	def __init__(self):
		super().__init__()

	def initialize(self):
		super().initialize(1200, 800, buildSettings.GAME_NAME+" ("+str(buildSettings.GAME_VERSION)+")")
		self.initLogger()
		self.sounds={}

	def initLogger(self):
		self.hLogHandler=FileHandler("debug.log", mode="w", encoding="UTF-8")
		self.hLogHandler.setLevel(logging.DEBUG)
		self.hLogFormatter=Formatter("%(name)s - %(levelname)s - %(message)s")
		self.hLogHandler.setFormatter(self.hLogFormatter)
		self.log=getLogger("app")
		self.log.setLevel(logging.DEBUG)
		self.log.addHandler(self.hLogHandler)
		self.log.info("Starting.")

	def run(self):
		self.playOneShot("fx/decide.ogg")
		while(True):
			self.frameUpdate()
			if self.keyPressed(keyCodes.K_RETURN): self.playOneShot("fx/decide.ogg")
			if self.keyPressed(keyCodes.K_ESCAPE): break
		#end main loop
	#end run

	def loadSoundFolder(self,path):
		"""
			Loads all sounds the specified folder and caches them in the memory. It doesn't search for subfolders.

			:param path: Path to load.
			:type path: str
		"""
		files=glob.glob("fx/"+path+"/*.ogg")
		self.log.info("loading sound folder: fx/%s (%d files)" % (path,len(files)))
		for elem in files:
			self.sounds[path+"/"+os.path.basename(elem)]=sound_lib.sample.Sample(elem)
	# end loadSounds

	def playOneShot(self,key,pan=0,vol=0,pitch=100,wait=False):
		"""
			Plays a sound as one shot.

			:param key: Sound to play.
			:type key: sound.Sample or str
			:param pan: Pan.
			:type pan: float
			:param volume: Volume.
			:type volume: float
			:param pitch: Pitch.
			:type pitch: float.
			:param wait: Wait until playing finishes? (default False)
			:type wait: bool
		"""
		s=sound.playOneShot(key,pan,vol,pitch)
		if wait:
			while(s.playing is True):
				self.frameUpdate()
			#end while playing
		#end wait is True
	#end playOneShot

	def message(self,msg):
		"""
		Shows a simple message dialog. This method is blocking; it won't return until user dismisses the dialog. While this method is blocking, onExit still works as expected.

		:param msg: Message to show.
		:type msg: str
		"""
		self.say(msg)
		while(True):
			self.frameUpdate()
			if True in (self.keyPressed(keyCodes.K_LEFT), self.keyPressed(keyCodes.K_RIGHT), self.keyPressed(keyCodes.K_UP), self.keyPressed(keyCodes.K_DOWN)): self.say(msg)#Message repeat
			if self.keyPressed(keyCodes.K_RETURN): break
		#end frame update
		sound.playOneShot(self.sounds["UI/decide.ogg"])
	#end message
