import time
import unittest
import keyboard
from keyboard_event import KeyboardEvent, canonical_names, KEY_DOWN, KEY_UP
import string

# Fake events with fake scan codes for a totally deterministic test.
all_names = list(canonical_names.values()) + list(string.ascii_lowercase) + ['shift']
scan_codes_by_name = {name: i for i, name in enumerate(all_names)}
class FakeEvent(KeyboardEvent):
	def __init__(self, event_type, name):
		self.event_type = event_type
		self.names = [name]
		self.scan_code = scan_codes_by_name[name]
		self.time = time.time()

class FakeOsKeyboard(object):
	def __init__(self, append):
		self.append = append
		self.scan_code_table = {code: [(name, False)] for name, code in scan_codes_by_name.items()}

	def press(self, scan_code):
		self.append((KEY_DOWN, next(name for name, i in scan_codes_by_name.items() if i == scan_code)))

	def release(self, scan_code):
		self.append((KEY_UP, next(name for name, i in scan_codes_by_name.items() if i == scan_code)))

	def map_char(self, char):
		return scan_codes_by_name[char.lower()], char.isupper()

class TestKeyboard(unittest.TestCase):
	def setUp(self):
		# We will use our own events, thank you very much.
		keyboard.listener.listening = True
		self.events = []
		keyboard.os_keyboard = FakeOsKeyboard(self.events.append)

	def press(self, name):
		keyboard.listener.callback(FakeEvent(KEY_DOWN, name))

	def release(self, name):
		keyboard.listener.callback(FakeEvent(KEY_UP, name))

	def click(self, name):
		self.press(name)
		self.release(name)

	def flush_events(self):
		events = list(self.events)
		self.events.clear()
		return events

	def test_is_pressed(self):
		self.assertFalse(keyboard.is_pressed('enter'))
		self.assertFalse(keyboard.is_pressed(scan_codes_by_name['enter']))
		self.press('enter')
		self.assertTrue(keyboard.is_pressed('enter'))
		self.assertTrue(keyboard.is_pressed(scan_codes_by_name['enter']))
		self.release('enter')
		self.assertFalse(keyboard.is_pressed('enter'))
		self.click('enter')
		self.assertFalse(keyboard.is_pressed('enter'))

		self.press('enter')
		self.assertFalse(keyboard.is_pressed('ctrl+enter'))
		self.press('ctrl')
		self.assertTrue(keyboard.is_pressed('ctrl+enter'))

	def triggers(self, combination, keys):
		self.triggered = False
		def on_triggered():
			self.triggered = True
		keyboard.add_hotkey(combination, on_triggered)
		for group in keys:
			for key in group:
				self.assertFalse(self.triggered)
				self.press(key)
			for key in reversed(group):
				self.release(key)
		keyboard.remove_hotkey(combination)
		return self.triggered

	def test_register_hotkey(self):
		self.assertFalse(self.triggers('a', [['b']]))
		self.assertTrue(self.triggers('a', [['a']]))
		self.assertTrue(self.triggers('a, b', [['a'], ['b']]))
		self.assertFalse(self.triggers('b, a', [['a'], ['b']]))
		self.assertTrue(self.triggers('a+b', [['a', 'b']]))
		self.assertTrue(self.triggers('ctrl+a, b', [['ctrl', 'a'], ['b']]))
		self.assertFalse(self.triggers('ctrl+a, b', [['ctrl'], ['a'], ['b']]))
		self.assertTrue(self.triggers('ctrl+a, b', [['a', 'ctrl'], ['b']]))
		self.assertTrue(self.triggers('ctrl+a, b, a', [['ctrl', 'a'], ['b'], ['ctrl', 'a'], ['b'], ['a']]))

	def test_write(self):
		keyboard.write('a')
		self.assertEqual(self.flush_events(), [(KEY_DOWN, 'a'), (KEY_UP, 'a')])

		keyboard.write('ab')
		self.assertEqual(self.flush_events(), [(KEY_DOWN, 'a'), (KEY_UP, 'a'), (KEY_DOWN, 'b'), (KEY_UP, 'b')])

		keyboard.write('Ab')
		self.assertEqual(self.flush_events(), [(KEY_DOWN, 'shift'), (KEY_DOWN, 'a'), (KEY_UP, 'a'), (KEY_UP, 'shift'), (KEY_DOWN, 'b'), (KEY_UP, 'b')])
		


if __name__ == '__main__':
	unittest.main()