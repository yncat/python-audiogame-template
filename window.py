﻿# -*- coding: utf-8 -*-
# Python audio game template
# Basic window, timer, speech, menu handling
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>

from copy import copy
import ctypes
import platform
import pygame
import re
import subprocess
import wx
import sys
import accessible_output2.outputs.auto
import keyCodes


class SingletonWindow():
    """Just a pygame window wrapper. As the name implies, you mustn't create multiple singletonWindow's in your game. You should inherit this class and make your own app main class to make your code easy to read."""

    def __init__(self):
        self.wxInstance = wx.App()
        pygame.init()
        self.clock = pygame.time.Clock()

    def __del__(self):
        pygame.quit()

    def initialize(self, x, y, ttl):
        """
        Initializes the game window. Returns True on success or False for failure.

        :rtype: bool
        """
        self.screen = pygame.display.set_mode((x, y))
        pygame.display.set_caption(ttl)
        self.keys = [0] * 255
        self.previousKeys = [0] * 255
        self.speech = accessible_output2.outputs.auto.Auto()
        return True

    def frameUpdate(self):
        """
        A function that must be called once per frame. Calling this function will keep the 60fps speed.

        When user presses alt+f4 or the x icon, this function attempts to shut down the game by calling self.exit method. It is possible that the exit message is canceled by the onExit callback currently set.
        """
        self.clock.tick(60)
        self.screen.fill((255, 63, 10,))
        pygame.display.update()
        self.previousKeys = copy(self.keys)
        self.keys = pygame.key.get_pressed()
        if self.keyPressed(keyCodes.K_LCTRL):
            self.sayStop()
        if self.keyPressing(
                keyCodes.K_LALT) and self.keyPressed(
                keyCodes.K_F4):
            self.exit()
        for event in pygame.event.get():
            if event.type == keyCodes.QUIT:
                self.exit()
        # end event
    # end frameUpdate

    def keyPressed(self, key):
        """
        Retrieves if the specified key has changed to "pressed" from "not pressed" at the last frame. Doesn't cause key repeats.

        :rtype: bool
        """
        return self.keys[key] and not self.previousKeys[key]

    def keyPressing(self, key):
        """
        Retrieves if the specified key is being pressed. Key repeats at 60rp/sec.

        :rtype: bool
        """
        return self.keys[key]

    def wait(self, msec):
        """waits for a specified period of milliseconds while keeping the window looping. """
        t = Timer()
        while t.elapsed < msec:
            self.frameUpdate()
        # end loop
    # end wait

    def say(self, str, interrupt=False):
        """tts speech"""
        self.speech.speak(str, interrupt=interrupt)

    def sayStop(self):
        """stops tts speech"""
        self.speech.silence()

    def exit(self):
        """Attempt to exit the game. It is canceled if the onExit callback is set and it returned False."""
        if not self.onExit():
            return
        sys.exit()

    def onExit(self):
        """
        Override this method to define your own onExit code. It is automatically called from self.frameUpdate method when the game is being closed.

        You should return True when game can exit normally or False if you want to cancel the exit event.

        :rtype: bool
        """
        return True  # This is default

    def input(self, title, message):
        """Shows a text input dialog and returns what was input by the user. Returns None when canceled."""
        ret = None
        dlg = wx.TextEntryDialog(None, message, title)
        if dlg.ShowModal() == wx.ID_OK:
            ret = dlg.GetValue()
        dlg.Destroy()
        return ret
    # end input

    def dialog(self, title, message):
        """Shows messageBox on win and mac.

        :param title: Title.
        :type title: str
        :param message: Message body.
        :type message: str
        """
        if platform.system() == "Windows":
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000040)
        else:
            str = "display dialog \"%s\" with title \"%s\" with icon note buttons {\"OK\"}" % (
                re.sub(r'"\'', " ", message), re.sub(r'"\'', " ", title))  # escaping ' and " on mac
            subprocess.call("osascript -e '{}'".format(str), shell=True)
        # end dialog
# end class singletonWindow

    def folderSelect(self, text):
        """Shows the folder select dialog. Returns the selected folder or None for cancel.

        :param text: Explanation to show.
        :type text: str
        """
        dlg = wx.DirDialog(None, text, "")
        return dlg.GetPath() if dlg.ShowModal() == wx.ID_OK else None


class Timer:
    """A simple timer class like bgt."""

    def __init__(self):
        self.paused = False
        self.pausedElapsed = 0
        self.restart()

    def restart(self):
        """Restarts this timer."""
        self.pausedElapsed = 0
        self.startTick = pygame.time.get_ticks()

    @property
    def elapsed(self):
        """
        Returns the elapsed time in milliseconds.

        :rtype: int
        """
        if self.paused:
            return self.pausedElapsed
        return self.pausedElapsed + pygame.time.get_ticks() - self.startTick

    def setPaused(self, p):
        if p == self.paused:
            return
        if p:
            self.pausedElapsed = self.elapsed
        else:
            self.startTick = pygame.time.get_ticks()
        # end paused or unpaused
        self.paused = p
    # end setPaused

# end class Timer


