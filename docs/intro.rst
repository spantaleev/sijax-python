Introduction to Sijax
=====================

Sijax is a Python/`jQuery`_ library designed to help you easily bring ajax to your application.
It uses ``jQuery.ajax`` to make AJAX requests, but hides most of the details which you don't care about.

If we think about the way ajax is normally used, we'll see ``jQuery.ajax`` calls to certain URIs.
These URIs make sure to return a properly formatted JSON or XML request. A callback function is then
called in your browser, and you go over the result and decide what to do with it.

This sounds extremely inconvenient and painful to do every time.

Sijax is here to offer you an alternative. Let's say that you want to update some news feed element on the page.
What you first need to do is develop a Python function that would handle this specific "page update request".
You can then call that server-side function straight from your browser, with a single line of javascript code.
There's no need for you to return JSON/XML, setup any callbacks, or interpret the ``jQuery.ajax`` response.
Sijax does all that for you.

Let's get back to our example.
Suppose we've got the following HTML markup::

    <div id="news">.. news items would go here..</div>

    <script type="text/javascript">
        Sijax.request('update_news');
    </script>

Sijax now creates a special request to your Python server.

We'll define the following Python function that handles the news feed update
and we'll make it available for calling by registering it with Sijax::

    def news():
        def update_news(obj_response):
            news = get_latest_news_items()
            news_html = render_news_items(news)

            obj_response.html("#news", news_html)
            obj_response.alert("News feed updated!")

        instance = Sijax()
        instance.set_data(POST_DICTIONARY_HERE)
        instance.set_request_uri(URI_OF_THE_CURRENT_PAGE)
        instance.register_callback('update_news', update_news)
        if instance.is_sijax_request:
            return instance.process_request()

        # normal page request
        return render_news_page()

Here's what this really does:

* We have defined a response function (a handler) - ``update_news``
* We have initialized Sijax with the POST data, so that it can inspect it and determine if the current request is meant to be handled by Sijax
* We have told Sijax to which request URI to send the requests
* We have registered the ``update_news`` function with Sijax. This tells Sijax that the function ``update_news`` is to be exposed for calling from the browser, with the public name of ``update_news``.
* We've detected whether the request is meant to be handled by Sijax. If it is, we're telling Sijax to process the request.

The ``obj_response`` argument (instance of :class:`sijax.response.BaseResponse`) automatically passed to your function is your way of sending data back to the browser.
Sijax always passes ``obj_response`` as the first argument to your function, much like Python passes ``self`` to object methods.

The response object is capable of doing much more than replacing HTML though.
View the full list of supported methods at :ref:`available-response-methods`.

The response that Sijax returns is usually a JSON string, which gets passed to your browser. Sijax in the browser reads the response and executes the commands (in order).
The ``obj_response.html("#news", news_html)`` code sort of gets transformed to ``jQuery("#news").html(news_html)``.

.. _jQuery: http://jquery.com/
