#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/kujan/NGU-scripts/blob/871c25249a3331a5fa3afeca7acbd880222a0dbf/classes/window.py#L26C35-L26C35 is that check correct? how about windows 11?
# https://github.com/kujan/NGU-scripts/blob/871c25249a3331a5fa3afeca7acbd880222a0dbf/classes/inputs.py#L29 The argument button should be an enum
# https://github.com/kujan/NGU-scripts/blob/871c25249a3331a5fa3afeca7acbd880222a0dbf/classes/inputs.py the type hints are nice but the way that they are written?!
# https://github.com/kujan/NGU-scripts/blob/871c25249a3331a5fa3afeca7acbd880222a0dbf/classes/inputs.py#L115C33-L115C33 This is NOT what the user intended. Better to fail
# https://github.com/kujan/NGU-scripts/blob/871c25249a3331a5fa3afeca7acbd880222a0dbf/classes/inputs.py#L124C14-L124C14 That cant be correct... Without the up event, the game thinks the user is still holding those buttons down
# https://github.com/kujan/NGU-scripts/blob/871c25249a3331a5fa3afeca7acbd880222a0dbf/classes/inputs.py#L349 WTF, this is a simple s.replace(' ', '')
"""
Module for handling keyboard presses and mouse movement and mouse clicks on Windows.
Use the module https://github.com/boppreh/keyboard whenever you can.
However, there is a bug in that module, see
https://github.com/boppreh/keyboard/blob/master/keyboard/_winkeyboard.py#L11
which is:
"- No way to specify if user wants a keypad key or not in `map_char`"

This module can handle numpad just fine

This module can also send key preses as window messages via SendMessage.
If you use the SendMessage, then the application do NOT need to have focus
"""

__version__ = 230704153633
__author__ = "Harding"
__description__ = __doc__
__copyright__ = "Copyright 2023"
__credits__ = ["https://github.com/neal365/python/blob/master/mouseClick.py",
               "https://github.com/kujan/NGU-scripts/blob/master/classes/inputs.py"]
__license__ = "GPL"
__maintainer__ = "Harding"
__email__ = "not.at.the.moment@example.com"
__status__ = "Development"


import time
import re
import ctypes
from ctypes import wintypes
from typing import Tuple, List, Union, Set, Optional
import logging as _logging
_g_logger = _logging.getLogger(__name__)
# _g_logger.setLevel(_logging.DEBUG) # This is the level that is actually used. In production, set this to logging.INFO
_g_logger.setLevel(_logging.INFO)
_console_handler = _logging.StreamHandler()
_console_handler.setLevel(_logging.DEBUG)
_console_handler.setFormatter(_logging.Formatter('[%(asctime)s] %(levelname)s: %(module)s.%(funcName)s:%(lineno)d --> %(message)s'))
if _g_logger.handlers:
    _g_logger.removeHandler(_g_logger.handlers[0]) # When you importlib.reload() a module, we need to clear out the old _g_logger
_g_logger.addHandler(_console_handler)
import win32gui as _win32gui
import win32con as _win32con
import win32api as _win32api
from typeguard import typechecked

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0 # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyexw
MAPVK_VSC_TO_VK = 1
MAPVK_VK_TO_CHAR = 2
MAPVK_VSC_TO_VK_EX = 3
MAPVK_VK_TO_VSC_EX = 4