STR_TO_KEY = {
    "A": keyCodes.K_a,
    "B": keyCodes.K_b,
    "C": keyCodes.K_c,
    "D": keyCodes.K_d,
    "E": keyCodes.K_e,
    "F": keyCodes.K_f,
    "G": keyCodes.K_g,
    "H": keyCodes.K_h,
    "I": keyCodes.K_i,
    "J": keyCodes.K_j,
    "K": keyCodes.K_k,
    "L": keyCodes.K_l,
    "M": keyCodes.K_m,
    "N": keyCodes.K_n,
    "O": keyCodes.K_o,
    "P": keyCodes.K_p,
    "Q": keyCodes.K_q,
    "R": keyCodes.K_r,
    "S": keyCodes.K_s,
    "T": keyCodes.K_t,
    "U": keyCodes.K_u,
    "V": keyCodes.K_v,
    "W": keyCodes.K_w,
    "X": keyCodes.K_x,
    "Y": keyCodes.K_y,
    "Z": keyCodes.K_z,
    "0": keyCodes.K_0,
    "1": keyCodes.K_1,
    "2": keyCodes.K_2,
    "3": keyCodes.K_3,
    "4": keyCodes.K_4,
    "5": keyCodes.K_5,
    "6": keyCodes.K_6,
    "7": keyCodes.K_7,
    "8": keyCodes.K_8,
    "9": keyCodes.K_9
}


