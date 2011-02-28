# -*- coding: utf-8 -*-

"""
    sijax.plugin.comet.CometResponse
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Provides the CometResponse class, an instance of which
    is passed as the first argument to all Comet functions.

    :copyright: (c) 2011 by Slavi Pantaleev.
    :license: BSD, see LICENSE.txt for more details.
"""


from ...response.StreamingIframeResponse import StreamingIframeResponse


class CometResponse(StreamingIframeResponse):
    pass
