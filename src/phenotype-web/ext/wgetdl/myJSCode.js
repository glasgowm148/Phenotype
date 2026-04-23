/*
FILENAME: myJSCode.js
Date: October 9th, 2015
Author: Christina Pollalis
Purpose: Skeleton of the js file in HW5 (wrote all the methods, whose descriptions
are below)
*/

// This is a sample function
function sayHello()
{
  alert('hello!!');
}

/*
Description:
Prompts the user for the number of books to order (sets the default value
of the prompt to 100)
Calculates the total price of the books ordered (the price of a single book is
$50 if the number of ordered books is less than 25 books and the price of a
single book is $40 if the number of ordered books is 25 or more books)
Reports the total price of the books to the user via the console.log() function.
*/

function calculateBookCost() {
    //initializing the variables used
    var numBooks = 100; //100 is given as the default number in the assignment
    var total_price;

    //gets the number from the user
    numBooks = parseInt(prompt("What is the number of books you want to order?"));

    if (numBooks<25) { //if th enumber of books given above is less than 25
        totalPrice = numBooks * 50;
    } else { //if the number of books is equal to or over 25
        totalPrice = numBooks * 40;
    }

    //tells the user the total price of the books:
    console.log("The total price of the books is $" + totalPrice);
} //closes method

/*
Description:
Prompts the user for the current time by asking for:
1. Hour which is the hour of the day, using a 24-hour clock, where 0 is the hour
just after midnight, 1 is 1am, ... 12 is noon, 13 is 1pm ... 22 is 10pm, and
23 is 11pm.
2. Minute which is the minute of the hour, an integer from 0 to 59.
Then, it decides on the message to show the user according to the time of day:
-The "Kitchen is closed" message appears on the web page starting at 12:00 AM,
up to but not including 8:00 AM.
-The "Breakfast is being served" message appears when visited during breakfast
hours, starting at 8:00 AM, up to but not including 11:30 AM.
-The "Lunch is being served" message appears when the page is visited during
lunch hours, starting at 11:30 AM, up to but not including 4:00 PM (4pm=16).
-The "Dinner is being served" message appears when the page is visited during
dinner hours, starting at 4:00 PM (1600), up to but not including 12:00 AM of the next day.
Reports the right message to the user via the console.log() function.
*/

function MealTime(){
    //initializing variables (could be done later as well, but looks cleaner
    //like this)
    var hour;
    var minute;
    var time;

    //prompts the user for what hour and minute of the day it is
    hour = prompt("What is the hour of the day (using a 24-hour clock, 0-23)?");
    minute = prompt("What is the minute of the hour (0-59)");
    if (minute.length==1) { //this is done so that the below conditionals will work
        minute = "0"+minute;
    }
    //computes the whole time
    time = hour + minute;
    //console.log("time is: " + time); //this was used for testing

    if (time>=0 && time<=759) {
        console.log("Kitchen is closed");
    } else if (time>=800 && time<=1129) {
        console.log("Breakfast is being served");
    } else if (time>=1130 && time<=1559) {
        console.log("Lunch is being served");
    } else {
        console.log("Dinner is being served");
    }

} //closes the method

/*
Description:
Prompts the user for the image details by asking for:
pixNum which is the total number of pixels in the image.
colorNum which is the total number of colors in the image.
Then, it calculates the bit depth of the colors in the image,
calculates the size of the color table, and
calculates the total size of the compressed image.
Then, it reports those values to the user.
Lastly, depending on the size of the image, it will tell the user if it is too large
or if it if just fine.
*/

function ImageSize(){
    //initializing variables (this could again be done in the next step, but
    //this look cleaner)
    var pixNum;
    var colorNum;
    var bitDepth;
    var sizeColorTable;
    var totalSize;
    var pixelBytes; //used to calculate the total size of the image

    //prompting the user for the information:
    pixNum = parseInt(prompt("Which is the total number of pizels in the image?"));
    colorNum = parseInt(prompt("Which is the total number of colors in the image?"));

    //calculating the bit depth of the colors in the image:
    //(all these equations are taken from the readings)

    //i tried to use this equation: ceiling(log(#colors)/log(2)) = bit depth
    //but, it did not recognize log or ceiling so I did it with conditionals:
    if (colorNum>=1 && colorNum<=2) {
        bitDepth = 1;
    } else if (colorNum>=3 && colorNum<=4) {
        bitDepth = 2;
    } else if (colorNum>=5 && colorNum<=8) {
        bitDepth = 3;
    } else if (colorNum>=9 && colorNum<=16) {
        bitDepth = 4;
    } else if (colorNum>=17 && colorNum<=32) {
        bitDepth = 5;
    } else if (colorNum>=33 && colorNum<=64) {
        bitDepth = 6;
    } else if (colorNum>=65 && colorNum<=128) {
        bitDepth = 7;
    } else if (colorNum>=129 && colorNum<=256) {
        bitDepth = 8;
    } else {
        console.log("Please input a correct value between 1-256");
    }

    //calculating things
    sizeColorTable = colorNum * bitDepth;

    pixelBytes = pixNum * bitDepth/8;
    totalSize = pixelBytes + sizeColorTable;

    //reporting these values to the user
    console.log("The bit depth is: " + bitDepth);
    console.log("The size of the color table is: " + sizeColorTable);
    console.log("The total size of the image is: " + totalSize);

    //reports back to the user if the image is too large (>100KB = 100000Bytes)
    if (totalSize>100000) {
        console.log("Image is too large.");
    } else {
        console.log("Image is just fine.");
    }

} //closes the method
