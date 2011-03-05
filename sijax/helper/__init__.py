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


def init_static_path(static_path):
    """Mirrors the important static files from the package into a directory of your choice.

    It may be a good idea to run this for your static path whenever Sijax gets upgraded, so that
    your files will be kept in sync.

    The directory that you provide needs to be empty (if it exists),
    or to have been previously used by Sijax using this same function.
    If the provided directory contains some other files, Sijax will refuse to use it.
    """

    import os, shutil, errno
    import sijax

    def mkdir_p(path):
        """NOOP if the directory exists. If not, it creates the whole directory tree."""
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise exc

    mkdir_p(static_path)

    version_file = os.path.join(static_path, 'sijax_version')

    if os.path.exists(version_file):
        version = open(version_file).read()
    else:
        version = None
        files_count = len(os.walk(static_path).next()[2])
        if files_count != 0:
            # non-empty path with a missing version file
            # this looks like a user directory - we'd better not touch anything!
            raise SijaxError('%s already contains files - Sijax refuses to write there!' % static_path)

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

    fp = open(version_file, 'w')
    fp.write(sijax.__version__)
    fp.close()

