from .BaseResponse import BaseResponse
from types import GeneratorType


class StreamingIframeResponse(BaseResponse):
    """A response class used with iframe-calls and supporting streaming.

    This is used by plugins that use an iframe to perform the Sijax call,
    instead of doing a regular ajax request.
    This has the benefit of allowing us to do streaming, which means that
    response functions can flush the commands buffer whenever they want
    without exiting.
    """

    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        self._is_first_flush = True
    
    def flush(self):
        """Generates command output to flush to the browser.
        
        The output is not JSON, because it's evaluated in an
        iframe. We're generating some html markup with script tags
        to pass our commands JSON to the parent, which will then execute it.

        We're also pushing some garbage content on the first flush,
        to get around a buffering "issue" certain browsers employ.
        Such browsers include IE and Google Chrome.
        They're generally buffering the first ~1500 bytes of data,
        before they start interpretting it.

        This should be used in streaming (Comet) functions when data
        is to be flushed to the browser.
        It should be used like this:
            obj_response.alert("Message")
            yield obj_response
            ... some other code here..
        which sends the alert() to the browser before executing the other code.

        Your don't need to explicitly flush at the end of a streaming function.
        What remains unflushed when the function exits will eventually get flushed.
        """
        output = """
        <script type="text/javascript">
            window.parent.Sijax.processCommands(%s);
        </script>
        """ % self.get_json()

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

        In constrast with SijaxResponse._process_callback, which only
        processes normal requests properly, this can process normal
        and streaming functions.

        Normal functions are the typical Sijax response functions,
        which don't flush content to the browser, but only push commands
        to the buffer list. Those commands are to be flushed by Sijax
        when the response function exits.

        Streaming functions are the typical Comet response functions,
        which are generators (they use yield to flush content).

        Basically this function can be seens as a converter from
        either a generator (streaming function) or a string (normal function)
        to a generator.
        """
        try:
            response = callback(self, *args)
        except TypeError:
            # we should re-raise the exception if it's coming
            # from within the function, meaning calling works.. @todo
            failed_callback = callback
            event_invalid_call = self._sijax.__class__.EVENT_INVALID_CALL
            callback = self._sijax.get_event(event_invalid_call)
            response = callback(self, failed_callback)


        if isinstance(response, GeneratorType):
            # Real streaming function using a generator to flush
            while True:
                # we don't really care what it yields..
                response.next()
                if len(self._commands) != 0:
                    yield self.flush()
        else:
            # Normal (non-streaming) function
            # Let's flush implicitly for such functions
            if len(self._commands) != 0:
                yield self.flush()

    def _process_call_chain(self, call_chain):
        """Executes all the callbacks in the chain for streaming response objects.

        The difference from SijaxResponse._process_call_chain is that this
        returns a generator instead of a string. This allows response functions
        to flush the commands buffer whenever they need, instead of all at once
        in the end.

        :param call_chain: a list of two-tuples (callback, args list) to call
        """
        for callback, args in call_chain:
            generator = self._process_callback(callback, args)
            for string in generator:
                yield str(string)

