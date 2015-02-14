# -*- coding: utf-8 -*-
__module_name__        = "Backlog summary"
__module_author__      = "bendem"
__module_version__     = "1.0"
__module_description__ = "Prints pings from your backlog in a separate tab"

from time import gmtime, mktime
import hexchat

COLOR = '\003%s'
RESET = '\017'
PREF  = 'backlog_last_hl'

messages = []
last_hl  = 0
hooks    = []

colors = (19, 20, 22, 24, 25, 26, 27, 28, 29)

def nick_color(nick):
    total = sum(ord(letter) for letter in nick)
    total %= len(colors)
    return colors[total]

def message(word, word_eol, userdata, attributes):
    # if not backlog or already seen
    if attributes.time == 0 or last_hl >= attributes.time:
        return

    global messages

    messages.append((
        attributes.time,
        '%s%s%s/%s%s%s' % (
            COLOR % nick_color(word[0]),
            word[0],
            RESET,
            COLOR % 18,
            hexchat.get_info('channel'),
            RESET
        ),
        word[1]
    ))

def printStuff(word, word_eol, userdata):
    # Disable all the things
    for hook in hooks:
        hexchat.unhook(hook)

    # if no hls, no need to do stuff
    if len(messages) == 0:
        print('%s\tNo backlogs' % __module_name__)
        return hexchat.EAT_ALL

    # Sort by time
    messages.sort(key = lambda t: t[0])

    # Create new tab
    hexchat.command('newserver')
    context = hexchat.find_context(channel = '')
    context.command('settab Backlog HLs')

    for message in messages:
        context.emit_print(
            'Generic Message',
            message[1],
            message[2],
            time = message[0]
        )

    if len(messages) != 0:
        hexchat.set_pluginpref(PREF, messages[-1][0])

    return hexchat.EAT_ALL

def unload(userdata):
    hexchat.set_pluginpref(PREF, mktime(gmtime()))

# Get last hilight (so we don't print hls already seen)
last_hl = hexchat.get_pluginpref(PREF)
if last_hl:
    last_hl = int(last_hl)
else:
    last_hl = 0

hooks.append(hexchat.hook_print_attrs('Channel Msg Hilight', message))
hooks.append(hexchat.hook_print_attrs('Channel Action Hilight', message))
hooks.append(hexchat.hook_command('backlog', printStuff))

# Hook on quit to save the timestamp the client was closed at
hexchat.hook_unload(unload)

# display backlogs in 10 seconds
hexchat.command('timer 10 backlog')

print('%s\tLoaded' % __module_name__)
