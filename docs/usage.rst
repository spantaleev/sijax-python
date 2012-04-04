.. _usage:

Using Sijax
===========

The **main idea** behind Sijax is **registering/exposing** functions on the server-side and easily **calling** those functions from the browser.

The functions that you expose can be referred to as *Response* functions or *Handler* functions.

All functions receive a response object as their first argument, which is an instance of :class:`sijax.response.BaseResponse`.
The Response function should use that argument to feed data back to the browser. You do that by calling one of the many methods that it provides.


Registering functions
---------------------

To register/expose a function you use the :meth:`sijax.Sijax.register_callback` method:

.. automethod:: sijax.Sijax.register_callback
   :noindex:

Let's take a look at an example function and a way of calling it::

    def index():
        def rate_news_item(obj_response, news_id, stars_count):
            update_news_rating(news_id, stars_count)
            rating = get_new_rating(news_id)

            obj_response.html('#news_rating', rating)
            obj_response.alert('Thanks for voting with %d stars' % stars_count)

        instance = Sijax()
        instance.set_data(POST_DATA_HERE)
        instance.set_request_uri(URI_OF_THE_CURRENT_PAGE)
        instance.register_callback('rate', rate_news_item)
        if instance.is_sijax_request:
            return instance.process_request()

        return render_news_page()

Note that we're registering the ``rate_news_item`` function with the name of ``rate``.
The public name of the function is the one that would be used in the browser to call it.

If we want to call this function now, we can just do::

    <script type="text/javascript">
        var news_id = 324;
        var user_rating = 4;
        Sijax.request('rate', [news_id, stars_count]);
    </script>

The first argument that ``Sijax.request()`` accepts in the browser is the public name of the function to call.
The second argument is an optional array/list of arguments to pass to the Python function.
This ``Sijax.request()`` call rates the news item (with an id of 324) with 4 stars.
To learn more on invoking functions using ``Sijax.request()``, see :ref:`clientside-sijax-request`.

Sijax will update the DOM element which matches the jQuery selector ``#news_rating`` with the new rating value.
It would then show an alert message to the user.



.. _mass-function-registration:

Mass function registration
--------------------------

It's common to have many functions exposed/registered for any page.
As pages grow more and more interactive (and complex) you'll want to be able to register all those different functions in a shorter way.

An easy way to do that is to group related functions inside a class (or a Python module) and tell Sijax that you want to register the whole thing (the whole object).

You do that using :meth:`sijax.Sijax.register_object`:

.. automethod:: sijax.Sijax.register_object
   :noindex:


Here's an example which registers 2 functions with a single call::

    class Handler(object):

        @staticmethod
        def say_hi(obj_response):
            obj_response.alert("Hi!")

        @staticmethod
        def say_hello(obj_response):
            obj_response.alert("Hello!")

    sijax_instance.register_object(Handler)

This is equivalent to registering both functions manually::

    sijax_instance.register_callback('say_hi', Handler.say_hi)
    sijax_instance.register_callback('say_hello', Handler.say_hello)

You can also use a class instance and register all of the object's methods the same way.
You only need to remove the ``@staticmethod`` decorator and do the actual registering like this::

    sijax_instance.register_object(Handler())


Available Response methods
--------------------------

To see the full list of available response methods (like ``alert()`` above), take a look at :ref:`available-response-methods`.


Extending the Response class
----------------------------

If you want to extend the functionality provided by :class:`sijax.response.BaseResponse` you can create your own subclass
and tell Sijax to use it when creating the ``obj_response`` object for a particular function.

Here's an example of a function, which uses a custom response class::

    # Custom Response class, which adds a new shortcut method
    class MyResponse(sijax.response.BaseResponse):
        def say_hello_to(self, name):
            self.alert('Hello %s' % name)

    # The handler function which would use our custom Response class
    def say_hello_handler(obj_response, name):
        obj_response.say_hello_to(name)

    sijax_instance.register_callback('say_hello', say_hello_handler, response_class=MyResponse)


.. _args-extra:

Passing extra arguments (context)
---------------------------------

Sometimes you may want to pass some more special arguments after ``obj_response``, but before the actual call arguments
coming from the browser. Perhaps you've got some data available when you're registering the Sijax function,
which you want to pass along to it (because you may only have a reference to it at the place the handler is registered).

You can use an optional argument when registering the function that tells Sijax what other variables to pass along.

Here's an example::

    # The handler is defined outside the other function
    # so it wouldn't normally be able to access its data
    def say_hello_handler(obj_response, hello_from, hello_to):
        obj_response.alert('Hello from %s to %s' % (hello_from, hello_to))

    # Let's assume that this is the entry point for all page requests
    def index():
        hello_from = get_site_name_from_database()

        sijax_instance = Sijax()
        sijax_instance.set_data(POST_DICTIONARY_HERE)
        sijax_instance.register_callback('say_hello', say_hello_handler, args_extra=[hello_from])
        if sijax_instance.is_sijax_request:
            return sijax_instance.process_request()

        # normal page request (not Sijax)
        return render_page()

You can do extra arguments passing with mass registration too::

    sijax_instance.register_object(SijaxHandler, args_extra=['additional', 'arguments', 'here'])


Events
------

There are certain events that you may be interested in.
Sijax can invoke a handler function for each event that you've "subscribed" to.

The following events are available as seen in the :class:`sijax.Sijax` class:

.. autoattribute:: sijax.Sijax.EVENT_BEFORE_PROCESSING
   :noindex:
.. autoattribute:: sijax.Sijax.EVENT_AFTER_PROCESSING
   :noindex:
.. autoattribute:: sijax.Sijax.EVENT_INVALID_REQUEST
   :noindex:
.. autoattribute:: sijax.Sijax.EVENT_INVALID_CALL
   :noindex:

Events are registered using :meth:`sijax.Sijax.register_event`:

.. automethod:: sijax.Sijax.register_event
   :noindex:

Here are some examples::

    def before_handler(obj_response):
        obj_response.alert('Called before calling the response function!')

    def after_handler(obj_response):
        obj_response.alert('Called after calling the response function!')

    def invalid_request_handler(obj_response, function_name):
        obj_response.alert('%s is an unknown function!' % function_name)

    def invalid_call_handler(obj_response, callback):
        obj_response.alert('The call to %s failed!' % callback.__name__)

    sijax_instance = Sijax()
    sijax_instance.register_event(Sijax.EVENT_BEFORE_PROCESSING, before_handler)
    sijax_instance.register_event(Sijax.EVENT_AFTER_PROCESSING, after_handler)
    sijax_instance.register_event(Sijax.EVENT_INVALID_REQUEST, invalid_request_handler)
    sijax_instance.register_event(Sijax.EVENT_INVALID_CALL, invalid_call_handler)

    # some more initialization code here

    sijax_instance.register_callback('say_hi', lambda r: r.alert('Hi!'))


If a request for ``say_hi`` is made using::

    Sijax.request('say_hi');

The result would be the following 3 alerts in order::

    Called before calling the response function!
    Hi!
    Called after calling the response function!


If a request for ``say_hi`` is made using::

    Sijax.request('say_hi', ['arguments', 'here']);

The result would be the following 3 alerts in order::

    Called before calling the response function!
    The call to say_hi failed!
    Called after calling the response function!

If a request for ``say_hello_instead_of_hi`` is made using::

    Sijax.request('say_hello_instead_of_hi');

The result would be the following 3 alerts in order::

    Called before calling the response function!
    say_hello_instead_of_hi is an unknown function!
    Called after calling the response function!
