# -*- coding: utf-8 -*-
# Python audio game template
# Bootstrap
# Copyright (C) 2020 Yukio Nozawa <personal@nyanchangames.com>

import sys

import appMain
import globalVars

def main():
	app=appMain.Application()
	app.initialize()
	globalVars.app=app
	app.run()
#global schope
if __name__ == "__main__": main()