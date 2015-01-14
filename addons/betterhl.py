# -*- coding: utf-8 -*-
__module_name__        = 'BetterHL'
__module_author__      = 'bendem'
__module_version__     = '1.0'
__module_description__ = 'Better highlighting system (IMO)'

import hexchat

colors = (19, 20, 22, 24, 25, 26, 27, 28, 29)

def nick_color(nick):
    total = sum(ord(letter) for letter in nick)
    total %= len(colors)
    return colors[total]

def message(word, word_eol, userdata):
    nick = word[0]
    msg  = word[1]
    mode = word[2] if len(word) == 3 else ''
    print('\010<\010\00328%s\002\003%s%s\017\010>\010\t\035%s' % (mode, nick_color(nick), nick, msg))

    return hexchat.EAT_HEXCHAT


hexchat.hook_print('Channel Msg Hilight', message)
