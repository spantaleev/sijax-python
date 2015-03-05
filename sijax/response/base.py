# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

"""
    sijax.response.base
    ~~~~~~~~~~~~~~~~~~~

    Provides the BaseResponse class, which is the base class
    used to create response objects for Sijax functions.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from builtins import object
from ..helper import json
from ..exception import SijaxError
from types import GeneratorType
from functools import partial


class BaseResponse(object):
    """The response class is the way by which Sijax functions (handlers)
    pass information back to the browser. They do this by calling
    various methods, which queue commands until they're sent to the browser.
    """

    COMMAND_ALERT = 'alert'
    COMMAND_HTML = 'html'
    COMMAND_SCRIPT = 'script'
    COMMAND_ATTR = 'attr'
    COMMAND_CSS = 'css'
    COMMAND_REMOVE = 'remove'
    COMMAND_CALL = 'call'
    #: Options related to the appearance of JSON during communication. By
    #: default the most compact form is chosen.
    JSON_AS_ASCII = False
    JSON_SEPARATORS = (',', ':')
    JSON_INDENT = None
    JSON_SORT_KEYS = False


    def __init__(self, sijax_instance, request_args):
        """Constructs a new empty Sijax Response object.

        The arguments that the sijax function is invoked with are passed,
        so that we can override them if we want.
        We don't need to do that for regular sijax responses,
        but certain plugins may need to do that.

        :param sijax_instance: the Sijax instance object
                               that created this response
        :param request_args: the request arguments that the sijax function
                             was invoked with
        """
        self._commands = []
        self._sijax = sijax_instance
        self._request_args = request_args
        self.dumps = partial(json.dumps, ensure_ascii=self.JSON_AS_ASCII,
                separators=self.JSON_SEPARATORS, indent=self.JSON_INDENT,
                sort_keys=self.JSON_SORT_KEYS)

    def _get_request_args(self):
        """Returns the arguments list to pass to callbacks.

        This class doesn't manipulate them, so it returns the original
        call arguments, but other classes can override them however they need.
        """
        return self._request_args

    def _add_command(self, cmd_type, params = None):
        """Adds a raw command to the buffer to send to the client."""
        if params is None:
            params = {}
        params['type'] = cmd_type

        self._commands.append(params)
        return self

    def clear_commands(self):
        """Clears the commands buffer.

        All the commands added by other methods will be removed.

        Example::

            obj_response.alert('Some alert!')
            obj_response.clear_commands()
            # The alert() above got removed from the commands queue
        """
        self._commands = []
        return self

    def alert(self, message):
        """Sends a ``window.alert`` command to the browser.

        Example that shows a message box::

            obj_response.alert('Alert message!')
        """
        params = {self.__class__.COMMAND_ALERT: message}
        return self._add_command(self.__class__.COMMAND_ALERT, params)

    def _html(self, selector, html, set_type):
        params = {'selector': selector, 'html': html, 'setType': set_type}
        return self._add_command(self.__class__.COMMAND_HTML, params)

    def html(self, selector, html):
        """Assigns the given html value to all elements
        matching the jQuery selector.

        Scripts inside the html block are also executed.

        Same as jQuery's: ``$(selector).html(value)``

        Example which sets a new html value for an element::

            obj_response.html('#element', '<strong>Hey!</strong>')

        :param selector: the jQuery selector for which we'll replace the html
        :param html: the html text
        """
        return self._html(selector, html, 'replace')

    def html_append(self, selector, html):
        """Same as :meth:`sijax.response.BaseResponse.html`,
        but appends instead of assigning a new value.
        """
        return self._html(selector, html, "append")

    def html_prepend(self, selector, html):
        """Same as :meth:`sijax.response.BaseResponse.html`,
        but prepends instead of assigning a new value.
        """
        return self._html(selector, html, 'prepend')

    def script(self, js):
        """Executes the given javascript code.

        Example::

            obj_response.script("alert('Javascript code!');")

        Note that the given javascript code is eval-ed inside a
        Sijax helper function in the browser, so it's not touching
        the global namespace, unless you explicitly do it.
        """
        params = {self.__class__.COMMAND_SCRIPT: js}
        return self._add_command(self.__class__.COMMAND_SCRIPT, params)

    def css(self, selector, property_name, value):
        """Assigns a style property value to all elements
        matching the jQuery selector.

        Same as jQuery's ``$(selector).css('property', 'value')``

        Example which changes the background color of an element::

            obj_response.css('#element', 'backgroundColor', 'red')

        Note that this can only change a single property at once.
        It doesn't support jQuery's mass change which uses a
        key/value map of properties/values to change.

        :param selector: the jQuery selector to invoke css() on
        :param property_name: the name of the style property
        :param value: the new value to assign to the property
        """
        params = {'selector': selector, 'key': property_name, 'value': value}
        return self._add_command(self.__class__.COMMAND_CSS, params)

    def _attr(self, selector, property_name, value, set_type):
        params = {
            'selector': selector, 'key': property_name,
            'value': value, 'setType': set_type
        }
        return self._add_command(self.__class__.COMMAND_ATTR, params)

    def attr(self, selector, property_name, value):
        """Assigns an attribute value to all elements
        matching the jQuery selector.

        Same as jQuery's ``$(selector).attr('property', 'value')``

        Example which changes 2 attributes of a given element::

            obj_response.attr('#element', 'width', '500px')
            obj_response.attr('#element', 'disabled', true)

        :param selector: the jQuery selector to invoke attr() on
        :param property_name: the name of the property
        :param value: the new value to assign to the property
        """
        return self._attr(selector, property_name, value, 'replace')

    def attr_append(self, selector, property_name, value):
        """Same as :meth:`sijax.response.BaseResponse.attr`,
        but appends instead of assigning a new value."""
        return self._attr(selector, property_name, value, 'append')

    def attr_prepend(self, selector, property_name, value):
        """Same as :meth:`sijax.response.BaseResponse.attr`,
        but prepends instead of assigning a new value."""
        return self._attr(selector, property_name, value, 'prepend')

    def remove(self, selector):
        """Removes all elements that match the jQuery selector from the DOM.

        Example which removes all DIV elements from the page::

            obj_response.remove('div')

        Same as jQuery's: ``$(selector).remove()``
        """
        params = {self.__class__.COMMAND_REMOVE: selector}
        return self._add_command(self.__class__.COMMAND_REMOVE, params)


    def redirect(self, uri):
        """Redirects the browser to the given URI.

        Example::

            obj_response.redirect('http://example.com/')

        """
        return self.script('window.location = %s;' % self.dumps(uri))

    def call(self, js_func_name, func_params=None):
        """Calls the given javascript function with the given arguments list.

        Example which calls the browser's ``alert()`` function::

            obj_response.call('alert', ['Message'])

        :param js_func_name: the name of the javascript function to call
        :param func_params: a list of arguments to call the function with
        """
        if func_params is None:
            func_params = []

        if (not isinstance(func_params, list) and
            not isinstance(func_params, tuple)):
            raise SijaxError('call() expects a list, a tuple or '
                             'None for the args list')

        params = {
            self.__class__.COMMAND_CALL: js_func_name,
            'params': func_params
        }
        return self._add_command(self.__class__.COMMAND_CALL, params)

    def _get_json(self):
        """Returns a JSON representation of the commands buffer list.

        The client side code will loop over the list and execute all the
        commands in order.
        """
        return self.dumps(self._commands)

    def _perform_handler_call(self, callback, args):
        """Performs the actual calling of the Sijax handler function.

        If the handler is called in a wrong way (bad arguments),
        the ``EVENT_INVALID_CALL`` event handler will be executed instead.

        Exceptions raised by the Sijax handler function won't be handled.
        """
        try:
            return callback(self, *args)
        except TypeError:
            # This means that the function was called with bad arguments
            # or that the function itself raised a TypeError.
            # We can determine which is it by inspecting the traceback.
            import sys, traceback
            stack_entries = traceback.extract_tb(sys.exc_info()[2])
            if len(stack_entries) != 1:
                # TypeError raised from somewhere within the Sijax handler
                raise
            # Invalid call to the handler (bad arguments)
            evt_invalid_call = self._sijax.__class__.EVENT_INVALID_CALL
            return self._sijax.get_event(evt_invalid_call)(self, callback)

    def _process_callback(self, callback, args):
        """Processes a single callback.

        For normal responses this only means calling the callback,
        because we'll flush the commands to the client once (in the end).

        For other responses (like Comet) though we can flush
        implicitly after every callback.
        """
        response = self._perform_handler_call(callback, args)
        # We usually don't expect a return value,
        # but if we get a generator, it may mean that our regular function
        # was used like a streaming function (yield).
        # This is a a mistake which could happen due to incorrect
        # function registration.
        if isinstance(response, GeneratorType):
            raise SijaxError('Flushing/Yielding/Streaming is not '
                             'supported for regular functions!')

    def _process_call_chain(self, call_chain):
        """Executes all the callbacks in the chain for this response object.

        Each callback in the chain adds commands to the buffer.
        When all the callbacks have been executed, the buffer would contain
        a list of commands that we need to pass to the browser (in order).

        :param call_chain: a list of two-tuples (callback, args list) to call
        :return: JSON string to be passed to the browser
        """
        for callback, args in call_chain:
            self._process_callback(callback, args)
        return self._get_json()