VK_LBUTTON = 0x01 # Left mouse button
VK_RBUTTON = 0x02 # Right mouse button
VK_MBUTTON = 0x04 # Middle mouse button (three-button mouse)
VK_XBUTTON1 = 0x05 # X1 mouse button (Mouse 4)
VK_XBUTTON2 = 0x06 # X2 mouse button (Mouse 5)
VK_BACK = 0x08 # BACKSPACE key
VK_TAB  = 0x09
VK_RETURN = 0x0D
VK_ENTER = 0x0D # VK_RETURN and VK_ENTER are the same key
VK_SHIFT = 0x10 # SHIFT key
VK_CONTROL = 0x11 # CONTROL key
VK_MENU = 0x12 # ALT key
VK_ALT = 0x12 # ALT key
VK_CAPSLOCK = 0x14
VK_ESCAPE = 0x1B
VK_ESC = 0x1B
VK_SPACE = 0x20
VK_PAGE_UP = 0x21
VK_PAGEUP = 0x21
VK_PAGE_DOWN = 0x22
VK_PAGEDOWN = 0x22
VK_END = 0x23
VK_HOME = 0x24
VK_LEFT = 0x25 # LEFT arrow
VK_UP = 0x26 # UP arrow
VK_RIGHT = 0x27 # RIGHT arrow
VK_DOWN = 0x28 # DOWN arrow
VK_DELETE = 0x2E
VK_0 = 0x30
VK_1 = 0x31
VK_2 = 0x32
VK_3 = 0x33
VK_4 = 0x34
VK_5 = 0x35
VK_6 = 0x36
VK_7 = 0x37
VK_8 = 0x38
VK_9 = 0x39
VK_A = 0x41 # A key
VK_B = 0x42 # B key
VK_C = 0x43 # C key
VK_D = 0x44 # D key
VK_E = 0x45 # E key
VK_F = 0x46 # F key
VK_G = 0x47 # G key
VK_H = 0x48 # H key
VK_I = 0x49 # I key
VK_J = 0x4A # J key
VK_K = 0x4B # K key
VK_L = 0x4C # L key
VK_M = 0x4D # M key
VK_N = 0x4E # N key
VK_O = 0x4F # O key
VK_P = 0x50 # P key
VK_Q = 0x51 # Q key
VK_R = 0x52 # R key
VK_S = 0x53 # S key
VK_T = 0x54 # T key
VK_U = 0x55 # U key
VK_V = 0x56 # V key
VK_W = 0x57 # W key
VK_X = 0x58 # X key
VK_Y = 0x59 # Y key
VK_Z = 0x5A # Z key
VK_LWINDOWS = 0x5B # Left windows button
VK_RWINDOWS = 0x5C # Right windows button
VK_SLEEP = 0x5F
VK_NUMPAD0 = 0x60
VK_NUMPAD1 = 0x61
VK_NUMPAD2 = 0x62
VK_NUMPAD3 = 0x63
VK_NUMPAD4 = 0x64
VK_NUMPAD5 = 0x65
VK_NUMPAD6 = 0x66
VK_NUMPAD7 = 0x67
VK_NUMPAD8 = 0x68
VK_NUMPAD9 = 0x69
VK_MULTIPLY = 0x6A # Multiply key on the numpad
VK_ADD = 0x6B # Add key on the numpad
VK_SEPARATOR = 0x6C # Separator key on numpad
VK_SUBTRACT = 0x6D # Subtract key
VK_DECIMAL = 0x6E # Decimal key
VK_DIVIDE = 0x6F # Divide key
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72
VK_F4 = 0x73
VK_F5 = 0x74
VK_F6 = 0x75
VK_F7 = 0x76
VK_F8 = 0x77
VK_F9 = 0x78
VK_F10 = 0x79
VK_F11 = 0x7A
VK_F12 = 0x7B
VK_F13 = 0x7C # From F13 and up, I had some problems with the programs not accepting them
VK_F14 = 0x7D
VK_F15 = 0x7E
VK_F16 = 0x7F
VK_F17 = 0x80
VK_F18 = 0x81
VK_F19 = 0x82
VK_F20 = 0x83
VK_F21 = 0x84
VK_F22 = 0x85
VK_F23 = 0x86
VK_F24 = 0x87
VK_LSHIFT = 0xA0 # Left SHIFT key
VK_LEFT_SHIFT = 0xA0 # Left SHIFT key
VK_RSHIFT = 0xA1 # Right SHIFT key
VK_RIGHT_SHIFT = 0xA1 # Right SHIFT key
VK_LCONTROL = 0xA2 # Left CONTROL key
VK_LEFT_CONTROL = 0xA2 # Left CONTROL key
VK_RCONTROL = 0xA3 # Right CONTROL key
VK_RIGHT_CONTROL = 0xA3 # Right CONTROL key
VK_LMENU = 0xA4 # Left ALT key
VK_LEFT_ALT = 0xA4 # Left ALT key
VK_RMENU = 0xA5 # Right ALT key
VK_RIGHT_ALT = 0xA5 # Right ALT key
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP = 0xB2
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_START_MAIL = 0xB4

# https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
g_virtual_keys = {k[3:].lower(): getattr(_win32con, k) for k in dir(_win32con) if k.startswith('VK_')} # As base, we use the keys that win32con supports
_g_virtual_keys_harding_keyboard = {k[3:].lower(): getattr(__import__(__name__), k) for k in dir(__import__(__name__)) if k.startswith('VK_')}
for key, value in _g_virtual_keys_harding_keyboard.items(): # Then we add our own virtual key mappings
    g_virtual_keys[key] = value
