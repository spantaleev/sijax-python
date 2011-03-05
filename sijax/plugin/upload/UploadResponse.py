# -*- coding: utf-8 -*-

"""
    sijax.plugin.upload.UploadResponse
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Provides the UploadResponse class, an instance of which
    is passed as the first argument to all Upload functions.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from ...response.StreamingIframeResponse import StreamingIframeResponse


class UploadResponse(StreamingIframeResponse):

    def __init__(self, *args, **kwargs):
        StreamingIframeResponse.__init__(self, *args, **kwargs)

        # The form_id that we're dealing with is the only expected argument.
        req_args = self._request_args
        req_args_len = len(req_args)
        if req_args_len != 1:
            raise RuntimeError("We only expect 1 request argument, %d given." % req_args_len)
        self._form_id = req_args[0]

        # Let's override the request arguments now
        # The upload handler function is to expect only one argument
        # which is a dictionary of form values
        # To get the form values from all the POST data,
        # we simply need to get rid of some internal/system params

        # We're creating a new dict, because the POST data dictionary
        # may be immutable and/or we don't want to change it anyways.
        # We want to work on a copy of it.
        form_values = dict(self._sijax.get_data())
        del form_values[self._sijax.__class__.PARAM_REQUEST]
        del form_values[self._sijax.__class__.PARAM_ARGS]
        self._request_args = [form_values]

    @property
    def form_id(self):
        """The id of the form that was submitted.

        You can have several forms handled by the same upload handler
        function, which can be confusing unless you know the form id.
        """
        return self._form_id

    def reset_form(self):
        """Resets the form to the state it was in at page loading time.

        Any changes made to it after that will be cleared."""
        return self.call("sjxUpload.resetForm", [self.form_id])
