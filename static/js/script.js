$(".td-tr").dblclick(function (event) {
    var target = $(event.target);

    if(target.hasClass("selected") || target.parent().hasClass("selected")) return;


    var id = $(event.target).attr("id");
    var content = target.text();

    target.addClass("selected");

    target.empty();
    target.append("<textarea id=\"tz-" + id + "\" class=\"tz-tr form-control\">" + content + "</textarea>");
    target.append("<input id=\"bt-" + id + "\" type='button' value='Cancel'>");

    var textarea = $("#tz-" + id);
    var cnButton = $("#bt-" + id);

    textarea.focus();
    textarea.focusout(function () {
        target.removeClass("selected");
        target.empty();
        target.text(textarea.val());
        $.post( "update/", { language: $.urlParam("language"), id: parseInt(id.substring(3)) + 1, translation: textarea.val() } );
    });

    cnButton.click(function () {
        target.removeClass("selected");
        target.empty();
        target.text(content);
    });
});

$.urlParam = function(name){
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results[1] || 0;
}