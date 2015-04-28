# -*- coding: utf-8 -*-
__module_name__        = "Pings"
__module_author__      = "bendem"
__module_version__     = "1.0"
__module_description__ = "Prints all pings you receive in a separate tab"

from time import time
import hexchat

COLOR    = '\003%s'
PREF     = 'backlog_last_hl'
RESET    = '\017'
TAB_NAME = 'HLs'

waiting  = 0
messages = []
last_hl  = 0
previous_session_last_hl = 0

colors   = (19, 20, 22, 24, 25, 26, 27, 28, 29)

def nick_color(nick):
    total = sum(ord(letter) for letter in nick)
    total %= len(colors)
    return colors[total]

def message(word, word_eol, userdata, attributes):
    # Get real timestamp
    stamp = attributes.time if attributes.time else int(time())

    # Ignore messages from previous sessions
    if previous_session_last_hl >= stamp:
        return

    global last_hl
    global messages

    if stamp > last_hl:
        last_hl = stamp

    messages.append((
        stamp,
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

    # We're not waiting and it's not from backlog, display it now
    if waiting == 0 and attributes.time == 0:
        printStuff()

def printStuff():
    """
    Display all messages in queue and saves the last timestamp.

    If there are multiple messages, they are sorted by time.
    """
    global messages

    count = len(messages)

    # if no hls, no need to do stuff
    if count == 0:
        return

    # Sort by time if there is more than one
    if count != 1:
        messages.sort(key = lambda t: t[0])

    # Get the tab if it exists
    ctx = hexchat.find_context('', '')

    if not ctx:
        # Or create a new one
        hexchat.command('newserver -noconnect')
        ctx = hexchat.find_context('', '')
        ctx.command('settab %s'  % TAB_NAME)

    for message in messages:
        ctx.emit_print(
            'Generic Message',
            message[1],
            message[2],
            time = message[0]
        )

    if count:
        # Reset the messages
        messages = []
        # Color the hl tab
        ctx.command('gui color 3')
        # and save the last_hl
        hexchat.set_pluginpref(PREF, last_hl)

    return

def forcePrint(word, word_eol, userdata):
    """
    The /backlog command forces to print all messages in queue
    """
    global waiting

    waiting -= 1
    if waiting == 0:
        printStuff()

    return hexchat.EAT_ALL

def connection(word, word_eol, userdata, attributes):
    """
    Display all messages at once 5 seconds after a connection.

    That way, messages can be sorted by time instead of
    having all from one channel, then all from another, etc.
    """
    global waiting
    waiting += 1
    hexchat.command('timer 5 backlog')

# Get last hilight (so we don't print hls already seen from backlogs)
previous_session_last_hl = hexchat.get_pluginpref(PREF)
if previous_session_last_hl:
    previous_session_last_hl = int(previous_session_last_hl)
    last_hl = previous_session_last_hl
else:
    previous_session_last_hl = 0
    last_hl = 0

hexchat.hook_print_attrs('Channel Msg Hilight', message)
hexchat.hook_print_attrs('Channel Action Hilight', message)
hexchat.hook_command('backlog', forcePrint)
# 376: RPL_ENDOFMOTD (just before starting receiving backlogs if any)
hexchat.hook_server_attrs('376', connection)

print('%s\tLoaded' % __module_name__)
