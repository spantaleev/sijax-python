var sjxComet = {};

sjxComet.request = function (functionName, callArgs) {
	if (callArgs === undefined) {
		callArgs = [];
	}

	var iframe = document.createElement('iframe'),
		frameId = 'frame4_' + functionName + '_' + (new Date().getTime());

	iframe.setAttribute('id', frameId);
	iframe.setAttribute('name', frameId);
	iframe.setAttribute('style', 'display: none;');

	var form = document.createElement('form'),
		formId = 'form4_' + functionName + '_' + (new Date().getTime());

	form.setAttribute('id', formId);
	form.setAttribute('name', formId);
	form.setAttribute('method', 'post');
	form.setAttribute('action', Sijax.getRequestUri());
	form.setAttribute('target', frameId);

	jQuery('body').append(iframe);
	jQuery('body').append(form);

	jQuery('#' + frameId).bind('load', function () {
		//We need to remove the iframe/form, but only after leaving this callback
		//Or Google Chrome would report "Failed to load resource"
		window.setTimeout(function () {
			jQuery('#' + frameId).remove();
			jQuery('#' + formId).remove();
		});
	});

	var formObject = jQuery('#' + formId);

	var element = document.createElement('input');
	element.setAttribute('type', 'hidden');
	element.setAttribute('name', Sijax.PARAM_REQUEST);
	element.setAttribute('value', functionName);
	formObject.append(element);

	var element = document.createElement('input');
	element.setAttribute('type', 'hidden');
	element.setAttribute('name', Sijax.PARAM_ARGS);
	element.setAttribute('value', JSON.stringify(callArgs));
	formObject.append(element);

	formObject.trigger('submit');
};