del _g_virtual_keys_harding_keyboard # Not used anymore
g_virtual_keys[' '] = VK_SPACE

HWND = int # Used as typedef for Windows API that takes a HWND
virtual_key_type = Union[str, int]
key_type = Union[virtual_key_type, List[str]]
mouse_position_type = Tuple[int, int] # (0,0) is the top left corner

# C struct definitions
wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

def create_LPARAM_KeyUpDown(arg_virtual_key: virtual_key_type,
                            RepeatCount: int,
                            TransitionState: bool,
                            PreviousKeyState: bool,
                            ContextCode: bool
                            ) -> int:
    ''' Taken from https://stackoverflow.com/questions/54638741/how-is-the-lparam-of-postmessage-constructed '''
    scancode = user32.MapVirtualKeyExW(virtual_key(arg_virtual_key), MAPVK_VK_TO_VSC, 0)
    _unknown_but_seems_to_work_as_zero = 0 # TODO: This needs to be fixed
    return TransitionState << 31 | PreviousKeyState << 30 | ContextCode << 29 | _unknown_but_seems_to_work_as_zero << 24 | scancode << 16 | RepeatCount

def create_LPARAM_KeyDown(arg_virtual_key: virtual_key_type, RepeatCount: int = 1) -> int:
    return create_LPARAM_KeyUpDown(arg_virtual_key, RepeatCount, TransitionState=False, PreviousKeyState=RepeatCount > 1, ContextCode=False)

def create_LPARAM_KeyUp(arg_virtual_key: virtual_key_type) -> int:
    return create_LPARAM_KeyUpDown(arg_virtual_key, RepeatCount=1, TransitionState=True, PreviousKeyState=True, ContextCode=False)

def _list_from_str(arg_str: Union[str, List, Set, Tuple, None],
                  arg_re_splitter: str = ' |,|;|:|[+]|[-]|[|]|[\n]|[\r]'
                  ) -> List[str]:
    ''' Take a str and try to convert into a list of str in a smart way.
    Raise ValueError if something breaks. '''

    if arg_str is None:
        return []
    if isinstance(arg_str, list):
        res = arg_str
    elif isinstance(arg_str, (set, tuple)):
        res = list(arg_str)
    elif isinstance(arg_str, str):
        res = re.split(arg_re_splitter, arg_str)
    else:
        print(f"ERROR! arg_str is of type: {type(arg_str)} which I cannot handle!")
        raise ValueError('Invalid argument, arg_str is is incorrect')

    res = [x for x in res if x]
    return res

# Public functions ------------------------------------------------------------------------------------------------------------------
@typechecked
def mouse_get_position() -> Optional[mouse_position_type]:
    ''' Returns the mouse position as a tuple (x, y) where (0, 0) is the top left of the screen

    Can throw pywintypes.error: (5, 'GetCursorPos', 'Access is denied.')
    From my limited tests, this can happen if the system has been put into screensaver mode or if the secure desktop is showing.

    '''
    res = None
    try:
        res  = _win32gui.GetCursorPos()
    except exc:
        # If the screen saver is running, the exception can be thrown
        _g_logger.error('_win32gui.GetCursorPos got an exception: {exc}')

    return res

@typechecked
def find_window(arg_class_name: Optional[str] = None, arg_title: Optional[str] = None) -> HWND:
    ''' Get the HWND to the window matching the class name or title.
        For more info see: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-findwindowa '''
    return _win32gui.FindWindow(arg_class_name, arg_title) # TODO: Can this also throw exception as win32gui.GetCursorPos() ?

@typechecked
def is_window(arg_hwnd: HWND) -> bool:
    ''' Determines whether the specified window handle identifies an existing window.
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-iswindow '''

    return _win32gui.IsWindow(arg_hwnd) == 1

@typechecked
def window_from_point(arg_pos: mouse_position_type) -> HWND:
    ''' Get the HWND from the given position '''
    return _win32gui.WindowFromPoint(arg_pos) # TODO: Can this also throw exception as win32gui.GetCursorPos() ?

