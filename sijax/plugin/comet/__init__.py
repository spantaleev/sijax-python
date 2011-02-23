from .CometResponse import CometResponse


def _prepare_options(sijax_instance, options):
    param_response_class = sijax_instance.__class__.PARAM_RESPONSE_CLASS
    if param_response_class not in options:
        options[param_response_class] = CometResponse

    return options


def register_comet_callback(sijax_instance, public_name, callback, **options):
    """Helps you easily register Comet functions with Sijax.
    
    :param sijax_instance: the :class:`Sijax` instance to register callbacks with
    :param public_name: the name of the function that the client will use to call it
    :param callback: the actual function that would get called to process the request
    :param options: options to pass to :meth:`Sijax.register_callback`
    """
    options = _prepare_options(sijax_instance, options)
    sijax_instance.register_callback(public_name, callback, **options)


def register_comet_object(sijax_instance, obj, **options):
    """Helps you easily register all "public" callable attributes of an object.

    :param sijax_instance: the :class:`Sijax` instance to register callbacks with
    :param obj: the object whose methods to register with Sijax
    :param options: options to pass to :meth:`Sijax.register_callback`
    """
    options = _prepare_options(sijax_instance, options)
    sijax_instance.register_object(obj, **options)
        
