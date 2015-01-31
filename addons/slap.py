# -*- coding: utf-8 -*-
__module_name__        = "Slap"
__module_author__      = "bendem"
__module_version__     = "1.0"
__module_description__ = "Slap command"

import hexchat
import random

slappingMaterials = [
    '><((((º>',
    'good old trout',
    'roasted pancake',
    'frozen fish',
    'whale',
    'dead kitteh',
    'angry russian bear',
]
voyels = 'aeiuoy'

def heading(msg):
    print('%s\t%s' % (__module_name__, msg))

def command(args, word_eol, userdata):
    if len(args) < 2:
        heading('Missing nick argument, use /slap <nick>')
    else:
        material = random.choice(slappingMaterials)
        n = 'n' if material[0] in voyels else ''
        hexchat.command('me slaps %s with a%s %s' % (args[1], n, material))

    return hexchat.EAT_ALL

hexchat.hook_command('slap', command)

heading('Loaded')
