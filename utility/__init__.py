from unidecode import unidecode

from dataparser import *


def unidecode_stream(f):
    for row in f:
        yield unidecode(unicode(row, 'utf-8'))