class Menu:
    """A simple nonblocking menu class."""

    def __init__(self):
        pass

    def initialize(
            self,
            wnd,
            ttl="no title",
            items=None,
            cursorSound=None,
            enterSound=None,
            cancelSound=None,
            unavailableSound=None):
        """
        Initializes the menu with window instance, title and initial menu items. Requires a singletonWindow instance for this menu to work. Menu items should be a sequence of strings (not an array). the "#" character is used as the menu delimitor.

        :param wnd: Window to which this menu is bound.
        :type wnd: SingletonWindow
        :param ttl: Menu title.
        :type ttl: str
        :param items: Default items.
        :type items: list
        :param CursorSound: Sample instance played when user cycles through the menu items.
        :type enterSound: sound_lib.sample
        :param enterSound: Sample instance played when user presses enter on a menu item.
        :type enterSound: sound_lib.sample
        :param cancelSound: Sample instance played when user cancels the menu.
        :type cancelSound: sound_lib.sample
        :param unavailableSound: Sample instance played when user focuses on "unavailable" marked item.
        :type unavailableSound: sound_lib.sample
        """
        self.wnd = wnd
        self.title = ttl
        self.items = []
        self.is_available = []
        self.shortcuts = []
        if items:
            self.append(items)
        self.cursor = 0
        self.cursorSound = cursorSound
        self.enterSound = enterSound
        self.cancelSound = cancelSound
        self.unavailableSound = unavailableSound
        self.holdTimer = Timer()
        self.lastHold = 0

    def append(self, lst, shortcut=True, available=True):
        """Adds one or multiple menu items. By setting shortcut false, you can skip parsing for shortcut key registration."""
        if isinstance(lst, str):
            self.items.append(self.append_internal(lst, shortcut))
            self.is_available.append(available)
            return
        # end single append
        for elem in lst:
            self.items.append(self.append_internal(elem, shortcut))
            self.is_available.append(available)

    def insert(self, index, item):
        """Inserts an item at the specified position.

        :param index: Index to add.
        :type index: int
        :item: Item to add.
        :type item: str
        """
        self.items.insert(index, self.append_internal(item))

    def append_internal(self, elem, processShortcut=True):
        """Parses and makes a single item tuple. Called from append.

        :param elem: Element to add.
        """
        if not processShortcut:
            return (elem, None, None)
        shortcut, shortcut_str = self.parseShortcut(elem)
        if shortcut:
            elem = elem[0:len(elem) - 2]
            self.shortcuts.append((shortcut, len(self.items)))
        # end if shortcut registration
        return (elem, shortcut_str, shortcut)

    def parseShortcut(self, elem):
        """Parses the menu item string and returns shortcut keycode and string if detected. Otherwise, set both as None.
        :param elem: Element to parse.
        """
        shortcut = None
        shortcut_str = None
        l = len(elem)
        if l <= 3:
            return None, None
        last = elem[l - 2:l].upper()
        if last[0] == "&":
            try:
                cmd = STR_TO_KEY[last[1]]
            except KeyError:
                pass
            else:
                shortcut = cmd
                shortcut_str = last[1]
            # end else
        # end if shortcut input exists
        return shortcut, shortcut_str

    def delete(self, index):
        """Deletes the item at the specified index.

        :param index: index to delete.
        :type index: int
        """
        for elem in self.shortcuts[:]:
            if elem[1] == index:
                self.shortcuts.remove(elem)
        self.items.pop(index)

    def modify(self, index, new):
        """Modifies the existing menu item.

        :param index: Index to modify.
        :type index: int
        :param new: New menu item
        :type new: str
        """
        self.delete(index)
        self.insert(index, new)

    def setAvailability(self, index, avail):
        if index >= len(self.items):
            return
        self.is_available[index] = avail

    def open(self):
        """Starts the menu. You should call frameUpdate() to keep the menu operate after this. """
        if len(self.items) == 0:
            return
        self.wnd.say("%s, %s" % (self.title, self.getReadStr()))

    def frameUpdate(self):
        """The frame updating function for this menu. You should call your window's frameUpdate prior to call this function. Returns None for no action, -1 for cancellation and 0-based index for being selected. """
        up = self.wnd.keyPressing(keyCodes.K_UP)
        dn = self.wnd.keyPressing(keyCodes.K_DOWN)
        processArrows = False
        if not up and not dn:
            self.lastHold = 0
        if self.lastHold == 0:
            processArrows = True
        if self.lastHold == 1 and self.holdTimer.elapsed >= 600:
            processArrows = True
        # end 600 ms hold
        if self.lastHold == 2 and self.holdTimer.elapsed >= 50:
            processArrows = True
        # end 50 ms hold
        if processArrows:
            if up:
                self.moveTo(self.cursor - 1)
            if dn:
                self.moveTo(self.cursor + 1)
        # end arrow keys
        if self.wnd.keyPressed(keyCodes.K_HOME) and self.cursor != 0:
            self.moveTo(0)
        if self.wnd.keyPressed(
                keyCodes.K_END) and self.cursor != len(
                self.items):
            self.moveTo(len(self.items) - 1)
        if self.wnd.keyPressed(keyCodes.K_PAGEUP):
            n = int(len(self.items) / 20)
            if n > 0:
                self.moveTo(self.cursor - n)
        # end pageup
        if self.wnd.keyPressed(keyCodes.K_PAGEDOWN):
            n = int(len(self.items) / 20)
            if n > 0:
                self.moveTo(self.cursor + n)
        # end pagedown
        if self.wnd.keyPressed(keyCodes.K_SPACE):
            self.moveTo(self.cursor)
        if self.wnd.keyPressed(keyCodes.K_ESCAPE):
            self.cancel()
            return -1
        # end cancel
        if self.wnd.keyPressed(keyCodes.K_RETURN):
            self.enter()
            return self.cursor
        # end enter
        if len(self.shortcuts) > 0:
            for command in STR_TO_KEY.values():
                if self.wnd.keyPressed(command):
                    return self.processShortcut(command)
            # end shortcut
        # end at least one shortcut is active
        return None
    # end frameUpdate

    def processShortcut(self, code):
        """Search for the shortcut actions that is associated with the given command. Returns the index if one item is matched and instantly selected, otherwise None. This method may move focus or trigger the enter event as the result of searching.

        :param code: key code.
        :type code: int
        """
        matched = []
        for elem in self.shortcuts:
            if elem[0] == code:
                matched.append(elem)
        # end for
        if len(matched) == 0:
            return
        if len(matched) == 1:
            self.cursor = matched[0][1]
            self.enter()
            return self.cursor
        # end instant selection
        i = self.cursor
        found = False
        while i < len(self.items) - 1:
            i += 1
            if self.items[i][2] == code:
                found = True
                break
            # end if
        # end while
        if found:
            self.moveTo(i)
            return None
        # end if found at the lower column
        # Research from the top
        i = -1
        while i < len(self.items) - 1:
            i += 1
            if self.items[i][2] == code:
                found = True
                break
        if found:
            self.moveTo(i)
            return None
        # end research
    # end processShortcut

    def cancel(self):
        """Internal function which is triggered when canceling the menu. """
        if self.cancelSound is not None:
            playOneShot(self.cancelSound)

    def enter(self):
        """Internal function which is triggered when selecting an option. """
        if self.enterSound is not None:
            playOneShot(self.enterSound)

    def getCursorPos(self):
        """Returns the current cursor position. """
        return self.cursor

    def getString(self, index):
        """Retrieves the menu item string at the specified index. Returns empty string when out of bounds.

        :param index: Index.
        :rtype: str
        """
        if index < 0 or index >= len(self.items):
            return ""
        return self.items[index][0]

    def moveTo(self, c):
        """Moves the menu cursor to the specified position and reads out the cursor. It also sets the lastHold status, which triggers key repeats. I decided not to use pygame key repeat functions. """
        if self.lastHold < 2:
            self.lastHold += 1
        if c < 0 or c > len(self.items) - 1:
            return
        self.holdTimer.restart()
        if self.cursorSound is not None:
            playOneShot(self.cursorSound)
        if not self.is_available[c] and self.unavailableSound is not None:
            playOneShot(self.unavailableSound)
        self.cursor = c
        self.wnd.say(self.getReadStr())
    # end moveTo

    def getReadStr(self):
        """Returns a string which should be used as readout string for the current cursor.

        :rtype: str
        """
        s = self.items[self.cursor][0]
        if self.items[self.cursor][1] is not None:
            s += ", " + self.items[self.cursor][1]
        return s

    def isLast(self, index):
        """Retrieves if the given index is the last item of the menu. This is particularly useful when you want to bind the last action to exit or close.

        :param index: index.
        :type index: int
        :rtype: bool
        """
        return self.cursor == len(self.items) - 1

# end class menu
