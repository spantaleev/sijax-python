Upload Plugin
=============

The Upload plugin for Sijax was developed to make ajax file uploads an easy task.

The idea is that you tell Sijax which form you want to be submitted to what handler function,
and it transforms that form in a way to do that.

Suppose you have this markup on your page::

    <form id="formOne" name="formOne"                                                                                                                                              
         style="width: 400px" method="post" enctype="multipart/form-data">
        Text field:
        <input type="text" name="message" value="Some text" /><br />

        Drop-down:
        <select name="dropdown">
            <option>1</option>
            <option selected="selected">2</option>
            <option>3</option>
        </select>
        <br />

        Chechbox:
        <input type="checkbox" checked="checked" name="chkbox" /><br />

        File:
        <input type="file" name="file" /><br />

        <input type="submit" value="Upload" />
    </form>


To convert this form to a Sijax-enabled one, you need the following Python code::

    from sijax.plugin.upload import register_upload_callback

    def upload_handler(obj_response, form_values):
        # form_values = {'message': ['Some text'], 'chkbox': ['on'], 'dropdown': ['2']}
        obj_response.alert(repr(form_values))
    
    js = register_upload_callback(sijax_instance, "formOne", upload_handler)
    
    # put the returned javascript code somewhere on your page to make your form Sijax-enabled


Notes on function registration
------------------------------

It's important to note that the ``register_upload_callback`` function returns a short javascript code snippet,
which takes care of preparing the form, so that it can be submitted using Sijax.

The ``args_extra`` function registration parameter can be used here (read more on it in `callbacks.rst`).
It's a good idea to always register upload handler function with one additional argument - the files object,
which would be used to manipulate the uploaded files.

For some environment there's really no way around it, because at the context at which the upload handler function executes,
there may not be an easy way (if any at all) to get a reference to the files object.

To pass an additional argument to ``upload_handler`` just do::
    
    files = {"your": "file", "object" "here"}

    def upload_handler(obj_response, files, form_values):
        pass

    register_upload_callback(sijax_instance, "formOne", upload_handler, args_extra=[files])


Streaming responses (Comet functionality)
-----------------------------------------

The way the Upload plugin works is very similar to the way the Upload plugin works.
They share most of their code, so you can do comet streaming from your upload handler function too.
Let's take a look at an example which handles a hypothetical image upload::

    def upload_handler(obj_response, files, form_values):
        obj_response.alert("Processing your image file..")
        yield obj_response

        resize_image(files)
        url = get_image_url()

        obj_response.redirect(url)

You don't need to do anything special to get streaming support in your upload handler functions.
Every function registered via `sijax.plugin.upload.register_upload_callback` supports Comet (can yield/flush whenever it wants).


The response object
-------------------

The response object (``obj_response``) for upload functions is an instance of `sijax.plugin.upload.UploadResponse`.
It provides several additional attributes over the `sijax.response.BaseResponse` class object, which is used with normal functions::

    - obj_response.form_id - the id of the form that was submitted (you can have several forms submit to the same upload handler function)
    - obj_response.reset_form() - a new response command, which resets the form to the way it was after page loading
