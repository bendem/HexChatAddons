# -*- coding: utf-8 -*-
__module_name__        = 'Pastebin'
__module_author__      = 'bendem'
__module_version__     = '1.0'
__module_description__ = 'Pastes large stuff on gist instead of flooding'

import base64
import hexchat
import json
import urllib.error
import urllib.parse
import urllib.request

GIST_END_POINT = 'https://api.github.com/gists'
USER           = '<redacted>'
PASSWORD       = '<redacted>'
ENCODING       = 'UTF-8'
HEADERS        = {
    'Accept'        : 'application/vnd.github.v3+json',
    'Accept-Charset': ENCODING,
    'Content-Type'  : 'application/json',
    'User-Agent'    : '%s/v%s/hexchat_script/python' % (__module_name__, __module_version__),
    'Authorization' : 'Basic %s' % base64.b64encode(('%s:%s' % (USER, PASSWORD)).encode(ENCODING)).decode(ENCODING)
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

def bs(val, pos):
    return bool(val & (1 << pos))

@unicode_check
def message(word, word_eol, userdata):
    channel = hexchat.get_info('channel')
    if channel[0] != '#': # Not a channel (query tab)
        return

    # 65293 is <enter>
    # 65421 is numpad <enter>
    # 0 is no modifier
    # 1 is caps lock
    # 4 is num lock
    mod = int(word[1])
    if (word[0] != "65293" and word[0] != "65421") or (mod != 0 and not bs(mod, 1) and not bs(mod, 4)):
        return

    msg = hexchat.get_info('inputbox')
    if msg is None or len(msg) == 0 or msg[0] == '/':
        return

    handle_message(channel, msg)

@unicode_check
def handle_message(channel, msg):
    msg = msg.strip('\n')
    if msg.count('\n') > 2:
        url = post_to_gist('Content pasted in %s' % channel, msg)
        hexchat.command("settext I posted too much, here is the paste: %s" % url)

@unicode_check
def post_to_gist(description, content):
    data = {
        'description': description,
        'public': False,
        'files': {
            'ircpaste.txt': {
                'content': content
            }
        }
    }

    code, content = post(GIST_END_POINT, data)
    if code < 200 or code > 299:
        return 'error (%s): %s' % (code, content)

    decoded = json.loads(content.decode(ENCODING))
    return decoded['html_url']

@unicode_check
def post(url, data):
    data = json.dumps(data).encode(ENCODING)

    request = urllib.request.Request(url, data, headers = HEADERS)
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        return (e.code, e.msg)

    return (response.code, response.read())

hexchat.hook_print('Key Press', message)
