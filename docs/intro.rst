Introduction to Sijax
=====================

Sijax is a Python/jQuery library designed to help you easily bring ajax to your application.
It uses jQuery.ajax to make AJAX requests, but hides most of the details which you don't care about.

If we think about the way ajax is normally used, we'll see jQuery.ajax calls to certain URIs.
These URIs make sure to return a properly formatted JSON or XML request. A callback function is then
called in your browser, and you go over the result and decide what to do with it.

This sounds extremely inconvenient and painful to do every time.

Sijax is here to offer you an alternative. Let's say that you want to update some news feed element on the page.
What you first need to do is develop a Python function that would handle this specific "page update request".
You can then call that server-side function straight from your browser, with a single line of javascript code.
There's no need for you to return JSON/XML, setup any callbacks, or interpret the jQuery.ajax response.
Sijax does all that for you.

Let's get back to our example. Suppose we want to update a DIV on the page, which has an ID like this::

    <div id="news">.. news items would go here..</div>

We'll use the following javascript code to make our ajax request::

    <script type="text/javascript">
        Sijax.request('update_news');
    </script>

Here's what we've really done so far:

* We've created a page element and assigned an ID to it, so that we can easily update it.
* We've called the ``Sijax.request()`` function from the browser, passing the name of the function we want to handle our request
* Sijax now creates a special request to your Python server


We'll define the following Python function that handles the news feed update
and we'll make it available for calling, by registering it with Sijax::

    def news():
        def update_news(obj_response):
            news = get_latest_news_items()
            news_html = render_news_items(news)

            obj_response.html("#news", news_html)
            obj_response.alert("News feed updated!")

        instance = Sijax()
        instance.set_data(POST_DICTIONARY_HERE)
        instance.register_callback("update_news", update_news)
        if instance.is_sijax_request():
            return instance.process_request()

        # normal page request
        return render_news_page()

Here's what this really does:

* We have defined a response function (a handler) - ``update_news``
* We have created an instance of Sijax
* We have passed the POST data to Sijax, so that it can inspect it and determine if the current request is meant to be handled by Sijax
* We have registered the ``update_news`` function with Sijax. This tells Sijax that the function ``update_news`` is to be exposed for calling from the browser, with the public name of ``update_news``.
* We've detected whether the request is meant to be handled by Sijax. If it is, we're telling Sijax to generate a response, which we return to the browser.

Anyone who's used jQuery would recognize the similar syntax.
The ``obj_response`` object automatically passed to your function is your way of feeding data back to the browser.
Sijax always passes the ``obj_response`` object to your function as its first argument.
It's similar to the way Python passes ``self`` to object methods.

The response object is capable of doing much more than replacing HTML though.
For the full list of currently supported methods it has, take a look at :ref:`available-response-methods`.

The response that Sijax returns is usually a JSON string, which gets passed to your browser. Sijax in the browser reads the response and executes the commands (in order).
The ``obj_response.html("#news", news_html)`` code sort of gets transformed to ``jQuery("#news").html(news_html)``.
