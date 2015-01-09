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

def command(word, word_eol, userdata):
    global enabled
    enabled = not enabled
    print('[%s] %s' % (__module_name__, 'enabled' if enabled else 'disabled'))
    return hexchat.EAT_ALL

def message(word, word_eol, userdata):
    if not enabled:
        return

    channel = hexchat.get_info('channel')
    if channel[0] != '#': # Not a channel (query tab)
        return

    if word[0] != "65293" or word[1] != "0": # 65293 is <enter> and 0 is no modifier
        return

    msg = hexchat.get_info('inputbox')
    if msg is None or len(msg) == 0 or msg[0] == '/':
        return

    handle_message(channel, msg)

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
