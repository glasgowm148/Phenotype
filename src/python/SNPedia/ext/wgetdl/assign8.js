// Filename: assign8.js
// Purpose: Javascript functions for the rock paper scissors assignment.
// Created: November 13, 2015
// Authors: Christina Pollalis and Isabelle Styslinger

// the array used for random elt
var choices = ["rock", "paper", "scissors"];

// this function takes in the player's choice and the computer's choice and
// determines who won (returns 0 if tie, 1 if player won, and 2 if computer won)
function rpsJudge(playerChoice, computerChoice) {
    if (playerChoice==computerChoice) {
        return 0;
    } else if (playerChoice=="rock" && computerChoice=="paper") {
        return 2;
    } else if (playerChoice=="paper" && computerChoice == "rock") {
        return 1;
    } else if (playerChoice=="scissors" && computerChoice == "rock") {
        return 2;
    } else if (playerChoice=="rock" && computerChoice == "scissors") {
        return 1;
    } else if (playerChoice=="paper" && computerChoice == "scissors") {
        return 2;
    } else if (playerChoice=="scissors" && computerChoice=="paper") {
        return 1;
    } else {
        console.log("you guys messed up somewhere");
    }
}

// this function takes in the player's choice and highlights it by putting a
// blue border around the image
function highlightPlayerChoice(playerChoice) {
    if (playerChoice == "rock") {
        $("#rock").css("border", "5px solid blue"); //makes the border blue
    } else if (playerChoice == "scissors") {
        $("#scissors").css("border", "5px solid blue"); //makes the border blue
    } else if (playerChoice == "paper") {
        $("#paper").css("border", "5px solid blue"); //makes the border blue
    }
}

// this function takes in the computer's choice and changes the carousel to show
// the right image through the animation code that we saw in class
function animateComputerChoice(computerChoice) {
    console.log("computer choice is: " + computerChoice);
    $("#cChoice").attr("src","images/"+computerChoice+"-200.png");
    // the below code changes the view point by -800px, which would show the last image
    $("#slides4 ul").animate({left: "-800px"}, 2000);
}

// this is the event handler for the button "play again". it gets connected to the
// function below that resets the game
$('#play').click(resetRPS);

// this function resets the game by making the borders white again, animating
// the slideshow to show the question mark, and changing the results div to be empty
// again
function resetRPS() {
    console.log("clicking the play");
    $("#rock").css("border", "1px solid white");
    $("#scissors").css("border", "1px solid white");
    $("#paper").css("border", "1px solid white");

    //shows the question mark
    $("#slides4 ul").animate({left: "0px"}, 2000);

    //makes the results div empty again (so that it doesn't show who won in the
    //previous round)
    $("#results").html("");
}

// the event handlers for the three images in the playe's section (when clicked, they
// call a function that then calls the playerTurn function with the appropriate
// player choice)
$('#rock').click(playedRock);
$('#scissors').click(playedScissors);
$('#paper').click(playedPaper);

// the below three functions all call the playerTurn function with the appropriate
// player choice (based on which image they are attached to above)
function playedRock() {
    playerTurn("rock");
}

function playedScissors() {
    playerTurn("scissors");
}

function playedPaper() {
    playerTurn("paper");
}

// this function takes in the player choice makes everything work and puts everything
// together.
// it first resets the game by calling resetRPS().
// then, it highlights the player choice by passing in the playerChoice given in the function.
// then, it finds the computer's choice by calling the random elt function and through that,
// animates the computer choice.
// then, it finds out the winner by calling rpsJudge and based on who is the winner,
// displays a different result to the user by dynamically changing the results div.
function playerTurn(playerChoice) {
    //console.log("play again!!"); //testing
    resetRPS(); //resets the game
    highlightPlayerChoice(playerChoice); //highlights player's choice
    var computerChoice = randomElt(choices); //finds computer's choice
    //console.log(computerChoice); //testing
    animateComputerChoice(computerChoice); //animates the computer choice found above
    var winnerNum = rpsJudge(playerChoice, computerChoice); //finds out the winner
    var winner; //creates a variable to store the appropriate string based on who is the winner

    //based on what the rpsJudge function returns, creates the appropriate string
    if (winnerNum==0) {
        winner = "It's a tie!";
    } else if (winnerNum==1) {
        winner = "Player wins!";
    } else if (winnerNum==2) {
        winner = "Computer wins!";
    }
    //console.log(winner);  //testing
    $("#results").html(winner); //dynamically changes the results div
}
