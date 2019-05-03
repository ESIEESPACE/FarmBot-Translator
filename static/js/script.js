$(".td-tr").dblclick(function (event) {

    saveTranslation();
    let target = $(event.target);

    //If it's already selected then return
    if(target.hasClass("selected") || target.parent().hasClass("selected")) return;

    let id = $(event.target).attr("id");
    let content = target.text();

    target.addClass("selected");

    target.empty();

    target.append("<textarea id='tz-" + id + "' class='tz-tr form-control'>" + content + "</textarea>");
    target.append("<input id='bt-" + id + "' type='button' value='Cancel' class='btn btn-danger cnButton'>");

    let textarea = $("#tz-" + id);
    let cnButton = $("#bt-" + id);

    textarea.focus();

    cnButton.click(function () {
        target.removeClass("selected");
        target.empty();
        target.text(content);
    });
});

$.urlParam = function(name){
	let results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results[1] || 0;
};

/**
 * Save selected translations
 */
function saveTranslation() {
    let selected = $(".selected");

    if(selected.length == 0) return;

    let id = selected.attr("id");
    let content = selected.find("textarea").val();
    let tr = selected.parent();

    selected.removeClass("selected");
    selected.empty();
    selected.text(content);

    let request = $.post( "update/",
        { 
            language: $.urlParam("language"),
            id: parseInt(id.substring(3)) + 1,
            translation: content 
        });

    request.done(function () {
        tr.addClass("bg-success");
        setTimeout(function(){
            tr.removeClass("bg-success")
        }, 1500);
    });

    request.fail(function () {
        tr.addClass("bg-danger");
        setTimeout(function(){
            tr.removeClass("bg-danger")
        }, 1500);
    })
}