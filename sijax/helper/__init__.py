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

