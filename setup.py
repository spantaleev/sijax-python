"""
Sijax
=====

Sijax stands for "Simple ajax" and provides just that.
It's a simple Python/jQuery library providing easy ajax integration for python web apps.

The main idea is to use javascript code that calls server-side callbacks, which generate a response (manipulating the DOM, etc) and pass it back to the client.
This way, you don't need to manually dispatch ajax requests to certain URIs and go over each XML/JSON response manually.
"""

from setuptools import setup, find_packages


def run_tests():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    from sijax_tests import suite
    return suite()


setup(
    name = "Sijax",
    packages = find_packages(),
    include_package_data = True,
    version = "0.1.1",
    description = "An easy to use AJAX library based on jQuery.ajax",
    long_description = __doc__,
    author = "Slavi Pantaleev",
    author_email = "s.pantaleev@gmail.com",
    url = "https://github.com/spantaleev/sijax-python",
    keywords = ["ajax", "jQuery"],
    platforms = "any",
    license = "BSD",
    zip_safe = False,
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    test_suite='__main__.run_tests'
)
