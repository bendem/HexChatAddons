# -*- coding: utf-8 -*-
__module_name__        = 'BetterHL'
__module_author__      = 'bendem'
__module_version__     = '1.1'
__module_description__ = 'Better highlighting system (IMO)'

import hexchat

COLOR  = '\003'
BOLD   = '\002'
ITALIC = '\035'
HIDDEN = '\010'
RESET  = '\017'

def translate(x):
    return x                   \
        .replace('%H', HIDDEN) \
        .replace('%C', COLOR)  \
        .replace('%R', RESET)  \
        .replace('%I', ITALIC) \
        .replace('%B', BOLD)

MSG_FORMAT    = translate('%H<%H%C28%s%B%I%C%s%s%R%H>%H\t%I%s')
ACTION_FORMAT = translate('%H<%H%B%C%s*%R%H>%H\t%C28%s%C%s%B%I%s%R %I%s')

colors = (19, 20, 22, 24, 25, 26, 27, 28, 29)

def nick_color(nick):
    total = sum(ord(letter) for letter in nick)
    total %= len(colors)
    return colors[total]

def printMessage(mode, nick, msg):
    print(MSG_FORMAT % (mode, nick_color(nick), nick, msg))

def printAction(mode, nick, msg):
    color = nick_color(nick)
    print(ACTION_FORMAT % (color, mode, color, nick, msg))

def message(word, word_eol, userdata):
    nick = word[0]
    msg  = word[1]
    mode = word[2] if len(word) == 3 else ''
    fct = printAction if userdata else printMessage
    fct(mode, nick, msg)

    return hexchat.EAT_HEXCHAT


hexchat.hook_print('Channel Msg Hilight', message, priority = hexchat.PRI_LOWEST)
hexchat.hook_print('Channel Action Hilight', message, priority = hexchat.PRI_LOWEST, userdata = True)
