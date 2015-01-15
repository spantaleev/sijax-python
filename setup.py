#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

"""
Sijax
=====

Sijax stands for "Simple ajax" and provides just that.
It's a simple Python/jQuery library providing easy ajax integration for python web apps.

The main idea is to use javascript code that calls server-side callbacks, which generate a response (manipulating the DOM, etc) and pass it back to the client.
This way, you don't need to manually dispatch ajax requests to certain URIs and go over each XML/JSON response manually.

Here's a tiny snippet of code to show what it's capable of doing::

    # Function definition in Python
    def say_hello_handler(obj_response, hello_from, hello_to):
        obj_response.alert("Hello from %s to %s" % (hello_from, hello_to))
        obj_response.alert("Redirecting you..")
        obj_response.redirect("https://github.com/spantaleev/sijax-python")

    # Expose the above function publicly by the name of "say_hello"
    sijax_instance.register_callback("say_hello", say_hello_handler)

    //The above function can be called from javascript using
    Sijax.request('say_hello', ['John', 'Greg']);

Links
-----

* `source <https://github.com/spantaleev/sijax-python>`_
* `documentation <http://packages.python.org/Sijax>`_
"""

import sys, os, re
from setuptools import (setup, find_packages)

def determine_version():
    """Determines the version in a way that works on Python 2.x.

    We need to do it this way, instead of simply importing sijax.__version__,
    because the code can't (initially) work on Python 2.x without the `future`
    dependency being installed.
    """
    regex_version = re.compile("__version__ = '([^']+)'")
    with open(os.path.join(os.path.dirname(__file__), 'sijax', '__init__.py'), 'r') as fp:
        matches = regex_version.search(fp.read())
        if matches is None:
            raise RuntimeError('Cannot determine version')
        return matches.group(1)

def run_tests():
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    from sijax_tests import suite
    return suite()

setup(
    name = "Sijax",
    packages=find_packages(),
    include_package_data = True,
    version = determine_version(),
    description = "An easy to use AJAX library based on jQuery.ajax",
    long_description = __doc__,
    author = "Slavi Pantaleev",
    author_email = "s.pantaleev@gmail.com",
    url = "https://github.com/spantaleev/sijax-python",
    keywords = ["ajax", "jQuery"],
    platforms = "any",
    license = "BSD",
    zip_safe = False,
    install_requires = ["six", "future"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    test_suite='__main__.run_tests'
)
