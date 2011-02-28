# -*- coding: utf-8 -*-

"""
    sijax.helper
    ~~~~~~~~~~~~

    Provides various helper functions and objects that other modules use.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from ..exception import SijaxError


# try to load the best simplejson implementation available.  If JSON
# is not installed, we add a failing class.
json = None
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            # Google Appengine offers simplejson via django
            from django.utils import simplejson as json
        except ImportError:
            pass

if json is None:
    raise SijaxError("You need a JSON library to use Sijax!")

