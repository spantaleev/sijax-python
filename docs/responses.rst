Sijax Responses
===============

A Response function is a function registered with Sijax, meaning it could be invoked from the browser.
Response functions receive a special Response object argument (it's the first argument in the arguments list).

The Response function should use that argument to feed data back to the browser. You do that by calling one of the many methods that it provides.
Sijax takes care of converting all those method calls to commands that your browser would understand and handle.

All functions receive a response object which is an instance of ``response.BaseResponse``.

Functions don't need to return anything. They manipulate the response object passed to them and exit. The rest is behind the scenes magic.

Let's take a look at another example function and a way of calling it::

    def rate_news_item(obj_response, news_id, stars_count):
        update_news_rating(news_id, stars_count)
        rating = get_new_rating(news_id)

        obj_response.html("#news_rating", rating)
        obj_response.alert("Thanks for voting with %d stars" % stars_count)

    instance = Sijax()
    instance.set_data(POST_DATA_HERE)
    instance.register_callback("rate", rate_news_item)
    if instance.is_sijax_request():
        return instance.process_request()

Note that we're registering the ``rate_news_item`` function with the name of ``rate``.
The public name of the function is the one that would be used in the browser to call it.

If we want to call this function now, we can just do::

    <script type="text/javascript">
        var news_id = 324;
        var user_rating = 4;
        Sijax.request('rate', [news_id, stars_count]);
    </script>

The first argument that ``Sijax.request()`` accepts in the browser is the public name of the function to call.
The second argument is an optional array of arguments to pass to the Python function.
This ``Sijax.request()`` call rates the news item (with id of 324) with 4 stars.

Sijax will update the DOM element which matches the jQuery selector ``#news_rating`` with the new rating value.
It would then show an alert message to the user.

``Sijax.request()`` also accepts a third optional (and more advanced) argument,
which can specify some custom options to pass to ``jQuery.ajax``.
You may want to use it to setup call retries, timeouts, etc.
