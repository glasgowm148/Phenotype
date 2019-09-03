/* Laura M. Ascher

===== Form Validation ===== */

// Check if #validate_msg div box contains text parameter
function textInContainer(text) {
    return $("#validate_msg:contains('" + text + "')").length === 0;
}

// Check if all radio buttons have been checked
function radio_allChecked(form) {
    var checkedAll = true;
    var radioNames = [];
    $("#" + form + " :radio").each(function() {
        var name = $(this).attr("name");
        if (radioNames.indexOf(name) < 0) radioNames.push(name);
    });
    $.each(radioNames, function(key, value) {
        var radioChecked = $("input:radio[name='" + value + "']").is(":checked");
        checkedAll = checkedAll && radioChecked;
    });
    return checkedAll;
}

// Check if user inputted ints in all text inputs 
function text_allInts(form) {
    var intRegex = /^\d+$/;
    var textNames = [];
    var checkedAll = true;
    $("#" + form + " :text").each(function() {
        var name = $(this).attr("name");
        if (textNames.indexOf(name) < 0) textNames.push(name);
    });
    $.each(textNames, function(key, value) {
        var hasText = (intRegex.test($("input:text[name='" + value + "']").val()));
        checkedAll = checkedAll && hasText;
    });
    return checkedAll;
}

// Update pop-up validation message
function updateWarningText(container, text) {
    var text_newHtml = container.html().replace(text, '');
    container.html(text_newHtml);
}

// Form validation
function validateForm_vis(submit, form, container) {
    var closeBtn = "<div id='exitBtn'>X</div>";
    container.hide();
    submit.click(function(event) {
        event.preventDefault();
        if (container.find($("#exitBtn")).size() === 0) {
            container.append(closeBtn);
        }
        //Check if form was filled out appropriately
        var txt_allInts = text_allInts($(form).attr('id'));
        var rd_allChecked = radio_allChecked($(form).attr('id'));
        var textarea = $(form).find("textarea");
        var textarea_filled = textarea.length === 0 ? true : textarea.val().length > 0;
        var onlyError = "Please answer all the survey questions to continue.";
        var onlyError_none = textInContainer(onlyError);
        if (txt_allInts && rd_allChecked && textarea_filled) {
            form.submit();
        } else {
			container.append(onlyError+"<p>");
            container.fadeIn(500, 0, function() {
                container.show();
            });
            $('#exitBtn').on('click', container, function() {
                container.fadeOut(300, 0, function() {
                    container.hide(function() {
                        container.html("");
                    });
                });
            });

        }
    });
}