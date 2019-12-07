/*
FILE NAME: assign7.js
WRITTEN BY: Isabelle Styslinger and Christina Pollalis
DATE: 4 November 2015
PURPOSE: This is the javascript file for homework 7, it is adapted from the
lab files
*/

//this puts the event handler on the button in the madlibs code (html file)
  $('#button1').click(makeMadLib);


// The below function is the one that takes the values from the text fields
// and assigns them to variables. it then passes in the values in the mad libs story
// below
function makeMadLib() {
    //saves the input in variables
    var noun = $('input[name=noun]').val();
    //testing: console.log("noun is: "+ noun);
    var object = $('input[name=object]').val();
    var adjective = $('input[name=adjective]').val();
    var adverb = $('input[name=adverb]').val();



    //uses the above variables to edit the html and make the story
    $('.noun').html(noun);
    $('.object').html(object);
    $('.adjective').html(adjective);
    $('.adverb').html(adverb);

  }


// This function is used to calculate the bit depth. It takes the number of colors as
// a parameter and then uses conditionals to determine the bit depth.
 function getBitDepth(numColors) {
    var bits; //creates the variable to store the bit depth
    if (numColors>=1 && numColors<=2) {
        bits=1;
    } else if (numColors>=3 && numColors<=4) {
        bits=2;
    } else if (numColors>=5 && numColors<=8) {
        bits=3;
    } else if (numColors>=9 && numColors<=16) {
        bits=4;
    } else if (numColors>=17 && numColors<=32) {
        bits=5;
    } else if (numColors>=33 && numColors<=64) {
        bits=6;
    } else if (numColors>=65 && numColors<=128) {
        bits=7;
    } else {
        bits=8;
    }
    //returns the bit depth
    return bits;
 }

// This function calculates the filesize and takes in the width, height, and number
// of colors as parameters
 function indexedFileSize(width, height, numColors) {
     //creates all the variables to store the information as calculations occur
     var colorTableSize = numColors * 3;
     var totalPixels = width*height;
     var bits = getBitDepth(numColors);
     var bytes = (totalPixels * bits)/8;
     var totalSize = colorTableSize + bytes;
     return totalSize; //returns the final result
 }

// This attaches the button from the tomthumb html file to the function calculateSize
// below (that calls the other functions and makes the correct message appear)
 $('#button2').click(calculateSize);

// This function calls the other two functions (that calculate the file size) and
// displays the correct message depending on the size of the image
 function calculateSize() {
    //testing: console.log("i am in here");
    var width = parseInt($('input[name=width]').val());
    var height = parseInt($('input[name=height]').val());
    var colors = parseInt($('input[name=colors]').val());
    
    var size = indexedFileSize(width, height, colors);
    var sizeBytes = size/1000;

    if (sizeBytes<50) {
        $('#results').html("Success! Your file size is "+sizeBytes + " KB");
    } else {
        $('#results').html("Fail! Your file size is " +sizeBytes+ " KB");
    }

 }
