API
===

Sijax
-----

.. autoclass:: sijax.Sijax
   :members:


.. _available-response-methods:

BaseResponse
------------

.. autoclass:: sijax.response.BaseResponse
   :members:


StreamingIframeResponse
-----------------------

.. autoclass:: sijax.response.StreamingIframeResponse
   :members:


Helpers
-------

.. autofunction:: sijax.helper.init_static_path

Exceptions
----------

.. autoclass:: sijax.exception.SijaxError
   :members:


Comet plugin
------------

.. autofunction:: sijax.plugin.comet.register_comet_callback
.. autofunction:: sijax.plugin.comet.register_comet_object
.. autoclass:: sijax.plugin.comet.CometResponse
   :members:

Also refer to :ref:`clientside-sjxcomet-request` for a way of invoking the :doc:`comet` from the browser.


Upload plugin
-------------

.. autofunction:: sijax.plugin.upload.register_upload_callback

.. autoclass:: sijax.plugin.upload.UploadResponse
   :members:


.. _clientside-sijax-request:

Client side API functions - Sijax.request()
-------------------------------------------

You've got access to only a handful of functions to use on the client side (in the browser).

The most import and frequently used is ``Sijax.request()``, which makes a new Sijax request to the server.

The signature of ``Sijax.request()`` is::

    Sijax.request(function_name, [list of arguments], {additional arguments to jQuery.ajax});

The only required argument is the first one - ``function_name``, which specifies which function you want to call.

If no "list of arguments" is specified, the function will be called with no arguments.

The 3rd parameter you can pass to ``Sijax.request()`` is the most advanced one, which allows you to override some of the
parameters Sijax uses to invoke ``jQuery.ajax()``.

Here are several examples::

    //Calling a function without arguments
    Sijax.request('my_function');

    //Calling a function with a single argument
    Sijax.request('my_function', ['string argument']);

    //Calling a function with 2 arguments
    Sijax.request('my_function', ['argument 1', 'argument 2']);

    //Calling a function with no arguments, telling the underlying
    //jQuery.ajax to use a timeout of 15 seconds
    Sijax.request('my_function', [], {"timeout": 15000});


.. _clientside-sijax-get-form-values:

Client side API functions - Sijax.getFormValues()
-------------------------------------------------

You often need to submit forms without reloading the page. If you want to use Sijax for that,
you would have to extract the fields from the form, create a dictionary and pass that to ``Sijax.request()`` (see :ref:`clientside-sijax-request`).

Sijax provides a browser helper for that called ``Sijax.getFormValues()`` which can extract all the fields from a form on the page and give you a dictionary.

The signature of ``Sijax.getFormValues()`` is::

    Sijax.getFormValues(jQuery_selector);

The result is a dictionary/object representing the names of the fields in the form matched by the selector and their values.

Here's some HTML markup and the result of ``Sijax.getFormValues()``::

    <form id="my_form">
        <input type="text" name="textbox" value="textbox 1" />
        <input type="text" name="tbx[nested]" value="tbx 2" />
        <input type="text" name="textbox2" value="textbox 1" disabled="disabled" />
        <input type="text" value="textbox with no name" />
        <input type="checkbox" name="cbx" checked="checked" />
    </form>

    <script type="text/javascript">
        var values = Sijax.getFormValues('#my_form');
        /*
        The values variable now contains:
        {
            "textbox": "textbox 1",
            "tbx": {"nested": "tbx 2"},
            "cbx": "on"
        }
        */

        Sijax.request('process_form', [values]);
    </script>

In the above example, we've used the ``#my_form`` jQuery selector to find our form, but any other jQuery selector would work.

You can see that the value for ``textbox2`` was skipped, because the field was disabled.
The value for the third text field was also skipped, because the field is missing a name.
If the checkbox were unchecked, it would have been skipped too.


.. _clientside-sjxcomet-request:

Client side API functions - sjxComet.request()
----------------------------------------------

``sjxComet.request()`` is the analogue of ``Sijax.request()`` (see :ref:`clientside-sijax-request`) for Comet functions (see :doc:`comet`).

In order to use this, you'll need to include the ``sijax_comet.js`` file on your page. More on that in :doc:`comet`.

``sjxComet.request()`` has the same signature as ``Sijax.request()`` except that it has **no third parameter** to configure ``jQuery.ajax()``,
because Comet functions don't use AJAX requests.
