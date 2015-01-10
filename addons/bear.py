__module_name__        = "Bear"
__module_author__      = "bendem"
__module_version__     = "1.0"
__module_description__ = "Say bear the right way"

import hexchat

words = {
    'bear': 'ʕ•ᴥ•ʔ',
}

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

@unicode_check
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
