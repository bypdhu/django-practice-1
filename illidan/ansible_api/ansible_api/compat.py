import sys

py3 = sys.version_info[0] == 3

if py3:
    string_types = (str, )
    text_type = str
else:
    string_types = (basestring, )
    text_type = unicode
