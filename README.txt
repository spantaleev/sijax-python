Sijax - a Python/jQuery ajax library
####################################

Sijax stands for "Simple ajax" and provides just that.
It's a simple Python/jQuery library providing easy ajax integration for python web apps.

The main idea is to use javascript code that calls server-side callbacks, which generate a response (manipulating the DOM, etc) and pass it back to the client.
This way, you don't need to manually dispatch ajax requests to certain URIs and go over each XML/JSON response manually.

Sijax was initially developed for PHP, inspired by the `Xajax <http://xajax-project.org/>`_ library (PHP-only).

There are sample files in ``Sijax/examples`` that demonstrate how it can be used.


How does it work?
-----------------

Sijax lets you register any callable (simple function, static class method, object method or lambda) to be called from the client (browser) using javascript like this::

    Sijax.request('my_function', ['argument 1', 15.84]);

Ajax support is provided by `jQuery <http://jquery.com/>`_ at the low-level. Sijax only handles dispatching the correct registered function on the server, and interpreting the response.

A registered function may be referred to as response function. It gets triggered with a javascript call, and receives a ``Response object`` as its first argument.

By calling different methods on the ``Response object`` the response function talks back to the browser.
Here's how the ``my_function`` implementation might look on the Python side::

    def my_function(obj_response, message, double):
        obj_response.alert("Argument 1 is %s" % message)

Once the response function exits, the ``queued commands`` (like ``alert()``, or any other method called on the response object) would be send to the browser and executed there.

The ``alert()`` from the above example shows an annoying alert window in the browser.


What response functions are available?
--------------------------------------

- ``alert(message)`` - shows the alert message
- ``html(selector, html)`` - sets the given ``html`` to all elements matching the jQuery selector ``selector``
- ``html_append(selector, html)`` - same as ``html()``, but appends html instead of setting the new html
- ``html_prepend(selector, html)`` - same as ``html()``, but prepends html instead of setting the new html
- ``attr(selector, property, value)`` - changes the ``property`` to ``value`` for all elements matching the jQuery selector ``selector``
- ``attr_append(selector, property, value)`` - same as ``attr()``, but appends to the property value, instead of setting a new value
- ``attr_prepend(selector, property, value)`` - same as ``attr()``, but prepends to the property value, instead of setting a new value
- ``css(selector, property, value)`` - changes the style ``property`` to ``value`` for all elements matching the jQuery selector ``selector``
- ``script(javascript)`` - executes the given ``javascript`` code
- ``remove(selector)`` - removes all DOM elements matching the selector
- ``redirect(url)`` - redirects the browser to the given ``url``
- ``call(function, args_list)`` - calls a javascript function named ``function``, passing the given arguments to it

Here's an example on how to use some of them::

    def my_function(obj_response, message, double):
        # Supposing we have: `<div id="message-container"></div>`
        obj_response.html('#message-container', message)

        # Supposing we have: `<input type="text" id="total-sum" />`
        obj_response.attr('#total-sum', 'value', double * 4)
    
        obj_response.alert('Sum was calculated!')
    
        # Let's remove all DIVs and the input box now
        obj_response.remove('div').remove('#total-sum')
    
        obj_response.alert('Redirecting you..')

        # Let's redirect the user away
        obj_response.redirect('http://github.com/')


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
    
The ``json2.js`` file is also hosted with this project, and can be found in the ``js/`` directory.

Browsers that do have native JSON support, won't need to load this additional resource.


Known limitations
-----------------

- Requires jQuery - since most projects probably already use jQuery, this may not be a problem
- Requires JSON - an additional 3kB library has to be loaded (automatically) for IE <= 7


Known issues
------------

- On rare occasions, empty strings ("") are passed as "null" (affects IE only)


Do you support comet?
---------------------

Yes, comet streaming is supported via the comet plugin. You can look at ``examples/comet.py`` for more details.

We only provide a very simple implementation (using a hidden iframe), because it works in all browsers and that's probably all that's needed for simple streaming usage.

If you need to get serious with long running requests and lots of concurrent users, you should look into other implementations.


What other plugins are available?
---------------------------------

2 plugins come built-in. These are:

- Comet plugin - allows you to send some commands to the browser and continue running your php response function, before sending some more, etc.
- Upload plugin - allows you to convert any simple upload form to an ajax-enabled one

There are demos in the ``examples`` directory for all plugins.

