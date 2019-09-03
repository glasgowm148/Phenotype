// Filename: assign9.js
// Purpose: Javascript functions for assign9.html
// Created: November 19, 2015
// Authors: Christina Pollalis and Isabelle Styslinger
// More: Contains the four main tasks, outlined in the homework assignments



//task 1: Function "formatOrder" that takes in no arguments and forumlates a string
//in this format: "Order made by Christina Pollalis (cpollali@wellesley.edu) on
//Thu Nov 19 2015 16:24:28 GMT-0500 (EST) 1 gloves 2 hats 3 scarves" and places
//this string in the order summary box
function formatOrder() {
    //console.log("i am in formatOrder"); //testing
    //initializes all the variables needed to create the string, as described above
    var name = $("#customer").val();
    var email = $("#email").val();
    var date = new Date();
    var gloves_quant = $("#gloves_quant").val();
    var hat_quant = $("#hat_quant").val();
    var scarf_quant = $("#scarf_quant").val();
    //create the string from the above:
    var s ="Order made by "+name + " (" + email+") on "+date+" \n"+gloves_quant +
    " gloves \n" + hat_quant + " hats \n" + scarf_quant + " scarves \n" ;
    //console.log(s); //testing
    $("#summary").val(s); //puts the above string in the order summary box
}

//task 2: function called "placeOrder" that takes in no arguments and submits
//the formatted shopping order using Ajax (some copied from code used in lab)
function placeOrder() {
    //calls the above function, formatOrder
    formatOrder();
    //directs to the url where the php file is saved
    var url = "http://cs.wellesley.edu/~istyslin/assign9mail-script.php";

    //initializes variables and gets input from the text fields created in the HTML
    var name = $("#customer").val();
    var email = $("#email").val();
    var subject = name + "placed an order.";
    var body = $("#summary").val();
    //initializes the variable to save all the above in a way Ajax will understand
    var what = {from_name: name,
               from_email: email,
               subject: subject,
               body: body};
    //posts it
    $.post(url, what, orderResponse, 'json');
}

//task3: function called "orderResponse" that takes in a variable "responseObj".
//this is taken from the lab and basically creates a message that informs the user
//that their form was submitted correctly
function orderResponse(responseObj) {
    //console.log("response is "+responseObj.status+" and "+responseObj.text); //testing
    if( responseObj.status == "ok" ) {
       $("#response_element").html("Your order has been placed!").css("color","green");
    }
}

//task4: event handlers for all the buttons creeated in the html
$("#button").click(placeOrder); //places the order
$("#scarf_button").click(formatOrder); //calls the first function (Task 1)
$("#hat_button").click(formatOrder); //calls the first function (Task 1)
$("#glove_button").click(formatOrder); //calls the first function (Task 1)
