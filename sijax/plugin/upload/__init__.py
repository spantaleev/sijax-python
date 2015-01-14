# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

"""
    sijax.plugin.upload
    ~~~~~~~~~~~~~~~~~~~

    Provides helpers to register Upload functions,
    and the :class:`sijax.plugin.comet.UploadResponse` class
    used instead of :class:`sijax.response.BaseResponse`.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from ...helper import json
from ...response import StreamingIframeResponse

# Parameters with these names are passed to the client side (JS)
# Modifying this would mean modifying the javascript files
PARAM_FORM_ID = 'formId'
PARAM_CALLBACK = 'callback'


def _prepare_options(sijax_instance, options):
    param_response_class = sijax_instance.__class__.PARAM_RESPONSE_CLASS
    if param_response_class not in options:
        options[param_response_class] = UploadResponse

    return options


def func_name_by_form_id(form_id):
    return '%s_upload' % form_id


def register_upload_callback(sijax_instance, form_id, callback, **options):
    """Helps you easily register Upload functions with Sijax.

    We recommend the ``args_extra`` option to be used here, so that the
    response function would receive the files object or
    anything else it might be needing to manipulate file uploads.
    By using ``args_extra`` you could change the response function's
    default signature from::

        def upload_handler(obj_response, form_values)

    to::

        def upload_handler(obj_response, files, form_values)

    where the args_extra=[files] option was passed during registering.
    To learn more on how the ``args_extra`` option works,
    refer to :meth:`sijax.Sijax.register_callback`.

    It's very important to keep in mind that unlike the regular
    :meth:`sijax.Sijax.register_callback` function, this one
    returns some javascript code as a response.
    You need to execute that code on the page that contains the
    form you want to transform to Sijax upload.

    :param sijax_instance: the :class:`sijax.Sijax` instance
                           to register callbacks with
    :param form_id: the id of the form as it appears in the DOM
    :param callback: the function to call to process the upload request
    :param options: options to pass to :meth:`sijax.Sijax.register_callback`
    :return: string - javascript code you need to put on your page,
                      to make your form use Sijax when submitted
    """

    public_name = func_name_by_form_id(form_id)

    options = _prepare_options(sijax_instance, options)
    sijax_instance.register_callback(public_name, callback, **options)

    js_params = json.dumps({PARAM_FORM_ID: form_id, PARAM_CALLBACK: public_name})
    return 'jQuery(function() { sjxUpload.registerForm(%s); });' % js_params


class UploadResponse(StreamingIframeResponse):
    """Class used for Upload handler functions,
    instead of the :class:`sijax.response.BaseResponse` class.

    This class extends :class:`sijax.response.BaseResponse` and
    every available method from it works here too.
    """

    def __init__(self, *args, **kwargs):
        StreamingIframeResponse.__init__(self, *args, **kwargs)

        # The form_id that we're dealing with is the only expected argument.
        req_args = self._request_args
        req_args_len = len(req_args)
        if req_args_len != 1:
            raise RuntimeError('We only expect 1 request argument, %d given.' %
                               req_args_len)
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
        return self.call('sjxUpload.resetForm', [self.form_id])
