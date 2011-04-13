.. _faq:

Frequently Asked Questions and Notes
====================================


How light is it?
----------------

The javascript core is about 4kB in its original form.

Keep in mind that you need jQuery loaded on the page for it to function.
It was tested with jQuery ``1.4`` and ``1.5``, but some older releases may also work.


Are there any other dependencies?
---------------------------------

JSON is used for passing messages around, so you'll need Python 2.6+ or Python 2.5 with ``simplejson``.

JSON is also needed (for encoding messages) in the browser, so browsers having no native JSON support (like IE <= 7) need to load the additional JSON library (3kB).

Sijax will detect such browsers and load the library for them, provided you have pointed to it like so::

    sijax_instance.set_json_uri('{URI TO json2.js}')

The ``json2.js`` file is included with this project.

Browsers that do have native JSON support won't need to load this additional resource.


Is Sijax available for other programming languages?
---------------------------------------------------

Yes.

Sijax was inspired by the Xajax_ library for PHP. It was developed as a simpler, faster and lighter alternative to Xajax for PHP. You can find Sijax for PHP on `GitHub <https://github.com/spantaleev/sijax>`_.

The PHP version of Sijax looks and feels pretty much the same as the Python verson.
There are minor differences between them to make the API better suit each language's unique capabilities.

.. _Xajax: http://xajax-project.org/


Are there any implementation examples I can look at?
----------------------------------------------------

Yes.

You can look at the examples that go with the `Flask-Sijax`_ extension for
the `Flask`_ microframework.

Things are slightly different, because the extension simplifies
usage by doing some of the work for you, but you can still see
what's possible.

.. _Flask: http://flask.pocoo.org/
.. _Flask-Sijax: http://packages.python.org/Flask-Sijax/#examples


Known limitations
-----------------

* Requires `jQuery`_ - since most projects probably already use jQuery, this may not be a problem
* Requires JSON in the browser - an additional 3kB library has to be loaded (happens automatically) for IE <= 7

.. _jQuery: http://jquery.com/