@typechecked
def virtual_key(arg_virtual_key: virtual_key_type, arg_debug: bool = False) -> int:
    ''' Try to convert whatever comes in to a virtual key code '''
    if isinstance(arg_virtual_key, str):
        arg_virtual_key = g_virtual_keys[arg_virtual_key.lower()]
    if not isinstance(arg_virtual_key, int):
        _g_logger.critical(f"arg_virtual_key is not an int and not a str. It is of type: {type(arg_virtual_key)}")
        raise ValueError('Invalid argument, arg_virtual_key is not int nor str')
    if arg_debug:
        _g_logger.debug(f"returned 0x{arg_virtual_key:x}")
    return arg_virtual_key

@typechecked
def key_down_SendInput(arg_virtual_key_code: virtual_key_type, arg_debug: bool = False):
    ''' Send the event that press down a key. You need to manually call key_up_SendInput() to release the key '''
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=virtual_key(arg_virtual_key_code)))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

@typechecked
def key_up_SendInput(arg_virtual_key_code: virtual_key_type):
    ''' Send the event that release a key. You need to manually call key_down_SendInput() before to press down the key '''
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=virtual_key(arg_virtual_key_code), dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

@typechecked
def key_hold_SendInput(arg_virtual_key_code: virtual_key_type, arg_hold_down_for_in_seconds: float = 0.050):
    ''' Press down a key, wait 'arg_hold_down_for_in_seconds' seconds then release the key. If no 'arg_hold_down_for_in_seconds' is given, holds down for 50 ms '''
    key_down_SendInput(arg_virtual_key_code)
    time.sleep(arg_hold_down_for_in_seconds)
    key_up_SendInput(arg_virtual_key_code)

# These functions do NOT need the application to have focus ---------------------------------------------------------------------------------
@typechecked
def mouse_SendMessage(arg_hwnd: HWND,
                      arg_pos: mouse_position_type,
                      arg_direction_is_down: bool = True,
                      arg_mouse_button_is_left: bool = True,
                      arg_move_mouse: bool = True,
                      arg_debug: bool = False):
    ''' Send a mouse message. Default is left mouse button. '''
    _MK = _win32con.MK_LBUTTON if arg_mouse_button_is_left else _win32con.MK_RBUTTON
    _WM = _win32con.WM_LBUTTONDOWN if arg_mouse_button_is_left else _win32con.WM_RBUTTONDOWN

    if not arg_direction_is_down:
        _WM = _win32con.WM_LBUTTONUP if arg_mouse_button_is_left else _win32con.WM_RBUTTONUP

    client_pos = _win32gui.ScreenToClient(arg_hwnd, arg_pos) # TODO: Will this be a problem if the window is not placed at (0,0) ?
    _lparam = _win32api.MAKELONG(client_pos[0], client_pos[1])
    _win32gui.SendMessage(arg_hwnd, _win32con.WM_ACTIVATE, _win32con.WA_ACTIVE, 0) # TODO: Is it a problem that I send many WM_ACTIVATE?
    if arg_move_mouse: # Some programs don't work well if we don't have the mouse in the correct position
        _win32api.SendMessage(arg_hwnd, _win32con.WM_MOUSEMOVE, None, _lparam)
    # TODO: Kujan have checks for if the user holds down a modifier key like CTRL and waits until that is released.
    # TODO: Thats a good idea I think but I have to meditate on it further
    _win32api.SendMessage(arg_hwnd, _WM, _MK, _lparam) # TODO: mypy say: 'error: Argument 3 to "SendMessage" has incompatible type "int"; expected "Optional[str]"  [arg-type]' but thats gotta be wrong?

@typechecked
def key_down_SendMessage(arg_hwnd: HWND,
                         arg_virtual_key: virtual_key_type,
                         arg_debug: bool = False):
    ''' Send the event that press down a key. You need to manually call key_up_SendMessage() to release the key '''

    _vk = virtual_key(arg_virtual_key, arg_debug=arg_debug)
    if arg_debug:
        _g_logger.debug(f"Got arg_virtual_key: {arg_virtual_key} with type: {type(arg_virtual_key)} --> virtual_key(): 0x{_vk:x}")
    _win32api.SendMessage(arg_hwnd, _win32con.WM_KEYDOWN, _vk, create_LPARAM_KeyDown(_vk))

@typechecked
def key_up_SendMessage(arg_hwnd: HWND,
                       arg_virtual_key: virtual_key_type,
                       arg_debug: bool = False):
    ''' Send the event the release a key. You need to manually call key_down_SendMessage() before to press down the key '''
    _vk = virtual_key(arg_virtual_key, arg_debug=arg_debug)
    if arg_debug:
        _g_logger.debug(f"Got arg_virtual_key: {arg_virtual_key} with type: {type(arg_virtual_key)} --> virtual_key(): 0x{_vk:x}")
    _win32api.SendMessage(arg_hwnd, _win32con.WM_KEYUP, _vk, create_LPARAM_KeyUp(_vk))

