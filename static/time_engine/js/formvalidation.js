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
    //document.getElementById("theForm").onsubmit = validateForm;
    // onclick handler attached to "reset" button calls clearDisplay function
    //document.getElementById("reset").onclick = clearDisplay;
    // set focus to the name field -- investigate HTML5 autofocus!
    document.getElementById("name").focus();
}

function onData() {
    //this gets data when it arrives
    var data = JSON.parse(request.responseText);
    console.log(data); //send to calendar like example shows
     $('#calendarContainer').fullCalendar(data);
}

var request = new XMLHttpRequest();

function loadData() {
    var form_data = [];
    form_data.push('name=' + document.getElementById('name').value);


    request.onreadystatechange = onData;
    request.open('POST', '/time_engine/', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(form_data.join('&'));

}



/* validateForm() is the handler to validate input fields */

function validateForm() {
    var result = true;
    //(isNotEmpty ("name", "Please enter a name.")
    //    && isChecked("color", "Please choose a color.")
    //    && isDate("id_start_date", "Enter a date as dd/mm/yyyy")
    //    && isStartTime("id_start_time", "Enter a start time as HH:MM")
    //    && isNumeric("id_lesson_count", "Enter the number of events in the series.")
    //    && isChecked("checkbox", "Please check at least one day")
    //);
    if (result){
        loadData();
    }
}

// return true if the input value is not empty
function isNotEmpty(inputId, errorMsg) {
    console.log("Input id = ");
    console.log(inputId);
    var inputElement = document.getElementById("id_" + inputId);
    var errorElement = document.getElementById("id_" + inputId + "Error");
    var inputValue = inputElement.value.trim();
    var isValid = (inputValue.length !== 0); // boolean
    showMessage(isValid, inputElement, errorMsg, errorElement);
    return isValid;
}

/* If isValid is false, print the errorMsg;
else, reset to normal display.
show via an alert for now.
Later make it work on an element.
 */
function showMessage(isValid, inputElement, errorMsg, errorElement){
    if (!isValid){
        //display error message:
        if (errorElement !== null) {
            errorElement.innerHTML = errorMsg;
        } else {
            alert(errorMsg);
        }
        //change class of inputElemtn so css displays differently
        if (inputElement !== null) {
            inputElement.className = "error";
            inputElement.focus();
        }
    } else {
        //reset to normal display
        if (errorElement !== null) {
            errorElement.innerHTML = "";
        }
        if (inputElement !== null) {
            errorElement.className = "";
        }
    }
}


// clear the fields when "reset" is clicked
function clearDisplay() {
    //get all the form elements
    var els = document.getElementById("theForm").elements;
    console.log("the elements are ", els);
    // loop over the elements and remove the errors:
    for (var i=0; i < els.length; i++){
        if ((els[i].id).match(/Error$/)) {
            els[i].innerHTML = "";
        }
        if (els[i].className === "error") {
            els[i].className = "";
        }
    }
    //set initial focus again:
    document.getElementById("name").focus();
}

//var runButton = document.getElementById("run");
//console.log(runButton);
//runButton.addEventListener("click", validateForm);

//if validates make the request.