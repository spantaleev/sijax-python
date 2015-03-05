# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

"""
    sijax.response.streaming
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Provides a response class to be used when Sijax functions
    are invoked using a form submitted to an iframe,
    instead of XHR (``jQuery.ajax``).
    The main difference from the BaseResponse class is that this one
    can do streaming, meaning it can flush the commands queue back to
    the browser at any time.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from builtins import next
from .base import BaseResponse
from types import GeneratorType


class StreamingIframeResponse(BaseResponse):
    """A response class used with iframe-calls, that supports streaming.

    This class extends :class:`sijax.response.BaseResponse` and
    every available method from it works here too.

    This is used by plugins that use an iframe to perform the Sijax call,
    instead of doing a regular ajax request.
    This has the benefit of allowing us to do streaming, which means that
    response functions can flush the commands buffer whenever they want
    without exiting.

    To push the current commands to the browser you need to use ``yield``,
    like this::

        def my_func(obj_response):
            obj_response.alert('Doing some work.. wait a second')
            yield obj_response

            from time import sleep
            sleep(5)

            obj_response.alert('Done!')

    Your don't need to explicitly ``yield`` at the end of a streaming function.
    What remains unsent when the function exits will eventually get sent.
    """

    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        self._is_first_flush = True

    def _flush(self):
        """Generates command output to flush to the browser.

        The output is not JSON, because it's evaluated in an
        iframe. We're generating some html markup with script tags
        to pass our commands JSON to the parent, which will then execute it.

        We're also pushing some garbage content on the first flush,
        to get around a buffering "issue" certain browsers employ.
        Such browsers include IE and Google Chrome.
        They're generally buffering the first ~1500 bytes of data,
        before they start interpretting it.
        """

        output = """
        <script type="text/javascript">
            window.parent.Sijax.processCommands(%s);
        </script>
        """ % self._get_json()

        self.clear_commands()

        if self._is_first_flush:
            # Push some more data initially, because certain
            # browsers buffer the first X bytes of output
            self._is_first_flush = False
            output = "%s%s%s" % (
                "\n<script type='text/javascript'></script>\n\n",
                "\n" * 2000,
                output
            )

        return output

    def _process_callback(self, callback, args):
        """Processes a callback to a normal or a streaming function.

        In constrast with
        :meth:`sijax.response.BaseResponse._process_callback` which only
        processes normal requests properly, this can process both normal
        and streaming functions.

        Normal functions are the typical Sijax response functions,
        which don't flush content to the browser, but only push commands
        to the buffer list. Those commands are to be flushed by Sijax
        when the response function exits.

        Streaming functions are the typical Comet response functions,
        which are generators (they use yield to flush content).

        Basically this function can be seen as a converter from
        either a generator (streaming function) or a string (normal function)
        to a generator.
        """
        response = self._perform_handler_call(callback, args)
        if isinstance(response, GeneratorType):
            # Real streaming function using a generator to flush
            while True:
                # we don't really care what it yields..
                next(response)
                if len(self._commands) != 0:
                    yield self._flush()
        else:
            # Normal (non-streaming) function
            # Let's flush implicitly for such functions
            if len(self._commands) != 0:
                yield self._flush()

    def _process_call_chain(self, call_chain):
        """Executes all the callbacks in the chain.

        The difference from
        :meth:`sijax.response.BaseResponse._process_call_chain` is that this
        returns a generator instead of a string.
        This allows response functions to flush the commands buffer whenever
        they need, instead of all at once in the end.

        :param call_chain: a list of two-tuples (callback, args list) to call
        """
        for callback, args in call_chain:
            generator = self._process_callback(callback, args)
            for string in generator:
                yield string.encode("utf-8")
#                yield bytes(string, "utf-8")
# in Python 3 every string is unicode and `bytes` will encode accordingly
# in Python 2, using `bytes` from the future module ensures a byte string but
# simply encoding is backwards compatible with `werkzeug`

