# -*- coding: utf-8 -*-
__module_name__        = 'Flip'
__module_author__      = 'bendem'
__module_version__     = '1.0'
__module_description__ = 'Flips what you write'

import hexchat

chars = {
    'a': 'ɐ',
    'b': 'q',
    'c': 'ɔ',
    'd': 'p',
    'e': 'ǝ',
    'f': 'ɟ',
    'g': 'ƃ',
    'h': 'ɥ',
    'i': 'ᴉ',
    'j': 'ɾ',
    'k': 'ʞ',
    'l': 'l',
    'm': 'ɯ',
    'n': 'u',
    'o': 'o',
    'p': 'd',
    'q': 'b',
    'r': 'ɹ',
    's': 's',
    't': 'ʇ',
    'u': 'n',
    'v': 'ʌ',
    'w': 'ʍ',
    'x': 'x',
    'y': 'ʎ',
    'z': 'z',
    '\'':',',
    ',':'\'',
}
enabled = False

def unicode_check(func):
    """
    Retry in case of unicode fail due to a known HexChat bug.
    See https://github.com/hexchat/hexchat/issues/869
    """
    def unicode_check_and_call(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UnicodeDecodeError:
            # Retrying
            return func(*args, **kwargs)
    return unicode_check_and_call

def command(word, word_eol, userdata):
    global enabled
    enabled = not enabled
    print('[%s] %s' % (__module_name__, 'enabled' if enabled else 'disabled'))
    return hexchat.EAT_ALL

def bs(val, pos):
    return bool(val & (1 << pos))

@unicode_check
def message(word, word_eol, userdata):
    if not enabled:
        return

    channel = hexchat.get_info('channel')
    if channel[0] != '#': # Not a channel (query tab)
        return

    # 65293 is <enter>
    # 65421 is numpad <enter>
    # 0 is no modifier
    # 1 is caps lock
    # 4 is num lock
    mod = int(word[1])
    if (word[0] != "65293" and word[0] != "65421") or (mod != 0 and not bs(mod, 1) and not bs(mod, 4)):
        return

    msg = hexchat.get_info('inputbox')
    if msg is None or len(msg) == 0 or msg[0] == '/':
        return

    handle_message(channel, msg)

@unicode_check
def handle_message(channel, msg):
    new = []
    for i in range(len(msg)):
        if msg[i] in chars:
            new.append(chars[msg[i]])
        else:
            new.append(msg[i])

    msg = ''.join(new)

    hexchat.command('settext %s' % msg[::-1])

hexchat.hook_print('Key Press', message)
hexchat.hook_command("flip", command)
