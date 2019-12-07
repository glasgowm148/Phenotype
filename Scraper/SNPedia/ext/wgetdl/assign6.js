// Filename: assign6.html
// Purpose: HTML page for "What's cooking?" assignment.
// Created: March 20, 2014
// Author: Eni Mustafaraj
//
// Modified by: Christina Pollalis
// Modification Date: October 28th 2015


//TASK 1:
//The below function, makeDate takes in an argument that is either the word "now" or
//the complete specification of a date and time, like "3/31/2015 9:45 am"
//The function returns a date object for that time, where "now" returns a date
//object for the current time.
function makeDate(time) {
    if (time=="now") {
        return new Date(); //returns a new date object of the current time
        //console.log("date is: "+ date); //used for testing
    } else {
        return new Date(time); //returns a new date object of the time given
    }
}

// TASK 2:
// The below function, findMealName takes a Date object as its input argument.
// The function returns the name of the meal for that date and time. Meaning:
// If the current day is Saturday or Sunday: the kitchen is "Closed"
// If the current day is a weekday (Monday - Friday), depending on the time:
// Return "Breakfast", between 8:30-11:30AM
// Return "Lunch", between 12:30-3:15PM
// Return "Dinner", between 6:00PM -10:00PM
// Return "Closed", at any other time
function findMealName(date) {
    //initialize all the variables below:
    var day = date.getDay();
    var string = ""; //to save what I will be returning
    var hours = date.getHours();
    var minutes = ""+date.getMinutes(); //by putting "", it makes into string
    //console.log("DATE: "+ date); //used for testing
    //console.log("HOURS: "+hours); //used for testing

    if (minutes.length==1) { //if minutes is <10, need to add a 0 before
        minutes = "0" + minutes;
    }

    var time = hours +""+ minutes; //this makes it into a string
    //console.log("time is: " + time); //for testing

    if (day==0 || day==6) { //0 is Sunday, 6 is Saturday
        string = "Closed";
    } else  {
        if (time>=830 && time<1130) {
            string = "Breakfast";
        } else if (time>=1230 && time<1515) {
            string = "Lunch";
        } else if (time>=1800 && time<2200) {
            string = "Dinner";
        } else {
            string = "Closed";
        }
    }
    return string; //returns the final result
}

//TASK 3:
//The below function, formatDateTime takes in a date object as an argument.
//It aims to display that date in this format: 10/23 at 1:03 pm
//It does this by extracting elements from the date object and manipulating them
function formatDateTime(date) {
    //initialize variables to save all the elements of the date
    var string = "";
    var month = date.getMonth(); //0=Jan, 1=Feb, ..., 11=Dec
    var dateDay = date.getDate(); //1 to 31
    var hours = date.getHours(); //0 to 23
    var minutes = ""+date.getMinutes(); //0 to 59 + makes it into a string
    var ampm = ""; //to save either "am" or "pm"
    //console.log(date); //for testing
    //console.log("this is month: "+month); //for testing

    //the below is to make the month correct (start from 1, not 0)
    month = month+1; //it returns it in integer form (not string)

    //the below is to make the hours and the ampm correct:
    if (hours==0) {
        hours = 12;
        ampm = "am";
    } else if (hours<12) { //not including 12
        ampm = "am"; //the hours do not need to be manipulated
    } else if (hours==12) {
        ampm = "pm"; //the hours do not need to be manipulated
    } else {
        hours = hours-12;
        ampm= "pm";
    }

    //the below is to make the minutes correct if they are <10:
    if (minutes.length == 1) {
        minutes = "0" + minutes;
    }

    //create the string in the format wanted
    string = month + "/" + dateDay + " at " + hours + ":" + minutes + " " + ampm;
    return string; //returns the string
}

// TASK 4:
// The below function is displayInfo and takes a time specification as an argument
// (either the word "now" or the complete specification of a date and time)
// The function then:
// Uses the makeDate function to turn the time specification into a date object.
// Uses the date object and the findMealName function to determine the meal name,
// and insert that name into the page in the element whose ID is meal.
// Uses the date object and the formatDateTime function to get a nicely formatted
// string for the date and insert that string into the page in the element whose
// ID is time.
function displayInfo(time) {
    var date = makeDate(time); //calls the first method and saves the output in a var
    var stringName = findMealName(date); //uses the above var to call the second method
    //console.log("stringName: " +stringName); //for testing

    //setting the string above as the html of the element whose id is "meal"
    document.querySelector("#meal").innerHTML=stringName;
    //below displays the image (for extra credit)
    displayMealPicture(stringName);

    //does the same as above, but for the date string (using the third method)
    var stringDate = formatDateTime(date);
    //console.log("stringDate: " +stringDate); //for testing

    //setting the string above as the html of the element whose id is "time"
    document.querySelector("#time").innerHTML=stringDate;
}

// Extra credit:
// The below function, named displayMealPicture that takes a string argument
// (mealName), as returned by findMealName function ("Closed", "Breakfast", ..),
// and inserts an IMG element (a chunk of HTML code) into the page in the element
// whose ID is picture.
// The IMG element is in the image folder
function displayMealPicture(mealName) {
    //creates a variable that is the image file name
    var image = mealName + ".jpg";
    //adjusts the html to change the source of the image and display the correct image
    document.querySelector("#picture").innerHTML="<img src='images/" + image + "'>";
}
