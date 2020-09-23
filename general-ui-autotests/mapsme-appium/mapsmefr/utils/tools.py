import configparser
import logging
import os
import random
import string
from os.path import join, dirname, realpath


def get_settings(block, name):
    rootdir = dirname(realpath(__file__)).split('utils')[0]
    settings = configparser.ConfigParser()
    settings.read(join(rootdir, 'settings.ini'))
    res = settings.get(block, name)
    if res == "None":
        res = os.environ[name]
    return res


def set_settings(block, name, value):
    rootdir = dirname(realpath(__file__)).split('utils')[0]
    settings = configparser.ConfigParser()
    settings.read(join(rootdir, 'settings.ini'))
    settings.set(block, name, value)
    with open(join(rootdir, 'settings.ini'), 'w') as configfile:
        settings.write(configfile)


def get_random_string(length, with_numbers=True):
    letters = string.ascii_letters
    if with_numbers:
        letters = letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def is_element_scrolled(driver, element):
    y = element.location['y']
    height = driver.get_window_size()['height']
    min_y = 250 if get_settings("System", "platform") == "Android" else 120
    return y < height - min_y

