$(".td-tr").dblclick(function (event) {
    var target = $(event.target);

    if(target.hasClass("selected") || target.parent().hasClass("selected")) return;

    var id = $(event.target).attr("id");
    var content = target.text();

    target.addClass("selected");

    target.empty();
    target.append("<textarea id=\"tz-" + id + "\" class=\"tz-tr form-control\">" + content + "</textarea>");

    var textarea = $("#tz-" + id);

    textarea.focus();
    textarea.focusout(function () {
        target.removeClass("selected");
        target.empty();
        target.text(textarea.val());
    });

});