@typechecked
def key_hold_SendMessage(arg_hwnd: HWND,
                         arg_virtual_key: Union[virtual_key_type, List[str]],
                         arg_hold_down_for_in_seconds: float = 0.050,
                         arg_debug: bool = False
                         ) -> bool:
    ''' Send the key messages KeyDown and then KeyUP via SendMessage. Can handle strings like 'control + w' to hold control and press w (close tab) '''
    _win32gui.SendMessage(arg_hwnd, _win32con.WM_ACTIVATE, _win32con.WA_ACTIVE, 0)

    if isinstance(arg_virtual_key, int):
        key_down_SendMessage(arg_hwnd=arg_hwnd, arg_virtual_key=arg_virtual_key, arg_debug=arg_debug)
        time.sleep(arg_hold_down_for_in_seconds)
        key_up_SendMessage(arg_hwnd=arg_hwnd, arg_virtual_key=arg_virtual_key, arg_debug=arg_debug)
    else:
        _keys = _list_from_str(arg_virtual_key) # This can handle strings like "control + S" --> hold down control and press S
        if not _keys:
            _g_logger.error("_keys is empty")
            return False
        _key = _keys[0].lower().strip()
        if len(_keys) == 1:
            # _g_logger.debug(f"Sending 1 key: {_key}")
            return key_hold_SendMessage(arg_hwnd=arg_hwnd, arg_virtual_key=virtual_key(_key, arg_debug=arg_debug), arg_hold_down_for_in_seconds=arg_hold_down_for_in_seconds)

        # This is when we have something like "control + w", then we hold down 'control' and pass the next part to the parser
        if arg_debug:
            _g_logger.debug(f"Holding down key: {_key}")
        key_down_SendMessage(arg_hwnd=arg_hwnd, arg_virtual_key=virtual_key(_key, arg_debug=arg_debug), arg_debug=arg_debug)
        key_hold_SendMessage(arg_hwnd=arg_hwnd, arg_virtual_key=_keys[1:], arg_hold_down_for_in_seconds=arg_hold_down_for_in_seconds, arg_debug=arg_debug)
        key_up_SendMessage(arg_hwnd=arg_hwnd, arg_virtual_key=virtual_key(_key, arg_debug=arg_debug), arg_debug=arg_debug)
        if arg_debug:
            _g_logger.debug(f"Releasing key: {_key}")
    return True

@typechecked
def key_type_message_SendMessage(arg_hwnd: HWND,
                                 arg_message: key_type,
                                 arg_seconds_between_keys: float = 0.050,
                                 arg_debug: bool = False
                                 ) -> bool:
    ''' Send a string of characters as a sequence of window messages '''
    res = True

    if isinstance(arg_message, int):
        return key_hold_SendMessage(arg_hwnd=arg_hwnd, arg_virtual_key=arg_message, arg_debug=arg_debug)

    for _key in arg_message:
        res = res and key_hold_SendMessage(arg_hwnd=arg_hwnd, arg_virtual_key=_key, arg_debug=arg_debug)
        time.sleep(arg_seconds_between_keys)
    return res

@typechecked
def mouse_left_down_SendMessage(arg_hwnd: HWND,
                                arg_pos: mouse_position_type,
                                arg_move_mouse: bool = True,
                                arg_debug: bool = False):
    mouse_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_direction_is_down=True, arg_mouse_button_is_left=True, arg_move_mouse=arg_move_mouse, arg_debug=arg_debug)

@typechecked
def mouse_left_up_SendMessage(arg_hwnd: HWND,
                              arg_pos: mouse_position_type,
                              arg_move_mouse: bool = True,
                              arg_debug: bool = False):
    mouse_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_direction_is_down=False, arg_mouse_button_is_left=True, arg_move_mouse=arg_move_mouse, arg_debug=arg_debug)

@typechecked
def mouse_left_click_SendMessage(arg_hwnd: HWND,
                                 arg_pos: mouse_position_type,
                                 arg_move_mouse: bool = True,
                                 arg_debug: bool = False):
    ''' Send a mouse_left_down_SendMessage() and then a mouse_left_up_SendMessage() right after to simulate a click '''
    mouse_left_down_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_move_mouse=arg_move_mouse, arg_debug=arg_debug)
    mouse_left_up_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_move_mouse=arg_move_mouse, arg_debug=arg_debug)

