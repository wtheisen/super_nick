import weechat as w
from collections import OrderedDict

w.register("super_nick", "FlashCode", "1.0", "GPL3", "Test script", "", "")

def build_list(data, item, window):
    currBuffer = w.current_buffer()

    nicklist = {}
    infolist_nicklist = w.infolist_get('nicklist', currBuffer, '')
    while w.infolist_next(infolist_nicklist):
        nick = w.infolist_string(infolist_nicklist, 'name')
        prefix = w.infolist_string(infolist_nicklist, 'prefix')
        pColor = w.color(w.infolist_string(infolist_nicklist, 'prefix_color'))
        nick_type = w.infolist_string(infolist_nicklist, 'type')
        if nick_type != 'nick':
            pass
        else:
            if not nicklist.has_key(pColor + prefix):
                if prefix == '':
                    prefix = ' '
                nicklist[pColor + prefix]=[]
            nicklist[pColor + prefix].append(nick)

    nickListString = ''
    opOrder = {k:v for v,k in enumerate(['~', '&', '@', '%', '+', ' '])}
    nicklist = OrderedDict(sorted(nicklist.items(), key=lambda i:opOrder.get(i[0][-1])))
    print(nicklist)
    for p,l in nicklist.items():
        nickListString += ''.join(['{}{}{}\n'.format(p, w.info_get('nick_color', n), n) for n in l])
    return nickListString

def update_super_nick(data, signal, signal_data):
    # print('buffer switched')
    w.bar_item_update('super_nick_list')
    return w.WEECHAT_RC_OK

super_nick_list = w.bar_item_new('super_nick_list', 'build_list', '')
super_nick_bar = w.bar_new("super_nick", "off", "100", "root", "", "right", "vertical", "vertical",
    "15", "15", "default", "cyan", "black", "on", 'super_nick_list')

h = w.hook_signal('buffer_switch', 'update_super_nick', '')
h = w.hook_signal('buffer_opened', 'update_super_nick', '')

h = w.hook_signal('window_switch', 'update_super_nick', '')
h = w.hook_signal('irc_channel_opened', 'update_super_nick', '')

h = w.hook_signal('nicklist_nick_changed', 'update_super_nick', '')
h = w.hook_signal('nicklist_nick_added', 'update_super_nick', '')
h = w.hook_signal('nicklist_nick_removed', 'update_super_nick', '')

print('super_nick loaded...')
