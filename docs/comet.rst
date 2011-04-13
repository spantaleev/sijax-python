.. _comet-plugin:

Comet Plugin
============

Normal Sijax requests are ``jQuery.ajax`` requests which execute and return a single response string in the end.

But what if you need to send some data back, but continue running, before pushing some more, etc.
Imagine a long running task, which does some work, updates a progress bar, does more work, updates the progress bar again
before reaching the end of the job, when it could finally exit.

Without streaming the response to the browser, you'd need to implement that workflow as separate requests.
You may want to call ``do_work_1``, which does a small portion of the work, updates a progress bar and schedules ``do_work2`` to be called.
``do_work2`` does the same, and maybe calls ``do_work3`` after that, etc. That's wasteful, because a lot more requests are created.
It's also wasteful, because all those ``do_workX`` functions probably depend on some common data. They may all need to do a database call to get the object
they're operating on, for example. With 3 requests, we'll have to do the database call in each 3 of them.

Using the Comet plugin
----------------------

To make use of the Comet plugin, you'll need to include the ``sijax_comet.js`` file on your page.

``sijax_comet.js`` can be mirrored to a directory of your choise using :func:`sijax.helper.init_static_path`.

With the Comet plugin your functions can tell Sijax to push (flush) the data to the browser and continue executing.
Here's an example::

    def comet_handler(obj_response):
        # do some work here..
        obj_response.html('#progress', 'Finished work batch 1')
        yield obj_response

        # do some more work here..
        obj_response.html('#progress', 'Finished work batch 2')
        yield obj_response


``yield`` tells Sijax to flush the commands we've queued so far to the browser.
If your Comet function doesn't ``yield`` at all, its response will be returned all at once (in the end),
much like a normal request function (that uses :class:`sijax.response.BaseResponse`).

Let's see how we can register a handler function as a Comet function.

To register Comet function, you need to use the :func:`sijax.plugin.comet.register_comet_callback` registration helper::

    from sijax.plugin.comet import register_comet_callback

    def comet_handler(obj_response):
        obj_response.alert("Comet!")

    # registers comet_handler by the name of "func_name"
    register_comet_callback(sijax_instance, "func_name", comet_handler)

There's a tiny difference in the way Comet functions are called, compared to regular Sijax functions::

    //Regular function call
    Sijax.request('func_name')

    //Comet function call
    sjxComet.request('func_name')


Mass function registration
--------------------------

The :func:`sijax.plugin.comet.register_comet_object` registration helper,
allows you to register several Comet functions all at once (like :ref:`mass-function-registration`)::

    from sijax.plugin.comet import register_comet_object

    class CometHandler(object):
        @staticmethod
        def callback_one(obj_response):
            obj_response.alert("One!")

        @staticmethod
        def callback_two(obj_response):
            obj_response.alert("Two!")

    # registers callback_one and callback_two preserving their names
    register_comet_object(sijax_instance, CometHandler)


The CometResponse object
------------------------

The response object (``obj_response``) for functions registered with Comet is an instance of
:class:`sijax.plugin.comet.CometResponse`, which doesn't provide any more functionality than the default
:class:`sijax.response.BaseResponse` class used for regular functions, apart from the internal changes,
which make streaming possible.


Note on performance with Comet
------------------------------

Long running requests may be handled in a bad way, depending on the framework/server you're using.
It may not be a good idea to have many long running comet requests at the same time.

If you need something with more scalability, you should probably look elsewhere.
The Comet plugin was designed to be very simple and to work everywhere, without nasty hacks and fallback strategies.
Because of that, it uses the most simple way of doing content streaming - using an iframe.
This has downsides of its own, but discussing them is not the purpose of this document.

In conclusion, the Comet plugin should work great for small projects with a low number of concurrent comet requests.
