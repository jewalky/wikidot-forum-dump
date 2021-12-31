# -*- coding: utf-8 -*-

import logging
import os

# this file sets up 'logging' default package to use our format
LOGLEVEL = os.getenv('LOGLEVEL', 'INFO')


class Formatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        prepend = '  '
        if record.levelname == 'INFO':
            prepend = '=='
        if record.levelname == 'WARNING' or record.levelname == 'ERROR' or record.levelname == 'CRITICAL':
            prepend = '!!'
        try:
            prepend = record.__dict__['ext_level']
        except:
            pass

        return ' %s  %s' % (prepend, super().format(record))


def setup():
    loglevel_int = getattr(logging, LOGLEVEL.upper())
    bad_loglevel = False
    if type(loglevel_int) != int:
        bad_loglevel = True
        loglevel_int = logging.INFO
    console = logging.StreamHandler()
    console.setLevel(loglevel_int)
    # set a format which is simpler for console use
    formatter = Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.basicConfig(level=LOGLEVEL, handlers=[console])
    if bad_loglevel:
        logging.warning('Bad log level specified (%s), falling back to INFO', LOGLEVEL)


setup()