# -*- coding: utf-8 -*-

"""
    sijax.plugin.upload
    ~~~~~~~~~~~~~~~~~~~

    Provides helpers to register Upload functions.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from ...helper import json
from ...exception import SijaxError
from .UploadResponse import UploadResponse


# Parameters with these names are passed to the client side (JS)
# Modifying this would mean modifying the javascript files
PARAM_FORM_ID = "formId"
PARAM_CALLBACK = "callback"


def _prepare_options(sijax_instance, options):
    param_response_class = sijax_instance.__class__.PARAM_RESPONSE_CLASS
    if param_response_class not in options:
        options[param_response_class] = UploadResponse

    return options


def func_name_by_form_id(form_id):
    return "%s_upload" % form_id


def register_upload_callback(sijax_instance, form_id, callback, **options):
    """Helps you easily register Upload functions with Sijax.
    
    We suggest that the `args_extra` options is passed here, so that the
    response function would receive the files object or anything else it might be
    needing to manipulate file uploads.
    By using `args_extra` you could change the response function's default header from::

        def upload_handler(obj_response, form_values)

    to::

        def upload_handler(obj_response, files, form_values)

    where the args_extra=[files] option was passed during registering.

    It's very important to keep in mind that unlike the regular
    :meth:`sijax.Sijax.Sijax.register_callback` function, this one returns some javascript code
    as a response. You need to execute that code on the page that contains the
    form you want to transform to Sijax upload.

    :param sijax_instance: the :class:`sijax.Sijax.Sijax` instance to register callbacks with
    :param form_id: the id of the form as it appears in the DOM
    :param callback: the function that would get called to process the upload request
    :param options: options to pass to :meth:`sijax.Sijax.Sijax.register_callback`
    :return: string - javascript code you need to put on your page,
                      to make your form use Sijax when submitted
    """

    public_name = func_name_by_form_id(form_id)

    options = _prepare_options(sijax_instance, options)
    sijax_instance.register_callback(public_name, callback, **options)

    js_params = json.dumps({PARAM_FORM_ID: form_id, PARAM_CALLBACK: public_name})
    return "jQuery(function() { sjxUpload.registerForm(%s); });" % js_params

