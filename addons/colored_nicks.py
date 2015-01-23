# -*- coding: utf-8 -*-
__module_name__        = 'Colored Nicks'
__module_author__      = 'bendem'
__module_version__     = '1.0'
__module_description__ = 'Colorize nicks in messages'

import hexchat
import re

edited = False

RESET  = '\017'
COLOR  = '\003%s'
BLUE   = COLOR % '18'
FORMAT = RESET + BLUE + '%s' + RESET + '%s%s' + RESET

colors = (19, 20, 22, 24, 25, 26, 27, 28, 29)

def nick_color(nick):
    total = sum(ord(letter) for letter in nick)
    total %= len(colors)
    return colors[total]

def message(word, word_eol, userdata, attributes):
    global edited
    if(edited):
        return

    nick = word[0]
    msg  = word[1]
    mode = word[2] if len(word) == 3 else ''

    for u in hexchat.get_context().get_list('users'):
        if u.nick in msg:
            msg = re.sub(
                r'\b%s\b' % re.escape(u.nick),
                FORMAT % (u.prefix, COLOR % nick_color(u.nick), u.nick),
                msg
            )

    edited = True
    hexchat.emit_print(userdata, nick, msg, mode, time = attributes.time)
    edited = False
    return hexchat.EAT_ALL

events = [
    'Channel Action',
    'Channel Message',
    'Channel Msg Hilight',
    'Channel Action Hilight'
]
for e in events:
    hexchat.hook_print_attrs(e, message, priority = hexchat.PRI_LOW, userdata = e)
