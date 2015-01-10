__module_name__        = 'Chat Replace'
__module_author__      = 'bendem'
__module_version__     = '1.1'
__module_description__ = 'Add chat snippets'

import hexchat
import re

HEADING          = '[%s]' % __module_name__
BOLD             = '\002'
RESET            = '\017'
KEY_SEPARATOR    = ';'
PLUGIN_PREF_KEYS = 'chat-replace-keys'
PLUGIN_PREF_VAL  = 'chat-replace-val-%s'
DEFAULT_WORDS    = { 'flip': '(╯°□°）╯︵ ┻━┻' }

words   = DEFAULT_WORDS
dirty   = False
enabled = True

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

def load():
    """
    Loads the config.
    """
    global dirty
    global words

    keys = hexchat.get_pluginpref(PLUGIN_PREF_KEYS)
    if keys == None:
        return

    keys = keys.split(KEY_SEPARATOR)
    for key in keys:
        x = hexchat.get_pluginpref(PLUGIN_PREF_VAL % key)
        if x:
            words[key] = x

def save(userdata):
    """
    Saves the current config.
    """
    global dirty

    if not dirty:
        return

    keys = KEY_SEPARATOR.join(words.keys())
    # This is because only the 512 first chars are read
    # https://github.com/hexchat/hexchat/issues/1265
    if len(keys) > 511:
        print('%s Fatal error: Your keys are too long, they cannot be saved!'
            + ' Aborting file corruption to prevent the end of the world!' % HEADING)
        return

    hexchat.set_pluginpref(PLUGIN_PREF_KEYS, keys)
    for key, val in words.items():
        hexchat.set_pluginpref(PLUGIN_PREF_VAL % key, val)

    print('%s Saved' % HEADING)
    dirty = False

def command(word, word_eol, userdata):
    """
    Wraps the command handling.
    """
    if len(word) < 1 or word[0] != 'cr':
        print('%s Error, unhandled command' % HEADING)
    else:
        handle_command(word[1:])

    return hexchat.EAT_ALL

def handle_command(args):
    """
    Handles plugin commands such as list, add, remove, clear and help.
    """
    global dirty
    global words
    global enabled

    if len(args) > 0:
        command = args[0]
    if len(args) > 1:
        key = args[1]
    if len(args) > 2:
        msg = ' '.join(args[2:])

    if command == 'help':
        format = (HEADING, BOLD, RESET)
        print('%s Usage: ' % HEADING)
        print('%s %s/cr <save|help|list|keys|clear|enable|disable>%s' % format)
        print('%s %s/cr <remove> <key>%s'                             % format)
        print('%s %s/cr <add> <key> <content>%s'                      % format)
        return

    if command in ('enable', 'disable'):
        enabled = command == 'enable'
        print('%s %sd' % (HEADING, command))
        return

    if command == 'keys':
        print('%s Keys: %s' % (HEADING, ', '.join(sorted(words.keys()))))
        return

    if command == 'list':
        for key, val in words.items():
            print('%s: %s' % (key, val))
        return

    if command == 'save':
        dirty = True
        save(None)
        return

    if command == 'clear':
        for key in words.keys():
            hexchat.del_pluginpref(key)
        words = {}
        dirty = True
        return

    if command == 'remove' and len(args) > 1:
        if not key in words:
            print('%s Error: Key (%s) not found' % (HEADING, key))
        else:
            del words[key]
            hexchat.del_pluginpref(PLUGIN_PREF_VAL % key)
            print('%s Key removed' % HEADING)
            dirty = True
        return

    if not command == 'add' or len(args) < 3:
        print('%s Error: Malformed command' % HEADING)
        return

    if KEY_SEPARATOR in key:
        print('%s Error: Key cannot contain "%s"' % (HEADING, KEY_SEPARATOR))
        return

    if len(msg) > 511:
        # https://github.com/hexchat/hexchat/issues/1265
        print('%s Error: Message too long')

    words[key] = msg
    print('%s "%s" %s' % (HEADING, key, 'added' if command == 'add' else 'modified'))
    dirty = True

@unicode_check
def message(word, word_eol, userdata):
    """
    Handles a message by replacing its content containing
    `.keyword.` with the appropriate replacement.
    """
    if not enabled:
        return

    channel = hexchat.get_info('channel')
    if channel[0] != '#': # Not a channel (query tab)
        return

    if word[0] != "65293" or word[1] != "0": # 65293 is <enter> and 0 is no modifier
        return

    msg = hexchat.get_info('inputbox')
    if msg is None or len(msg) == 0 or msg[0] == '/' or not '.' in msg:
        return

    needs_changing = False
    for key, val in words.items():
        search = '\\.' + key + '\\.'
        regex = re.compile('(?:^|[^a-zA-Z0-9])%s(?:[^a-zA-Z0-9]|$)' % search)
        if '.%s.' % key == msg or regex.search(msg):
           msg = msg.replace('.' + key + '.', val)
           needs_changing = True

    if needs_changing:
        hexchat.command('settext %s' % msg)

load()
hexchat.hook_print('Key Press', message)
hexchat.hook_command("cr", command)
hexchat.hook_unload(save)
