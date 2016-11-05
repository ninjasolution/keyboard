# -*- coding: utf-8 -*-

from time import time as now

try:
    basestring
except NameError:
    basestring = str

KEY_DOWN = 'down'
KEY_UP = 'up'

class KeyboardEvent(object):
    event_type = None
    scan_code = None
    name = None
    time = None

    def __init__(self, event_type, scan_code, name=None, time=None):
        self.event_type = event_type
        self.scan_code = scan_code
        self.time = now() if time is None else time
        self.name = normalize_name(name)

    def __repr__(self):
        return 'KeyboardEvent({} {})'.format(self.name or 'Unknown {}'.format(self.scan_code), self.event_type)

# TODO: add values from https://svn.apache.org/repos/asf/xmlgraphics/commons/tags/commons-1_0/src/java/org/apache/xmlgraphics/fonts/Glyphs.java
canonical_names = {
    'escape': 'esc',
    'return': 'enter',
    'del': 'delete',
    'control': 'ctrl',
    'altgr': 'alt gr',

    ' ': 'space', # Prefer to spell out keys that would be hard to read.
    '\x1b': 'esc',
    '\x08': 'backspace',
    '\n': 'enter',
    '\t': 'tab',

    'scrlk': 'scroll lock',
    'prtscn': 'print screen',
    'prnt scrn': 'print screen',
    'snapshot': 'print screen',
    'ins': 'insert',
    'pause break': 'pause',
    'ctrll lock': 'caps lock',
    'capslock': 'caps lock',
    'number lock': 'num lock',
    'numlock:': 'num lock',
    'space bar': 'space',
    'spacebar': 'space',
    'linefeed': 'enter',
    'win': 'windows',

    'pagedown': 'page down',
    'next': 'page down', # This looks wrong, but this is how Linux reports.
    'pageup': 'page up',
    'prior': 'page up',

    'underscore': '_',
    'equal': '=',
    'minplus': '+',
    'plus': '+',
    'add': '+',
    'subtract': '-',
    'minus': '-',
    'multiply': '*',
    'asterisk': '*',
    'divide': '/',

    'question': '?',
    'exclam': '!',
    'slash': '/',
    'bar': '|',
    'backslash': '\\',
    'braceleft': '{',
    'braceright': '}',
    'bracketleft': '[',
    'bracketright': ']',
    'parenleft': '(',
    'parenright': ')',

    'period': '.',
    'dot': '.',
    'comma': ',',
    'semicolon': ';',
    'colon': ':',

    'less': '<',
    'greater': '>',
    'ampersand': '&',
    'at': '@',
    'numbersign': '#',
    'hash': '#',
    'hashtag': '#',

    'dollar': '$',
    'sterling': '£',
    'pound': '£',
    'yen': '¥',
    'euro': '€',
    'cent': '¢',
    'currency': '¤',
    'registered': '®',
    'copyright': '©',
    'notsign': '¬',
    'percent': '%',
    'diaeresis': '"',
    'quotedbl': '"',
    'onesuperior': '¹',
    'twosuperior': '²',
    'threesuperior': '³',
    'onehalf': '½',
    'onequarter': '¼',
    'threequarters': '¾',
    'paragraph': '¶',
    'section': '§',
    'ssharp': '§',
    'division': '÷',
    'questiondown': '¿',
    'exclamdown': '¡',
    'degree': '°',
    'guillemotright': '»',
    'guillemotleft': '«',
    
    'acute': '´',
    'agudo': '´',
    'grave': '`',
    'tilde': '~',
    'asciitilde': '~',
    'til': '~',
    'cedilla': ',',
    'circumflex': '^',
    'apostrophe': '\'',
    
    'adiaeresis': 'ä',
    'udiaeresis': 'ü',
    'odiaeresis': 'ö',
    'oe': 'Œ',
    'oslash': 'ø',
    'ooblique': 'Ø',
    'ccedilla': 'ç',
    'ntilde': 'ñ',
    'eacute': 'é',
    'uacute': 'ú',
    'oacute': 'ó',
    'thorn': 'þ',
    'ae': 'æ',
    'eth': 'ð',
    'masculine': 'º',
    'feminine': 'ª',
    'iacute': 'í',
    'aacute': 'á',
    'mu': 'Μ',
    'aring': 'å',

    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',

    # French names.
    'maj': 'shift',
    'impr.ecran': 'print screen',
    'entree': 'enter',
}

def normalize_name(name):
    if not isinstance(name, basestring):
        raise ValueError('Can only normalize string names. Unexpected '+ repr(name))

    name = name.lower()
    if name != '_':
        name = name.replace('_', ' ')

    return canonical_names.get(name, name)
