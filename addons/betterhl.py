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

MSG_HEADER    = translate('%C28%s%B%I%C%s%s%R')
MSG_FORMAT    = translate('%I%s%R')
ACTION_HEADER = translate('%B%C%s*%R')
ACTION_FORMAT = translate('%C28%s%C%s%B%I%s%R %I%s')

colors = (19, 20, 22, 24, 25, 26, 27, 28, 29)

def nick_color(nick):
    # TODO Handle clients not having nick colors with
    # hexchat.get_prefs('text_color_nicks')
    total = sum(ord(letter) for letter in nick)
    total %= len(colors)
    return colors[total]

def printMessage(mode, nick, msg, time):
    hexchat.emit_print(
        'Generic Message',
        MSG_HEADER % (mode, nick_color(nick), nick),
        MSG_FORMAT % msg,
        time = time
    )

def printAction(mode, nick, msg, time):
    color = nick_color(nick)
    hexchat.emit_print(
        'Generic Message',
        ACTION_HEADER % color,
        ACTION_FORMAT % (mode, color, nick, msg),
        time = time
    )

def message(word, word_eol, userdata, attributes):
    nick = word[0]
    msg  = word[1].replace(ITALIC, '').replace(RESET, RESET + ITALIC)
    mode = word[2] if len(word) == 3 else ''
    fct = printAction if userdata else printMessage
    fct(mode, nick, msg, attributes.time)

    return hexchat.EAT_HEXCHAT


hexchat.hook_print_attrs('Channel Msg Hilight', message, priority = hexchat.PRI_LOWEST)
hexchat.hook_print_attrs('Channel Action Hilight', message, priority = hexchat.PRI_LOWEST, userdata = True)

print('%s\tLoaded' % __module_name__)
