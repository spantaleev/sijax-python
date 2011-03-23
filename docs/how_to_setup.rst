How to setup Sijax for your project
===================================

To get started with Sijax, you'll first need to install the Sijax_ Python library.
It has no dependencies, so it should be very easy to do.

Instead of using the Sijax library directly, you may want to look for an extension
to your framework that adds Sijax support.

A Sijax extension for the `Flask microframework <http://flask.pocoo.org>`_ is available (`Flask-Sijax`_).
Extensions for other frameworks may appear in the future.

If you find such an extension, you should take a look at the setup docs for it instead.

What follows is an overview of how all things stick together and how you can integrate Sijax (hopefully) everywhere.


Installing
----------

Sijax is available on PyPI_ and can be installed using **pip** or **easy_install**::

    pip install sijax

or::

    easy_install sijax


Javascript files
----------------

Any page that needs to use Sijax will need to include a supported version of the jQuery_ library.

The ``sijax.js`` file also needs to be loaded. The file is available with the source distribution in the ``js`` directory.

You can easily mirror all Sijax static files to a directory of your choice using :func:`sijax.helper.init_static_path`.

Once you've located the ``sijax.js`` file in a web-accessible directory you need to include it on your page like this::

    <script type="text/javascript" src="/static/jquery.js"></script>
    <script type="text/javascript" src="/static/sijax.js"></script>


Server side initialization code
-------------------------------

There's some common Sijax initialization code on the Python side that prepares the environment::

    from sijax import Sijax

    sijax_instance = Sijax()

    # POST_DATA should be a dictionary of POST parameters
    # Sijax uses POST data to pass information around
    sijax_instance.set_data(POST_DATA)

    # The URL where requests originating from this page should be sent to.
    # Most commonly, this is the URL of the current page.
    # Use your framework's functionality to determine what it is.
    sijax_instance.set_request_uri(current_page_url)

    # Make the sijax_instance object available globally (or a proxy to it),
    # so that new functions could be registered

    # Read about this in the next section
    js = sijax_instance.get_js()


Javascript initialization code
------------------------------

After the ``sijax.js`` file has been loaded, the browser initialization code needs to be executed.

Sijax generates that javascript code dynamically (on every page request) using :func:`sijax.Sijax.get_js`::

    javascript_code = sijax_instance.get_js()

Put that code somewhere on your page (but after ``sijax.js`` has been loaded).
The code would look something like this::

    Sijax.setRequestUri('http://example.com/send_requests_for_the_current_page_here');


Start using it
--------------

Now that Sijax has been initialized, you can start using it from your normal request handling functions::

    # We're assuming this is executed when a request to `http://example.com/` is made.
    # It's very important that POST requests are permitted to this URL/handler,
    # because Sijax relies on POST to work.
    # Some frameworks (like Flask) don't permit POST requests by default.
    def index():
        def func(obj_response):
            obj_response.alert('Sijax works!')

        # sijax_instance is an initialized instance of `sijax.Sijax`
        sijax_instance.register_callback('func', func)
        if sijax_instance.is_sijax_request:
            # Valid Sijax request found.
            # Tell Sijax to execute the function that was called,
            # and return the response to the browser
            return sijax_instance.process_request()

        # non-Sijax request.. render regular page here
        # don't forget to load the javascript files
        # and the javascript initialization code
        return render_page()


Note on browsers that don't support native JSON
-----------------------------------------------

Since Sijax relies on JSON to pass messages around, it won't work by default on browsers that don't support JSON natively.
Fixing this requires one more line of code during the server-side initialization step::

    # Fix the path to json2.js!
    sijax_instance.set_json_uri('http://example.com/static/json2.js')

This tells Sijax to load the ``json2.js`` file from the given URI, for browsers that doesn't support JSON natively.
If a browser that supports JSON natively is found, no additional files are loaded.

The ``json2.js`` file is distributed with this project.

You can easily mirror all Sijax static files to a directory of your choice using :func:`sijax.helper.init_static_path`.


Note on the response result
---------------------------

``sijax_instance.process_request()`` is what calls your registered callback, passing the proper instance of the response class
to it as its first argument.

Your handler function calls methods on that response object, which queue commands (like ``html()``, ``css()``, etc).
When your handler function exits those queued commands are represented as JSON and returned as a string.
This means that ``sijax_instance.process_request()`` returns **a string** (valid JSON) for normal handler functions that use the
default :class:`sijax.response.BaseResponse` class.

If the :doc:`comet` or :doc:`upload` is used, it does something else though.
Comet is implemented using an iframe and doesn't use XHR requests (``jQuery.ajax``).
The purpose of the Comet plugin is to allow you to push some commands to the browser without exiting the handler,
do some more work, push some more commands, as many times as you want until you finally exit the handler function.

This means that it can't return a single string once. It needs to push (flush) the data several times, whenever you tell it to.
That's why such handler functions return a **generator object** instead. You can flush the data to the browser on each iteration.
Each iteration's data is **a string**, but it's **not JSON** - it's HTML markup (that includes javascript script tags).

.. _Sijax: http://pypi.python.org/pypi/Sijax/
.. _Flask-Sijax: http://pypi.python.org/pypi/Flask-Sijax/
.. _PyPI: http://pypi.python.org/pypi/Sijax/
.. _jQuery: http://jquery.com/
