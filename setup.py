from setuptools import setup, find_packages


def run_tests():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    from sijax_tests import suite
    return suite()


setup(
    name = "Sijax",
    packages = find_packages(),
    version = "0.1.0",
    description = "An easy to use AJAX library based on jQuery.ajax",
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
