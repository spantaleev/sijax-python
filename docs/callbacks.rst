Sijax Callbacks (aka Response functions)
========================================

In order to make a function available for calling from the browser, you first need to register it with Sijax.
It needs to know a public name for your function and a reference to it (a callback).

Functions not registered with Sijax will not be handled. Those are known as invalid requests.
There's a special event for handling invalid requests. More on that in ``events.rst``.

There are lots of ways to register functions with Sijax. The simplest (but not really usable) way is to use a lambda::

    sijax_instance.register_callback("say_hi", lambda obj_response: obj_response.alert("Hi!"))


Another way is to use a regular function::

    def function(obj_response):
        obj_response.alert("Hi!")

    sijax_instance.register_callback("say_hi", function)


A more popular approach for sites that need to register many callbacks is to register them all at once with a single call::

    class Handler(object):

        @staticmethod
        def say_hi(obj_response):
            obj_response.alert("Hi!")

        @staticmethod
        def say_hello(obj_response):
            obj_response.alert("Hello!")

    sijax_instance.register_object(Handler)


You can also use a class instance and register all of the object methods the same way.
You only need to remove the ``@staticmethod`` decorator and pass do the actual registering like this::

    sijax_instance.register_object(Handler())


Using Custom Response Objects
-----------------------------

The simplest way of registering a single callback is to pass a public name for it and a callback function.
By doing that, you'll receive a first argument ``obj_response`` (as always) which is an instance of `response.BaseResponse`.

If you want to extend the functionality provided by `response.BaseResponse` you can create your own subclass
and tell Sijax to use your own class when creating the ``obj_response`` object for a particular function.

Here's an example of a function, which uses a custom response object::

    class MyResponse(response.BaseResponse):
        def say_hello_to(name):
            self.alert("Hello %s" % name)

    def say_hello_handler(obj_response, name):
        obj_response.say_hello_to(name)

    sijax_instance.register_callback("say_hello", say_hello_handler, response_class=MyResponse)


Passing some more arguments (context)
-------------------------------------

Sometimes you may want to pass some more special arguments after ``obj_response``, but before the actual arguments
coming from the browser. Perhaps you've got some data available when you're registering the Sijax function,
which you want to pass along to it (because you may have a reference to it at the place the handler is defined).

You can use another optional argument when registering the function that tells Sijax what other variables to pass along
to your function.

Here's an example that resembles more closely the way things actually work in real web apps::

    # the handler is defined outside the other function
    # so it wouldn't normally be able to access its data
    def say_hello_handler(obj_response, hello_from, hello_to):
        obj_response.alert("Hello from %s to %s" % (hello_from, hello_to))

    # let's assume that this is the entry point for all page requests
    def index():
        hello_from = get_site_name_from_database()
        
        sijax_instance = Sijax()
        sijax_instance.set_data(POST_DICTIONARY_HERE)
        sijax_instance.register_callback("say_hello", say_hello_handler, args_extra=[hello_from])
        if sijax_instance.is_sijax_request():
            return sijax_instance.proces_request()

        # normal page request (not Sijax)
        return render_page()

You can do extra arguments passing with mass registration too::

    sijax_instance.register_object(SijaxHandler, arsg_extra=["additional", "arguments", "here"])
