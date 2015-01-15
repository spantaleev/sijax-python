# -*- coding: utf-8 -*

from __future__ import (absolute_import, unicode_literals)

"""
    sijax.core
    ~~~~~~~~~~

    Implements the main Sijax class, an instance of which is used to
    register callbacks, invoke callbacks, setup events handlers, etc.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""

from builtins import str
from .helper import json
from .response.base import BaseResponse
from .exception import SijaxError

class Sijax(object):
    """The main Sijax object is what manages function registration and calling.

    Sijax initialization usually looks like this::

        instance = Sijax()
        instance.set_data(POST_DICTIONARY_HERE)
        instance.set_request_uri(URI_TO_SEND_REQUESTS_TO)
        instance.register_callback('function_name', some_function)

    Sijax needs the POST parameters for the current request, to determine
    whether the request is meant to be handled by Sijax or by your regular
    page loading logic.

    Sijax needs a request URI to tell the client where to
    send the ajax requests.
    This is usually the current request URI, but another URI can also be used.

    Functions that are registered (using :meth:`sijax.Sijax.register_callback`
    or :meth:`sijax.Sijax.register_object`) are the only functions exposed to the
    browser for calling.
    """

    PARAM_REQUEST = 'sijax_rq'
    PARAM_ARGS = 'sijax_args'

    #: Event called immediately before calling the response function.
    #: The event handler function receives the Response object argument.
    EVENT_BEFORE_PROCESSING = 'before_processing'

    #: Event called immediately after calling the response function.
    #: The event handler function receives the Response object argument.
    EVENT_AFTER_PROCESSING = 'after_processing'

    #: Event called when the function to be called is unknown
    #: (not registered with Sijax).
    #: The event handler function receives the Response object argument
    #: followed by the public name of the function that was
    #: supposed to be called.
    EVENT_INVALID_REQUEST = 'invalid_request'

    #: Event called when the function was called in a wrong way
    #: (bad arguments count).
    #: The event handler function receives the Response object argument
    #: followed by the callback function that was not called correctly.
    EVENT_INVALID_CALL = 'invalid_call'

    #: An option when registering callbacks that stores the callback function
    PARAM_CALLBACK = 'callback'

    #: An option when registering callbacks that allows the response class to
    #: be changed from :class:`sijax.response.BaseResponse` to something else.
    PARAM_RESPONSE_CLASS = 'response_class'

    #: An option when registering callbacks that makes certain extra arguments
    #: be passed automatically to the response function after the
    #: obj_response argument and before the other arguments
    PARAM_ARGS_EXTRA = 'args_extra'

    def __init__(self):
        cls = self.__class__

        #: Would contain the request data (usually POST)
        self._data = {}

        #: Would contain the callbacks (name => dictionary of params)
        self._callbacks = {}

        #: Stores the various event callbacks
        self._events = {}

        #: The URI where the client should send ajax requests to
        self._request_uri = None

        #: The URI to json2.js or similar to provide JSON support
        #: for browsers that don't have it.. Sijax would load this on demand
        self._json_uri = None

        #: Stores a cached version of the arguments
        #: to be passed to the requested function
        self._request_args = None

        def invalid_request(obj_response, func_name):
            """Handler to be called when an unknown function is called."""
            msg = 'The action you performed is unavailable! (Sijax error)'
            obj_response.alert(msg)

        def invalid_call(obj_response, callback):
            """Handler to be called when a function is called the wrong way."""
            msg = 'You tried to perform an action in a wrong way! (Sijax error)'
            obj_response.alert(msg)

        # Register the before/after processing events
        # to not do anything by default
        self.register_event(cls.EVENT_BEFORE_PROCESSING, lambda r: r)
        self.register_event(cls.EVENT_AFTER_PROCESSING, lambda r: r)

        # Register the "error" events to show some alerts by default
        self.register_event(cls.EVENT_INVALID_REQUEST, invalid_request)
        self.register_event(cls.EVENT_INVALID_CALL, invalid_call)

    def set_data(self, data):
        """Sets the incoming data dictionary (usually POST).

        Sijax needs this data to determine if the current request
        is a Sijax request, and which callback should be called
        with what arguments.
        """
        self._data = data
        self._request_args = None # cache invalidation
        return self

    def get_data(self):
        """Returns the incoming data array that the current instance uses."""
        return self._data

    def register_callback(self, public_name, callback, response_class=None,
                          args_extra=None):
        """Registers the specified callback function with the given name.

        Example::

            def handler(obj_response):
                pass

            # Exposing the same function by 2 different names
            instance.register_callback('test', handler)
            instance.register_callback('test2', handler)

        The optional ``response_class`` parameter could be used to substitute the
        :class:`sijax.response.BaseResponse` class used by default.
        An instance of ``response_class`` is passed automatically
        as a first parameter to your response function (``obj_response``).

        Example::

            def handler(obj_response):
                pass

            class MyResponse(sijax.response.BaseResponse):
                pass

            # `obj_response` passed to `handler` will be an instance of MyResponse
            instance.register_callback('test', handler, response_class=MyResponse)

        The optional ``args_extra`` parameter allows you to pass a list of
        extra arguments to your response function, immediately after
        the ``obj_response`` argument and before the other call arguments.

        Example::

            def handler(obj_response, arg1, arg2, arg3):
                # arg1 = 'arg1'
                # arg2 = 'arg2'
                # arg3 - expected to come from the browser
                pass

            instance.register_callback('test', handler, args_extra=['arg1', 'arg2'])

        :param public_name: the name with which this function will be
                            exposed in the browser
        :param callback: the actual function to call
        :param response_class: the response class, an instance of which to use
                               instead of :class:`sijax.response.BaseResponse`
        :param args_extra: an optional list of additional arguments to pass
                           after the response object argument and before the
                           other call arguments
        """
        if response_class is None:
            response_class = BaseResponse
        if not hasattr(response_class, '__call__'):
            raise SijaxError('response_class needs to be a callable!')

        if args_extra is None:
            args_extra = []
        else:
            if isinstance(args_extra, tuple):
                args_extra = list(args_extra)
            elif not isinstance(args_extra, list):
                raise SijaxError('args_extra could only be a tuple or a list!')

        params = {}
        params[self.__class__.PARAM_CALLBACK] = callback
        params[self.__class__.PARAM_RESPONSE_CLASS] = response_class
        params[self.__class__.PARAM_ARGS_EXTRA] = args_extra

        self._callbacks[public_name] = params
        return self

    def register_object(self, obj, **options):
        """Registers all "public" callable attributes of the given object.

        The object could be anything (module, class, class instance, etc.)

        :param obj: the object whose callable attributes to register
        :param options: the options to be sent to
                        :meth:`sijax.Sijax.register_callback`
        """
        for attr_name in dir(obj):
            if attr_name.startswith('_'):
                continue

            attribute = getattr(obj, attr_name)
            if hasattr(attribute, '__call__'):
                self.register_callback(attr_name, attribute, **options)

    @property
    def is_sijax_request(self):
        """Tells whether this page request looks like
        a valid request meant to be handled by Sijax.

        Even if this is a Sijax request, this doesn't mean it's a valid one.
        Refer to :meth:`sijax.Sijax.process_request` to see what happens when
        a request for an unknown function was made.
        """
        for k in (self.__class__.PARAM_REQUEST, self.__class__.PARAM_ARGS):
            if k not in self._data:
                return False
        return True

    @property
    def requested_function(self):
        """The name of the requested function,
        or None if the current request is not a Sijax request."""
        request = self.__class__.PARAM_REQUEST
        return str(self._data[request]) if request in self._data else None

    @property
    def request_args(self):
        """The arguments list, that the function was called with
        in the browser.

        It should be noted that this is not necessarily the arguments list
        that the callback function will actually receive.
        Custom Response objects are allowed to override the arguments list.
        """
        key_args = self.__class__.PARAM_ARGS
        if self._request_args is None:
            # no precached version.. cache it now
            self._request_args = []
            if key_args in self._data:
                try:
                    args = json.loads(self._data[key_args])
                    if isinstance(args, list):
                        self._request_args = args
                except (ValueError):
                    pass
        return self._request_args

    def process_request(self):
        """Executes the Sijax request and returns the response.

        Make sure that the current request is a Sijax request,
        using :attr:`sijax.Sijax.is_sijax_request` before calling this.
        A :class:`sijax.exception.SijaxError` will be raised,
        if this method is called for non-Sijax requests.

        If the function that was called from the browser is not
        registered (the function is unknown to Sijax),
        the :attr:`sijax.Sijax.EVENT_INVALID_REQUEST` event handler will
        be called instead.

        Refer to :meth:`sijax.Sijax.execute_callback` to see how the main
        handler is called and what the response (return value) is.
        """
        if not self.is_sijax_request:
            raise SijaxError('You should not call this for non-Sijax requests!')

        function_name = self.requested_function
        if function_name in self._callbacks:
            options = self._callbacks[function_name]
            args = self.request_args
        else:
            # Function not registered.. Let's call the invalid request handler
            # passing to it the function name that should've been called
            args = [function_name]
            callback = self._events[self.__class__.EVENT_INVALID_REQUEST]
            options = {self.__class__.PARAM_CALLBACK: callback}

        return self.execute_callback(args, **options)

    def execute_callback(self, args, callback, **params):
        """Executes the given callback function and returns a response.

        Before executing the given callback, the
        :attr:`sijax.Sijax.EVENT_BEFORE_PROCESSING` event callback is fired.
        After executing the given callback, the
        :attr:`sijax.Sijax.EVENT_AFTER_PROCESSING` event callback is fired.

        The returned result could either be a string (for regular functions)
        or a generator (for streaming functions like Comet or Upload).

        :param args: the arguments list to pass to the callback
        :param callback: the callback function to execute
        :param options: more options - look at
                                       :meth:`sijax.Sijax.register_callback`
                                       to see what else is available
        :return: string for regular callbacks or generator for streaming callbacks
        """
        cls = self.__class__

        # Another response class could be used to extend behavior
        response_class = BaseResponse
        if cls.PARAM_RESPONSE_CLASS in params:
            response_class = params[cls.PARAM_RESPONSE_CLASS]

        args_extra = []
        if cls.PARAM_ARGS_EXTRA in params:
            args_extra = params[cls.PARAM_ARGS_EXTRA]

        if not hasattr(callback, '__call__'):
            raise SijaxError('Provided callback is not callable!')

        # Pass the original call args to the response and get them back later
        # This allows the response class (potentially custom)
        # to override the arguments list.
        # Note that we're not passing args_extra to it, as we don't
        # want responses to know anything about that.
        obj_response = response_class(self, args)
        call_args = args_extra + obj_response._get_request_args()

        call_chain = [
            (self._events[cls.EVENT_BEFORE_PROCESSING], []),
            (callback, call_args),
            (self._events[cls.EVENT_AFTER_PROCESSING], [])
        ]
        return obj_response._process_call_chain(call_chain)

    def register_event(self, event_name, callback):
        """Register a callback function to be called when the event occurs.

        Only one callback can be executed per event.

        The provided ``EVENT_*`` constants should be used
        for handling system events.
        Additionally, you can use any string to define your
        own events and callbacks.

        If more than one handler per event is needed, you can chain them
        manually, although it's not recommended.
        """
        self._events[event_name] = callback
        return self

    def has_event(self, event_name):
        """Tells whether we've got a registered event by that name."""
        return event_name in self._events

    def get_event(self, event_name):
        """Returns the event handler callback for the specified event."""
        return self._events[event_name] if event_name in self._events else None

    def set_request_uri(self, uri):
        """Specifies the URI where ajax requests will be sent to
        by the client.

        This is usually the URI of the current request.
        """
        self._request_uri = uri
        return self

    def set_json_uri(self, uri):
        """Sets the URI to an external JSON library,
        for browsers that do not support native JSON (such as IE <= 7).

        If this is not specified, Sijax will not work at all in such browsers.

        The script will only be loaded if a browser
        without JSON support is detected.
        """
        self._json_uri = uri
        return self

    def get_js(self):
        """Returns the javascript code needed to prepare the
        Sijax environment in the browser.

        Note that the javascript code is unique and cannot be shared between
        different pages.
        """
        if self._request_uri is None:
            raise SijaxError('Trying to get the sijax js, '
                             'but no request_uri has been set!')

        js = 'Sijax.setRequestUri(%s);' % json.dumps(self._request_uri)
        if self._json_uri is not None:
            js += 'Sijax.setJsonUri(%s);' % json.dumps(self._json_uri)
        return js

