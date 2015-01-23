/**
 * Created by student on 1/22/15.
 */

/* this file is where I validate the form data and
   also send off the ajax request.
 */

// the init() function runs after the page is fully loaded
window.onload = init;

function init(){
    // validateForm function is the onsubmit handler
    document.getElementById("theForm").onsubmit = validateForm;
    // onclick handler attached to "reset" button calls clearDisplay function
    document.getElementById("reset").onclick = clearDisplay;
    // set focus to the name field -- investigate HTML5 autofocus!
    document.getElementById("tt_name").focus();
}

/* validateForm() is the handler to validate input fields */

function validateForm() {
    return (isNotEmpty ("tt_name", "Please enter a name.")
        && isChecked("color", "Please choose a color.")
        && isDate("id_start_date", "Enter a date as dd/mm/yyyy")
        && isStartTime("id_start_time", "Enter a start time as HH:MM")
        && isNumeric("id_lesson_count", "Enter the number of events in the series.")
        && isChecked("checkbox", "Please check at least one day")
    );
}

// clear the fields when "reset" is clicked
function clearDisplay() {
    //get all the form elements
    var els = document.getElementById("theForm").elements;
    console.log("the elements are ", els);
    // loop over the elements and remove the errors:
    for (var i=0; i < els.length; i++){
        if ((els[i].className).match(/errorlist$/)) {
            elms[i].innerHTML = "";
        }
        if (els[i].className === "errorlist") {
            els[i].className = "";
        }
    }
    //set initial focus again:
    document.getElementById("tt_name").focus();
}

var runButton = document.getElementById("run");
console.log(runButton);
runButton.addEventListener("click", validateForm);