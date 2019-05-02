$(".td-tr").dblclick(function (event) {
    var target = $(event.target);
    var id = $(event.target).attr("id");
    var content = target.text();

    target.empty();
    target.append("<input id=\"tz-" + id + "\" class=\"tz-tr form-control\" value=\"" + content + "\">");
    $("#tz-" + id).focus();
    $("#tz-" + id).focusout(function () {
        target.empty();
        target.text(content);
    })
});