__module_name__        = "Bear"
__module_author__      = "bendem"
__module_version__     = "1.0"
__module_description__ = "Say bear the right way"

import hexchat

words = {
    'bear': 'ʕ•ᴥ•ʔ',
}

def bear(word, word_eol, userdata):
    if word[0] != "65293" or word[1] != "0": # 65293 is <enter> and 0 is no modifier
        return
    msg = hexchat.get_info('inputbox')
    if msg is None or len(msg) == 0 or msg[0] == '/':
        return

    changed = False
    for word, replace in words.items():
        if word in msg:
            msg = msg.replace(word, replace)
            changed = True
            for user in hexchat.get_list('users'):
                if word in user.nick:
                    msg = msg.replace(user.nick.replace(word, replace), user.nick)

    if changed:
        hexchat.command("settext %s" % msg)

hexchat.hook_print('Key Press', bear, priority = hexchat.PRI_LOWEST)
