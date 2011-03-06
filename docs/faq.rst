.. _faq:

Frequently Asked Questions and Notes
====================================


How light is it?
----------------

The javascript core is less than 3kB in its original form.

Keep in mind that you need jQuery loaded on the page for it to function.
It was tested with jQuery ``1.4`` and ``1.5``, but some older releases should/may also work.


Are there any other dependencies?
---------------------------------

JSON is used for passing messages around, so you'll need Python 2.6+ or Python 2.5 with ``simplejson``.
The package hasn't been tested on Python 2.5 yet though.

JSON is also needed (for encoding messages) in the browser, so browsers having no native JSON support (like IE <= 7) need to load the additional JSON library (3kB).

Sijax will detect such browsers and load the library for them, provided you have pointed to it like so::

    sijax_instance.set_json_uri('{URI TO json2.js}')
    
The ``json2.js`` file is included with this project.

Browsers that do have native JSON support, won't need to load this additional resource.


Is Sijax available for other programming languages?
---------------------------------------------------

Yes.

Sijax was inspired by the Xajax_ library for PHP. It was developed as a simpler, faster and lighter alternative to Xajax for PHP. You can find Sijax for PHP on `GitHub <https://github.com/spantaleev/sijax>`_.

The PHP version of Sijax looks and feels pretty much the same. There are minor differences between the PHP and Python version to make the API better suit each language's unique capabilities.

.. _Xajax: http://xajax-project.org/


Known limitations
-----------------

* Requires jQuery - since most projects probably already use jQuery, this may not be a problem
* Requires JSON - an additional 3kB library has to be loaded (automatically) for IE <= 7


Known issues
------------

* On very rare occasions, empty strings ("") are passed as "null" (affects IE only)
