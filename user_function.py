import json

import datetime
from config import bot_config


# read file
def get_users():
    with open(bot_config['user_file'], 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            print "Error on read user file"
            data = {}
        return data


# save to file:
def add_user(user, address):
    print("Add user " + user + ' ' + address)
    data = get_users()
    with open(bot_config['user_file'], 'w') as f:
        data[user] = address
        json.dump(data, f)


def get_user_info(msg):
    dict = get_users()
    address = dict[msg.author.name]
    msg.reply(msg.author.name + ' your address is ' + address)


def get_user_address(user):
    dict = get_users()
    return dict[user]


def user_exist(user):
    dict = get_users()
    if user in dict.keys():
        return True
    else:
        return False


def get_unregistered_tip():
    with open(bot_config['unregistered_tip_user'], 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            print "Error on read unregistered tip user file"
            data = {}
        return data


def save_unregistered_tip(sender, receiver, amount):
    print("Save tip form %s to %s " % (sender, receiver))
    data = get_unregistered_tip()
    with open(bot_config['unregistered_tip_user'], 'w') as f:
        data[receiver] = []
        data[receiver].append({
            'amount': amount,
            'sender': sender,
            'time': datetime.datetime.now().isoformat(),
        })
        json.dump(data, f)


def get_user_pending_tip(username):
    unregistered_tip = get_unregistered_tip()
    if username in unregistered_tip.keys():
        return unregistered_tip[username]
    else:
        return False


def remove_pending_tip(username):
    unregistered_tip = get_unregistered_tip()
    del unregistered_tip[username]
    with open(bot_config['unregistered_tip_user'], 'w+') as f:
        json.dump(unregistered_tip, f)


def get_user_history(user):
    with open(bot_config['user_history_path'] + user + '.json', 'r') as f:
        try:
            data = json.load(f)
        except IOError:
            print "Error on read user file history"
            data = {}
        except ValueError:
            print "Error on read user file history"
            data = []
        return data


def add_to_history(user, sender, receiver, amount, action, finish=True):
    print("Save for history user=%s, sender=%s, receiver=%s, amount=%s, action=%s, finish=%s" % (
        user, sender, receiver, amount, action, finish))
    data = get_user_history(user)
    with open(bot_config['user_history_path'], 'w+') as f:
        data.append({
            "user": user, "sender": sender, "receiver": receiver, "amount": amount, "action": action,
            "finish": finish,
            'time': datetime.datetime.now().isoformat(),
        })
        json.dump(data, f)
