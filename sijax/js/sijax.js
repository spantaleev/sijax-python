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

	$.getScript(uri);
};

Sijax.processCommands = function (commandsArray) {
	$.each(commandsArray, function (idx, command) {
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
	var selectorResult = $(params.selector);
	
	if (params.setType == 'replace') {
		selectorResult.html(params.html);
	} else if (params.setType == 'append') {
		selectorResult.append(params.html);
	} else {
		selectorResult.prepend(params.html);
	}
};

Sijax.process_attr = function (params) {
	var selectorResult = $(params.selector);
	
	if (params.setType === 'replace') {
		selectorResult.attr(params.key, params.value);
	} else if (params.setType === 'append') {
		selectorResult.attr(params.key, selectorResult.attr(params.key) + params.value);
	} else {
		selectorResult.attr(params.key, params.value + selectorResult.attr(params.key));
	}
};

Sijax.process_css = function (params) {
	$(params.selector).css(params.key, params.value);
};

Sijax.process_script = function (params) {
	eval(params.script);
};

Sijax.process_remove = function (params) {
	$(params.remove).remove();
};

Sijax.process_call = function (params) {
	var callbackString = params.call,
		callback = eval(callbackString);
	
	callback(params.params);
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
	
	$.ajax($.extend(defaultRequestParams, requestParams));
};

Sijax.getFormValues = function (formSelector) {
	var values = {},
		regexNested = /(\w+)\[(\w+)\]/,
		elementsSelector = formSelector + ' input, ' + formSelector + ' textarea, ' + formSelector + ' select';

	$.each($(elementsSelector), function (idx, object) {
		var attrName = $(this).attr('name'),
			attrValue = $(this).attr('value'),
			attrDisabled = $(this).attr('disabled'),
			nestedMatches;

		if (attrName === '' || attrDisabled === true) {
			return;
		}
		
		if (this.tagName === 'INPUT' && $(this).attr('type') === 'checkbox' && ! $(this).attr('checked')) {
			return;
		}

		if (attrValue === "") {
			//IE's JSON.stringify doesn't like empty bare strings
			//It replaces "" with "null", unless we wrap them in a String() object
			attrValue = new String(attrValue);
		}

		nestedMatches = regexNested.exec(attrName);
		if (nestedMatches === null) {
			values[attrName] = attrValue;
		} else {
			//0: wholeMatch, 1: outerObjectKey, 2: innerKey
			if (values[nestedMatches[1]] === undefined) {
				values[nestedMatches[1]] = {};
			}

			values[nestedMatches[1]][nestedMatches[2]] = attrValue;
		}
	});

	return values;
};