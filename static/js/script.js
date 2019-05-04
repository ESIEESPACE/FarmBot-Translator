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
    target.append("<input id='cl-" + id + "' type='button' value='Cancel' class='btn btn-danger cnButton'>");
    target.append("<input id='sc-" + id + "' type='button' value='Save' class='btn btn-success cnButton'>");

    let textarea = $("#tz-" + id);
    let clButton = $("#cl-" + id);
    let scButton = $("#sc-" + id);

    textarea.focus();

    scButton.click(saveTranslation);

    clButton.click(function () {
        target.removeClass("selected");
        target.empty();
        target.text(content);
    });
});

$.urlParam = function(name){
	let results = new URL(window.location.href);
	return results.searchParams.get(name);
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
            id: parseInt(id.substring(3)),
            translation: content 
        });

    request.done(function () {
        coloredSignal(tr, "rgba(40, 167, 69, 1)", 500);
    });

    request.fail(function () {
        coloredSignal(tr, "rgba(250, 55, 69, 1)", 500);
    })
}

function coloredSignal(object, bckColor, duration, txtColor = "rgba(255, 255, 255, 1)") {
    //Time init
    const refreshRate = 10;
    let timeCounter = 0;

    //Original and target background
    let originBckColor = object.css("background-color").substring(5).replace(')', '').split(',');
    bckColor = bckColor.substring(5).replace(')', '').split(',');

    //Original and target color
    let originTxtColor = object.css("color").substring(4).replace(')', '').split(',');
    txtColor = txtColor.substring(5).replace(')', '').split(',');


    let interval = setInterval(function () {

        //Background color
        let tempBckColor = "rgba(";
        for(let i=0; i<4; i++){
            if(i!=0) tempBckColor += ",";
            let coef = (parseFloat(originBckColor[i]) - parseFloat(bckColor[i]))/duration;
            let cons = -coef * duration + parseFloat(originBckColor[i]);
            tempBckColor += coef * timeCounter + cons;
        }
        tempBckColor += ")";
        object.css("background-color", tempBckColor);

        //Text color
        let tempTxtColor = "rgba(";
        for(let i=0; i<3; i++){
            if(i!=0) tempTxtColor += ",";
            let coef = (parseFloat(originTxtColor[i]) - parseFloat(txtColor[i]))/duration;
            let cons = -coef * duration + parseFloat(originTxtColor[i]);
            tempTxtColor += coef * timeCounter + cons;
        }
        tempTxtColor += ")";
        object.css("color", tempTxtColor);

        //Timing operations
        timeCounter += refreshRate;
        if(timeCounter >= duration) {
            clearInterval(interval);
            setTimeout(function () {
                object.css("background-color", "");
                object.css("color", "");
            }, refreshRate)
        }
    }, refreshRate);
}

function updateByID(id, content, date) {
    let row = $("#" + id);
    row.find("td.td-tr").text(content);
    row.find("td.date").text(date);
    coloredSignal(row, "rgba(40, 167, 69, 1)", 500);
}