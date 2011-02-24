Comet Plugin
============

Normal Sijax requests are jQuery.ajax requests which execute and return a single response string in the end.

But what if you need to send some data back, but continue running, before pushing some more, etc.
Imagine a long running task, which does some work, updates a progress bar, does more work, updates the progress bar again
before reaching the end, when it exits.

Without streaming the response to the browser, you'd need to implement that workflow as separate requests.
You may want to call ``do_work_1``, which does a small portion of the work, updates a progress bar and schedules ``do_work2`` to be called.
``do_work2`` does the same, and maybe calls ``do_work3`` after that, etc. That's wasteful, because a lot more requests are created than really needed.
It's also wasteful, because all those ``do_workX`` functions probably depend on some common data. They may all need to do a database call to get the object
they're operating on, for example. With 3 requests, we'll have to do the database call in each 3 of them.

With Comet, you get the shared data at the top, do a portion of your work and tell Sijax to send the data to the browser::

    def comet_handler(obj_response):
        # do some work here..
        obj_response.html("#progress", "Finished with work batch 1")
        yield obj_response

        # do some more work here..
        obj_response.html("#progress", "Finished with work batch 2")
        yield obj_response


``yield`` tells Sijax to flush the commands we've queued so far in the response object (``obj_response``).
If your Comet function doesn't ``yield`` at all, it's response will be returned all at once (in the end),
much like a normal request function (that uses `response.BaseResponse`).

Let's see how we can register a handler function as a Comet function. If you don't do something special over
regular function registrations, you'll end up with a regular function, which can't use yield!

All you need to to register a Comet function is to use the registration helper function that Comet provides::

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

There's also a mass registration helper function::

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


The response object
-------------------

The response object (``obj_response``) for functions registered with Comet is an instance of
`sijax.plugin.comet.CometResponse`, which doesn't provide any more functionality than the default
`sijax.response.BaseResponse` class used for regular functions, apart from the internal changes,
which make streaming possible.


Note on performance with Comet
------------------------------

Long running requests may be handled in a bad way, depending on the framework/server you're using.
It may not be a good idea to have many long running comet requests at the same time.

If you really need something with more scalability, you should probably look elsewhere.
The Comet plugin was designed to be very simple and to work everywhere, without nasty hacks and fallback strategies.
Because of that, it uses the most simple way of doing content streaming - using an iframe. This has downsides of its own,
but discussing them is not the purpose of this document.

In conclusion, the Comet plugin should work great for small projects with a low number of concurrent comet requests.
