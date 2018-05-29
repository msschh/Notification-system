function expand(obj) {
	nextObj = $(obj).next();
	if ($(nextObj).is(":visible")) {
		$(nextObj).hide();
	} else {
		$(nextObj).show();
	}
}