# -*- coding: utf-8 -*-

"""
    sijax.response.BaseResponse
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Provides the BaseResponse class, which is the default class
    used to create response objects from for regular Sijax functions.
    The response class is the way for Sijax functions (handlers) to
    pass information back to the browser. They do this by calling
    various methods, which queue commands until they're sent to the browser.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from ..helper import json
from ..exception import SijaxError
from types import GeneratorType


class BaseResponse(object):
    
    COMMAND_ALERT = 'alert'
    COMMAND_HTML = 'html'
    COMMAND_SCRIPT = 'script'
    COMMAND_ATTR = 'attr'
    COMMAND_CSS = 'css'
    COMMAND_REMOVE = 'remove'
    COMMAND_CALL = 'call'
    
    def __init__(self, sijax_instance, request_args):
        """Constructs a new empty Sijax Response object.

        The arguments that the sijax function is invoked with are passed,
        so that we can override them if we want.
        We don't need to do that for regular sijax responses,
        but certain plugins may need to do that.

        :param sijax_instance: the Sijax instance object that created this response
        :param request_args: the request arguments that the sijax function
                             was invoked with
        """
        self._commands = []
        self._sijax = sijax_instance
        self._request_args = request_args
    
    @property
    def request_args(self):
        """Returns the arguments array to pass to callbacks.

        This class doesn't manipulate them, so it returns the original arguments,
        but other classes can override them however they need.
        """
        return self._request_args
        
    def add_command(self, cmd_type, params = None):
        """Adds a raw command to the buffer to send to the client.

        You generally don't need to use this at all,
        unless you really know what you're doing.
        """
        if params is None:
            params = {}
        params['type'] = cmd_type
        
        self._commands.append(params)
        return self
    
    def clear_commands(self):
        """Clears the commands buffer."""
        self._commands = []
        return self

    def alert(self, message):
        """Sends a window.alert command to the browser."""
        params = {self.__class__.COMMAND_ALERT: message}
        return self.add_command(self.__class__.COMMAND_ALERT, params)
    
    def _html(self, selector, html, set_type):
        params = {"selector": selector, "html": html, "setType": set_type}
        return self.add_command(self.__class__.COMMAND_HTML, params)
   
    def html(self, selector, html):
        """
        Adds the given html to the element specified by the selector,
        replacing any html content inside it.

        Scripts inside the html block are also executed.

        :param selector: the jQuery selector for which we'll replace the html
        :param html: the html text
        """
        return self._html(selector, html, "replace")

    def html_append(self, selector, html):
        """Appends the given html to the element specified by the selector.

        Scripts inside the html block are also executed.

        :param selector: the jQuery selector to append html to
        :param html: the html text
        """
        return self._html(selector, html, "append")
   
    def html_prepend(self, selector, html):
        """Prepends the given html to the element specified by the selector.

        Scripts inside the html block are also executed.

        :param selector: the jQuery selector to prepend html to
        :param html: the html text
        """
        return self._html(selector, html, "prepend")
    
    def script(self, js):
        """Executes the given javascript code.

        Note that the given javascript code is eval-ed inside a
        Sijax helper function, so it's not touching the global namespace,
        unless you explicitly do it.
        """
        params = {self.__class__.COMMAND_SCRIPT: js}
        return self.add_command(self.__class__.COMMAND_SCRIPT, params)

    def css(self, selector, property_name, value):
        """Assigns a new style property value to all elements matching the selector.

        Finds an element by the specified selector and changes
        the specified css (style) property to the given value.
        Same as jQuery's $(selector).css('property', 'value');

        Note that this can only change a single property at once.
        It doesn't support jQuery's mass change which uses a
        key/value map of properties/values to change.

        :param selector: the jQuery selector to invoke css() on
        :param property_name: the name of the style property
        :param value: the new value to assign to the property
        """
        params = {"selector": selector, "key": property_name, "value": value}
        return self.add_command(self.__class__.COMMAND_CSS, params)

    def _attr(self, selector, property_name, value, set_type):
        params = {
            "selector": selector, "key": property_name,
            "value": value, "setType": set_type
        }
        return self.add_command(self.__class__.COMMAND_ATTR, params)

    def attr(self, selector, property_name, value):
        """Assigns an attribute value to all elements matching the selector.

        Finds an element by the specified selector and changes
        the specified property to the given value.
        Same as jQuery's $(selector).attr('property', 'value');

        :param selector: the jQuery selector to invoke attr() on
        :param property_name: the name of the property
        :param value: the new value to assign to the property
        """
        return self._attr(selector, property_name, value, "replace")
    
    def attr_append(self, selector, property_name, value):
        """Same as attr(), but appends instead of assigning a new value."""
        return self._attr(selector, property_name, value, "append")

    def attr_prepend(self, selector, property_name, value):
        """Same as attr(), but prepends instead of assigning a new value."""
        return self._attr(selector, property_name, value, "prepend")
    
    def remove(self, selector):
        """Removes all elements from the DOM that match the selector."""
        params = {self.__class__.COMMAND_REMOVE: selector}
        return self.add_command(self.__class__.COMMAND_REMOVE, params)

    
    def redirect(self, uri):
        """Redirects the browser to the given URI."""
        return self.script("window.location = %s;" % json.dumps(uri))
    
    def call(self, js_func_name, func_params=None):
        """Calls the given javascript function with the given arguments list.

        :param js_func_name: the name of the javascript function to call
        :param func_params: a list of arguments to call the function with
        """
        if func_params is None:
            func_params = []

        if not isinstance(func_params, list) and not isinstance(func_params, tuple):
            raise SijaxError("call() expects a list, a tuple or None for the args list")

        params = {self.__class__.COMMAND_CALL: js_func_name, "params": func_params}
        return self.add_command(self.__class__.COMMAND_CALL, params)
    
    def get_json(self):
        """Returns a JSON representation of the commands buffer list.

        The client side code will loop over the list and execute all the
        commands in order.
        """
        return json.dumps(self._commands)
    
    def _process_callback(self, callback, args):
        """Processes a single callback.

        For normal responses this only means calling the callback,
        because we'll flush the commands to the client once (in the end).

        For other responses (like Comet) though we can flush implicitly after
        every callback.
        """

        try:
            result = callback(self, *args)
        except TypeError:
            # we should re-raise the exception if it's coming
            # from within the function, meaning calling works.. @todo
            event_invalid_call = self._sijax.__class__.EVENT_INVALID_CALL
            self._sijax.get_event(event_invalid_call)(self, callback)
        else:
            # We usually don't expect a return value, but if we get a generator
            # it means that our regular function was used as a streaming function -
            # a mistake which could happen due to incorrect function registration
            if isinstance(result, GeneratorType):
                raise SijaxError('Flushing/Yielding/Streaming is not supported for regular functions!')

    def _process_call_chain(self, call_chain):
        """Executes all the callbacks in the chain for this response object.

        Each callback in the chain adds commands to the buffer.
        When all the callbacks have been executed, the buffer contains a list of commands
        that we need to pass to the browser (in order).

        The result of this is a JSON string to pass to the browser.

        :param call_chain: a list of two-tuples (callback, args list) to call
        """
        for callback, args in call_chain:
            self._process_callback(callback, args)
        return self.get_json()

