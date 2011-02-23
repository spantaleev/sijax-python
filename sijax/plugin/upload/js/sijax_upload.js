var sjxUpload = {};

sjxUpload.FIELD_FORM_ID = 'sjxUpload_formId';

sjxUpload.getFrameId = function (formId) {
	return 'sjxUpload_iframe_' + formId;
};

sjxUpload.prepareForm = function (formId, callbackName) {
	var frameId = sjxUpload.getFrameId(formId),
		formObject = $('#' + formId),
		requestArgs = JSON.stringify([formId]),
		element;
	
	formObject.attr('target', frameId);
	formObject.attr('method', 'post');
	formObject.attr('enctype', 'multipart/form-data');
	
	if (formObject.attr('action') === '') {
		//Only change the submit URI if it's not explicitly set to something
		formObject.attr('action', Sijax.getRequestUri());
	}
	
	if (formObject.attr(Sijax.PARAM_REQUEST) === undefined) {
		//Initial registration
		element = document.createElement('input');
		element.setAttribute('type', 'hidden');
		element.setAttribute('name', Sijax.PARAM_REQUEST);
		element.setAttribute('value', callbackName);
		formObject.append(element);
		
		element = document.createElement('input');
		element.setAttribute('type', 'hidden');
		element.setAttribute('name', Sijax.PARAM_ARGS);
		element.setAttribute('value', requestArgs);
		formObject.append(element);
	} else {
		//The fields are already created, let's just "refresh" their contents
		formObject.attr(Sijax.PARAM_REQUEST).value = callbackName;
		formObject.attr(Sijax.PARAM_ARGS).value = requestArgs;
	}
};

sjxUpload.resetForm = function (formId) {
	var callbackName = $('#' + formId).attr(Sijax.PARAM_REQUEST).value;
	
	$('#' + formId).each(function () {
		this.reset();
	});
	
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

	$('#' + formId).append(iframe);
	
	if (window.frames[frameId].name !== frameId) {
		//IE bugfixes
		window.frames[frameId].name = frameId;
		$('#' + frameId).css('display', 'none');
	}

	sjxUpload.prepareForm(formId, callbackName);
};

sjxUpload.processResponse = function (formId, commandsArray) {
	Sijax.processCommands(commandsArray);
};
