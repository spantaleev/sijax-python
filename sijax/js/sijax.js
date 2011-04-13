var Sijax = {};

Sijax.PARAM_REQUEST = 'sijax_rq';
Sijax.PARAM_ARGS = 'sijax_args';

Sijax.requestUri = null;

Sijax.setRequestUri = function (uri) {
	Sijax.requestUri = uri;
};

Sijax.getRequestUri = function () {
	return Sijax.requestUri;
};

Sijax.setJsonUri = function (uri) {
	if (uri === null || typeof(JSON) !== "undefined") {
		return;
	}

	jQuery.getScript(uri);
};

Sijax.processCommands = function (commandsArray) {
	jQuery.each(commandsArray, function (idx, command) {
		var callback = Sijax.getCommandProcessor(command.type);
		callback(command);
	});
};

Sijax.getCommandProcessor = function (commandType) {
	return Sijax["process_" + commandType];
};

Sijax.process_alert = function (params) {
	window.alert(params.alert);
};

Sijax.process_html = function (params) {
	var selectorResult = jQuery(params.selector);

	if (params.setType == 'replace') {
		selectorResult.html(params.html);
	} else if (params.setType == 'append') {
		selectorResult.append(params.html);
	} else {
		selectorResult.prepend(params.html);
	}
};

Sijax.process_attr = function (params) {
	var selectorResult = jQuery(params.selector);

	if (params.setType === 'replace') {
		selectorResult.attr(params.key, params.value);
	} else if (params.setType === 'append') {
		selectorResult.attr(params.key, selectorResult.attr(params.key) + params.value);
	} else {
		selectorResult.attr(params.key, params.value + selectorResult.attr(params.key));
	}
};

Sijax.process_css = function (params) {
	jQuery(params.selector).css(params.key, params.value);
};

Sijax.process_script = function (params) {
	eval(params.script);
};

Sijax.process_remove = function (params) {
	jQuery(params.remove).remove();
};

Sijax.process_call = function (params) {
	var callbackString = params.call,
		callback = eval(callbackString);

	callback.apply(null, params.params);
};

Sijax.request = function (functionName, callArgs, requestParams) {
	if (callArgs === undefined) {
		callArgs = [];
	}

	if (requestParams === undefined) {
		requestParams = {};
	}

	var data = {},
		defaultRequestParams;

	data[Sijax.PARAM_REQUEST] = functionName;
	data[Sijax.PARAM_ARGS] = JSON.stringify(callArgs);

	defaultRequestParams = {
		"url": Sijax.requestUri,
		"type": "POST",
		"data": data,
		"cache": false,
		"dataType": "json",
		"success": Sijax.processCommands
	};

	jQuery.ajax(jQuery.extend(defaultRequestParams, requestParams));
};

Sijax.getFormValues = function (formSelector) {
	var values = {};

	jQuery.each(jQuery(formSelector).find('input, textarea, select'), function (idx, object) {
		var attrName = jQuery(this).attr('name'),
			attrValue = jQuery(this).attr('value'),
			tagName = this.tagName,
			type = jQuery(this).attr('type'),
			nestingParts;

		if (attrName === '' || jQuery(this).attr('disabled') === true) {
			return;
		}

		if (tagName === 'INPUT') {
			if ((type === 'checkbox' || type === 'radio') && ! jQuery(this).attr('checked')) {
				return;
			}
		}

		if (attrValue === "") {
			//IE's JSON.stringify doesn't like empty bare strings
			//It replaces "" with "null", unless we wrap them in a String() object
			attrValue = new String(attrValue);
		}

		if (attrName.indexOf('[') === -1) {
			//Regular field name, not really nested
			nestingParts = [attrName];
		} else {
			//Nested field, like `something[key][key2][]`
			var nestedMatches = /^(\w+)\[(.*?)\]$/.exec(attrName);
			if (nestedMatches === null) {
				//Bad name field syntax, skip this attribute
				return;
			}
			//nestedMatches looks like this: `[attrNameReal, 'key][key2][']`
			nestingParts = [nestedMatches[1]].concat(nestedMatches[2].split(']['));
		}

		var nestingRef = values,
			lastPart = nestingParts.pop(),
			isArrayTarget = (lastPart === '');

		//Descend into the structure, creating any missing elements
		jQuery.each(nestingParts, function (i, part) {
			if (typeof(nestingRef[part]) === 'undefined') {
				var isLastPart = (nestingParts.length - 1 === i);
				nestingRef[part] = (isLastPart && isArrayTarget ? [] : {});
			}
			nestingRef = nestingRef[part];
		});

		if (isArrayTarget) {
			nestingRef.push(attrValue);
		} else {
			nestingRef[lastPart] = attrValue;
		}
	});

	return values;
};
