# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

"""
    sijax.helper
    ~~~~~~~~~~~~

    Provides various helper functions and objects that other modules use.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from builtins import (next, open)
from .exception import SijaxError


# Try to load the best json implementation,
# If json support is not available, we'll add
# an object that raises a RuntimeError when used
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
    class _JSON(object):
        def __getattr__(self, name):
            raise RuntimeError('You need a JSON library to use Sijax!')
    json = _JSON()


def init_static_path(static_path):
    """Mirrors the important static files from the whole Sijax package
    into a directory of your choice.

    It may be a good idea to run this whenever Sijax gets upgraded,
    so that your files will be kept in sync.

    The directory that you provide needs to be empty (if it exists),
    or to have been previously used by this same function.
    If the provided directory contains some other files, Sijax will refuse
    to use it, by raising a :class:`sijax.exception.SijaxError` exception.

    The following files will be made available in the specified directory:

    * ``sijax.js`` - the core javascript file used by Sijax
    * ``json2.js`` - JSON library that can be loaded for browsers
                     that don't support native JSON (like IE <= 7)
    * ``sijax_comet.js`` - the javascript file used by the Comet plugin
    * ``sijax_upload.js`` - the javascript file used by the Upload plugin
    * ``sijax_version`` - a system file that keeps track of versioning -
                          do not touch this file
    """

    import os, shutil
    import sijax

    def mkdir_p(path):
        """Creates the whole directory tree (recursively), if it's missing."""
        if not os.path.exists(path):
            os.makedirs(path)

    mkdir_p(static_path)

    version_file = os.path.join(static_path, 'sijax_version')

    if os.path.exists(version_file):
        with open(version_file) as fp:
            version = fp.read()
    else:
        version = None
        files_count = len(next(os.walk(static_path))[2])
        if files_count != 0:
            # non-empty path with a missing version file
            # this looks like a user directory - we'd better not touch anything!
            raise SijaxError('%s already contains files - refusing to write there!' %
                             static_path)

    if version == sijax.__version__:
        return

    if version is not None:
        # Cleanup previous files first
        for root, dirs, files in os.walk(static_path):
            for file_name in files:
                os.unlink(os.path.join(root, file_name))

    files = []

    core_js = os.path.join(os.path.dirname(sijax.__file__), 'js/')
    files.append(os.path.join(core_js, 'sijax.js'))
    files.append(os.path.join(core_js, 'json2.js'))

    plugins = os.path.join(os.path.dirname(sijax.__file__), 'plugin')
    files.append(os.path.join(plugins, 'comet/js/sijax_comet.js'))
    files.append(os.path.join(plugins, 'upload/js/sijax_upload.js'))

    for src_path in files:
        file_name = os.path.basename(src_path)
        dst_path = os.path.join(static_path, file_name)

        if not os.path.lexists(dst_path):
            shutil.copyfile(src_path, dst_path)

    with open(version_file, 'w') as fp:
        fp.write(sijax.__version__)

