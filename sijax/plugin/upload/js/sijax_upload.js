var sjxUpload = {};

sjxUpload.FIELD_FORM_ID = 'sjxUpload_formId';

sjxUpload.getFrameId = function (formId) {
	return 'sjxUpload_iframe_' + formId;
};

sjxUpload.prepareForm = function (formId, callbackName) {
	var frameId = sjxUpload.getFrameId(formId),
		$object = jQuery('#' + formId),
		requestArgs = JSON.stringify([formId]),
		element,
        attrOrProp = (! $object.prop ? 'attr' : 'prop');

	$object.attr('target', frameId);
	$object.attr('method', 'post');
	$object.attr('enctype', 'multipart/form-data');

	if ($object[attrOrProp]('action') === '') {
		//Only change the submit URI if it's not explicitly set to something
		$object[attrOrProp]('action', Sijax.getRequestUri());
	}

	if (! $object[attrOrProp](Sijax.PARAM_REQUEST)) {
		//Initial registration
		element = document.createElement('input');
		element.setAttribute('type', 'hidden');
		element.setAttribute('name', Sijax.PARAM_REQUEST);
		element.setAttribute('value', callbackName);
		$object.append(element);

		element = document.createElement('input');
		element.setAttribute('type', 'hidden');
		element.setAttribute('name', Sijax.PARAM_ARGS);
		element.setAttribute('value', requestArgs);
		$object.append(element);
	} else {
		//The fields are already created, let's just "refresh" their contents
		$object.find('input[name=' + Sijax.PARAM_REQUEST + ']').val(callbackName);
		$object.find('input[name=' + Sijax.PARAM_ARGS + ']').val(requestArgs);
	}
};

sjxUpload.resetForm = function (formId) {
	var $form = jQuery('#' + formId),
		callbackName = $form.find('input[name=' + Sijax.PARAM_REQUEST + ']').val();

	$form[0].reset();

	sjxUpload.prepareForm(formId, callbackName);
};

sjxUpload.registerForm = function (params) {
	var formId = params.formId,
		frameId = sjxUpload.getFrameId(formId),
		callbackName = params.callback,
		iframe = document.createElement('iframe');

	iframe.setAttribute('id', frameId);
	iframe.setAttribute('name', frameId);
	iframe.setAttribute('style', 'display: none');

	jQuery('#' + formId).append(iframe);

	if (window.frames[frameId].name !== frameId) {
		//IE bugfixes
		window.frames[frameId].name = frameId;
		jQuery('#' + frameId).css('display', 'none');
	}

	sjxUpload.prepareForm(formId, callbackName);
};

sjxUpload.processResponse = function (formId, commandsArray) {
	Sijax.processCommands(commandsArray);
};
