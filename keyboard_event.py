class KeyboardEvent(object):
    @staticmethod
    def keycode_to_char(keycode):
        if 32 <= keycode < 128:
            return chr(keycode)
        else:
            return None

    @staticmethod
    def keycode_to_name(keycode):
        try:
            return keycode_to_name[keycode]
        except KeyError:
            return KeyboardEvent.keycode_to_char(keycode)

    @staticmethod
    def name_to_keycode(name):
        return name_to_keycode.get(name.lower(), None)

    def __init__(self, event_type, keycode, scan_code, alt_pressed, time, char=None):
        self.event_type = event_type
        self.keycode = keycode
        self.scan_code = scan_code
        self.alt_pressed = alt_pressed
        self.time = time
        self.name = KeyboardEvent.keycode_to_name(keycode)
        if char is None:
            self.char = KeyboardEvent.keycode_to_char(keycode)
        else:
            self.char = char

    def __str__(self):
        return 'KeyboardEvent({} {})'.format(self.name,
                                             'up' if self.event_type
                                             == KEY_UP else 'down')

KEY_DOWN = 'key down'
KEY_UP = 'key up'

name_to_keycode = {
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    'f1': 112,
    'f2': 113,
    'f3': 114,
    'f4': 115,
    'f5': 116,
    'f6': 117,
    'f7': 118,
    'f8': 119,
    'f9': 120,
    'f10': 121,
    'f11': 122,
    'f12': 123,
    'f13': 124,
    'f14': 125,
    'f15': 126,
    'f16': 127,
    'f17': 128,
    'f18': 129,
    'f19': 130,
    'f20': 131,
    'f21': 132,
    'f22': 133,
    'f23': 134,
    'f24': 135,
    'a': 65,
    'accept': 30,
    'add': 107,
    'alt': 164,
    'apps': 93,
    'attn': 246,
    'b': 66,
    'back': 8,
    'backspace': 8,
    'browser back': 166,
    'browser forward': 167,
    'browser_back': 166,
    'browser_forward': 167,
    'c': 67,
    'cancel': 3,
    'capital': 20,
    'capslock': 20,
    'clear': 12,
    'control': 17,
    'convert': 28,
    'crsel': 247,
    'ctrl': 162,
    'd': 68,
    'decimal': 110,
    'delete': 46,
    'del': 46,
    'divide': 111,
    'down': 40,
    'e': 69,
    'end': 35,
    'enter': 13,
    'ereof': 249,
    'esc': 27,
    'escape': 27,
    'execute': 43,
    'exsel': 248,
    'f': 70,
    'final': 24,
    'g': 71,
    'h': 72,
    'hangeul': 21,
    'hangul': 21,
    'hanja': 25,
    'help': 47,
    'home': 36,
    'i': 73,
    'insert': 45,
    'j': 74,
    'junja': 23,
    'k': 75,
    'kana': 21,
    'kanji': 25,
    'l': 76,
    'lbutton': 1,
    'lcontrol': 162,
    'left': 37,
    'lmenu': 164,
    'lshift': 160,
    'lwin': 91,
    'win': 91,
    'm': 77,
    'mbutton': 4,
    'media next track': 176,
    'media play pause': 179,
    'media prev track': 177,
    'media_next_track': 176,
    'media_play_pause': 179,
    'media_prev_track': 177,
    'menu': 18,
    'modechange': 31,
    'multiply': 106,
    'n': 78,
    'next': 34,
    'noname': 252,
    'nonconvert': 29,
    'numlock': 144,
    'numpad0': 96,
    'numpad1': 97,
    'numpad2': 98,
    'numpad3': 99,
    'numpad4': 100,
    'numpad5': 101,
    'numpad6': 102,
    'numpad7': 103,
    'numpad8': 104,
    'numpad9': 105,
    'o': 79,
    'oem clear': 254,
    'oem_clear': 254,
    'p': 80,
    'pa1': 253,
    'pause': 19,
    'play': 250,
    'print': 42,
    'prior': 33,
    'processkey': 229,
    'q': 81,
    'r': 82,
    'rbutton': 2,
    'rcontrol': 163,
    'return': 13,
    '\n': 13,
    'right': 39,
    'rmenu': 165,
    'rshift': 161,
    'rwin': 92,
    's': 83,
    'scroll': 145,
    'select': 41,
    'separator': 108,
    'shift': 160,
    'snapshot': 44,
    'space': 32,
    ' ': 32,
    'subtract': 109,
    't': 84,
    'tab': 9,
    '\t': 9,
    'u': 85,
    'up': 38,
    'v': 86,
    'volume down': 174,
    'volume mute': 173,
    'volume up': 175,
    'volume_down': 174,
    'volume_mute': 173,
    'volume_up': 175,
    'w': 87,
    'x': 88,
    'xbutton1': 5,
    'xbutton2': 6,
    'y': 89,
    'z': 90,
    'zoom': 251,
}

keycode_to_name = {keycode: name for name, keycode in
                   name_to_keycode.items()}