@typechecked
def mouse_left_doubleclick_SendMessage(arg_hwnd: HWND,
                                       arg_pos: mouse_position_type,
                                       arg_move_mouse: bool = True,
                                       arg_debug: bool = False):
    ''' Send a double click message
    https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondblclk

    OBS! On Microsofts site we can read:
    Only windows that have the CS_DBLCLKS style can receive WM_LBUTTONDBLCLK messages,
    which the system generates whenever the user presses, releases, and again presses
    the left mouse button within the system's double-click time limit. Double-clicking
    the left mouse button actually generates a sequence of four messages:
    WM_LBUTTONDOWN, WM_LBUTTONUP, WM_LBUTTONDBLCLK, and WM_LBUTTONUP.
    '''

    client_pos = _win32gui.ScreenToClient(arg_hwnd, arg_pos)
    _lparam = _win32api.MAKELONG(client_pos[0], client_pos[1])
    _win32gui.SendMessage(arg_hwnd, _win32con.WM_ACTIVATE, _win32con.WA_ACTIVE, 0)
    if arg_move_mouse:
        _win32api.SendMessage(arg_hwnd, _win32con.WM_MOUSEMOVE, 0, _lparam)
    # The following line must be here, see the docstring for more info
    mouse_left_click_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_move_mouse=arg_move_mouse, arg_debug=arg_debug)
    _win32api.SendMessage(arg_hwnd, _win32con.WM_LBUTTONDBLCLK, _win32con.MK_LBUTTON, _lparam)
    _win32api.SendMessage(arg_hwnd, _win32con.WM_LBUTTONUP, _win32con.MK_LBUTTON, _lparam)

@typechecked
def mouse_right_down_SendMessage(arg_hwnd: HWND,
                                 arg_pos: mouse_position_type,
                                 arg_move_mouse: bool = True,
                                 arg_debug: bool = False):
    mouse_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_direction_is_down=True, arg_mouse_button_is_left=False, arg_move_mouse=arg_move_mouse, arg_debug=arg_debug)

@typechecked
def mouse_right_up_SendMessage(arg_hwnd: HWND,
                               arg_pos: mouse_position_type,
                               arg_move_mouse: bool = True,
                               arg_debug: bool = False):
    mouse_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_direction_is_down=False, arg_mouse_button_is_left=False, arg_move_mouse=arg_move_mouse, arg_debug=arg_debug)

@typechecked
def mouse_right_click_SendMessage(arg_hwnd: HWND,
                                  arg_pos: mouse_position_type,
                                  arg_move_mouse: bool = True,
                                  arg_debug: bool = False):
    mouse_right_down_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_move_mouse=arg_move_mouse)
    mouse_right_up_SendMessage(arg_hwnd=arg_hwnd, arg_pos=arg_pos, arg_move_mouse=arg_move_mouse)

@typechecked
def mouse_move_SendMessage(arg_hwnd: HWND,
                           arg_pos: mouse_position_type,
                           arg_debug: bool = False):
    ''' Move the mouse to the given position on screen (OBS! It does NOT actually move the mouse, but the events that the target window gets is that) '''
    client_pos = _win32gui.ScreenToClient(arg_hwnd, arg_pos)
    _lparam = _win32api.MAKELONG(client_pos[0], client_pos[1])
    _win32gui.SendMessage(arg_hwnd, _win32con.WM_ACTIVATE, _win32con.WA_ACTIVE, 0)
    _win32api.SendMessage(arg_hwnd, _win32con.WM_MOUSEMOVE, 0, _lparam)

@typechecked
def mouse_left_drag_and_drop_SendMessage(arg_hwnd: HWND,
                                         arg_from_pos: mouse_position_type,
                                         arg_to_pos: mouse_position_type,
                                         arg_debug: bool = False):
    ''' Move mouse to the from position, hold down left mouse button, move the mouse to the to postion, release left mouse button '''
    mouse_left_down_SendMessage(arg_hwnd, arg_from_pos, arg_move_mouse=True, arg_debug=arg_debug)
    mouse_left_up_SendMessage(arg_hwnd, arg_to_pos, arg_move_mouse=True, arg_debug=arg_debug)
