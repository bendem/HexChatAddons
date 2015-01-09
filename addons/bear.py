__module_name__ = "Bear PLEASE"
__module_author__ = "bendem"
__module_version__ = "1.0"
__module_description__ = "say bear the right way"

import hexchat

def bear(word, word_eol, userdata):
    if word[0] != "65293" or word[1] != "0": # 65293 is <enter> and 0 is no modifier
        return
    msg = hexchat.get_info('inputbox')
    if msg is None or len(msg) == 0 or msg[0] == '/':
        return

    if 'bear' in msg:
        hexchat.command("settext " + msg.replace('bear', 'ʕ•ᴥ•ʔ').replace('Curlyʕ•ᴥ•ʔ', 'Curlybear'))

hexchat.hook_print('Key Press', bear)
