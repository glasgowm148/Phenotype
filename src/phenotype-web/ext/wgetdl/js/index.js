// Dimensions of sunburst.
var width = 870/2;
var height = 480;
var radius = Math.min(width, height) / 2;

/*How to order: Pathogenic, Protective, Pharma, Benign, (first affected, then carrier (sorted by size))*/

d3.csv("test1.csv", function(data1) {
  d3.csv("test2.csv", function(data2) {

    //More will be added in the forEach functions below
    var colors = {
      "": "white",
      "Jessie": "url(#Jessie)",
      "Jamie": "url(#Jamie)"

    };


    /*THE FIRST DATA FROM THE FIRST CSV:*/
    var objectArray1 = []; 
    var allObjects = []; //this array will hold all the variants (so that there is one that has everything)

    //This is where the rectangles get the information passed through from the csv file
    data1.forEach(function(d){

      /* THE BELOW CODE determines the size (taken from Clarissa's code):*/
      var varSize; //create a variable to hold size value
      if (d.frequency == "" || d.frequency == "1.0"){
        d.frequency = 0.9;
      }
    
      varSize = -Math.log(d.frequency);
      if (varSize < 1){
        varSize = 0.8;
      }

      //initialize the variable to hold the name
      var variantName = d.variant;
      var categories = d.category.split(";"); // this array will hold all the categories

      /*THE BELOW CODE adds to the colors array based on what the variant name is:*/
      if (d.impact == "Protective") { 
        colors[variantName]= "#89b4fd";
      } else if (d.impact == "Benign") {
        colors[variantName]= "#cccccc";
      } else if (d.impact == "Pathogenic") {
        colors[variantName]= "#ff6666";
      } else if (d.impact == "NotPresent") {
        colors[variantName]= "#white";
      } /*End of code determining color*/

      /* THE BELOW CODE determines if they are a carrier and if yes, then sets the color to be the diagonal thing*/
      var carrierStatus = false; //the default
      if (d.zygosity == "Heterozygous" && d.inheritance == "Recessive") {
        carrierStatus = true; //it is a carrier! 
        if (d.impact == "Pathogenic"){
          colors[variantName] = "url(#PathDiag)";
        }
        if (d.impact == "Protective"){
          colors[variantName] = "url(#ProtDiag)";
        }
        if (d.impact == "Benign" || d.impact == "Not Reviewed"){
          colors[variantName] = "url(#BenDiag)";
        }
        if (d.impact == "Pharmacogenetic"){
          colors[variantName] = "url(#PathDiag)"; //this should be different
        } else if (d.impact == "Not Reviewed" || (d.inheritance == "Unknown" || d.inheritance == "Complex/Other")) { //probably don't include these (ask madeleine)
        colors[variantName] = "green";
        } 
      } /*End of code determining whether variant is carrier*/


      //the object:
      var object = {
        name: d.variant, //this variable is unique
        jamieHas: true, //since it is the first person
        jessieHas: false, //this might change later
        isVisible: true, //all start as visible at the beginning
        size: varSize, //passes in the size determined above
        summary: d.summary,
        certainty_of_evidence: d.evidence,
        health_effect: d.clinical_importance,
        impact: d.impact,
        rarity: -Math.log(d.frequency),
        carrier: carrierStatus,
        color: colors[d.variant], //doesn't work?
        category: categories //will need to break this up based on commas later (parsing later)
      }; /*closes object*/

      objectArray1.push(object); //pushes the object to the array
      allObjects.push(object);

    }); //closing of for each for DATA1



    /*THE SECOND DATA FROM THE SECOND CSV*/
    var array2 = [];
    var size2 = [];
    var objectArray2 = [];


    //This is where the SECOND information gets passed through from the csv file
    data2.forEach(function(d){

      //re-initialize this variable
      var variantName = d.variant;
      var categories = d.category.split(";"); // this array will hold all the categories

       /* THE BELOW CODE determines the size (taken from Clarissa's code):*/
      var varSize; //create a variable to hold size value (re-initialize from above)
      
      if (d.frequency == "" || d.frequency == "1.0"){
          d.frequency = 0.9;
      }
      
      varSize = -Math.log(d.frequency);
      if (varSize < 1){
          varSize = 0.8;
      }

      /*THE BELOW CODE adds to the colors array based on what the variant name is:*/
      if (d.impact == "Protective") { 
        colors[variantName]= "#89b4fd";
      } else if (d.impact == "Benign") {
        colors[variantName]= "#cccccc";
      } else if (d.impact == "Pathogenic") {
        colors[variantName]= "#ff6666";
      } else if (d.impact == "NotPresent") {
        colors[variantName]= "#white";
      } /*End of code determining color*/

      /* THE BELOW CODE determines if they are a carrier and if yes, then sets the color to be the diagonal thing*/
      var carrierStatus = false; //the default
      if (d.zygosity == "Heterozygous" && d.inheritance == "Recessive") {
        carrierStatus = true; //it is a carrier! 
        if (d.impact == "Pathogenic"){
          colors[variantName.toString()] = "url(#PathDiag)";
        }
        if (d.impact == "Protective"){
          colors[variantName.toString()] = "url(#ProtDiag)";
        }
        if (d.impact == "Benign" || d.impact == "Not Reviewed"){
          colors[variantName.toString()] = "url(#BenDiag)";
        }
        if (d.impact == "Pharmacogenetic"){
          colors[variantName.toString()] = "url(#PathDiag)"; //this should be different
        } else if (d.impact == "Not Reviewed" || (d.inheritance == "Unknown" || d.inheritance == "Complex/Other")) { //probably don't include these (ask madeleine)
        colors[variantName.toString()] = "green";
        } 
      } /*End of code determining whether variant is carrier*/

      /*insert while trying to make an array of objects for simpler code:*/
      //the object:
      var object = {
        name: d.variant, //this variable is unique
        jamieHas: false, //since it is the first person
        jessieHas: true, //this might change later
        isVisible: true, //all start as visible at the beginning
        size: varSize, //passes in the size determined above
        summary: d.summary,
        certainty_of_evidence: d.evidence,
        health_effect: d.clinical_importance,
        impact: d.impact,
        rarity: -Math.log(d.frequency),
        carrier: carrierStatus,
        color: colors[d.variant], //doesn't work?
        category: categories //will need to break this up based on commas later
      }; /*closes the object*/

      objectArray2.push(object); //pushes the object to the array
      allObjects.push(object); //add it to array that has all
      /*end of insert*/
      
    }); //closing for each




    // Total size of all segments; we set this later, after loading the data.
    var totalSize = 0; 

    var svgContainer = d3.select("body").append("svg");

    
    var partition = d3.layout.partition()
      .size([2 * Math.PI, radius * radius]) 
      .value(function(d) { return d.size; }) //this is where the sorting happens based on size
      .sort(null); //this makes it not sort! (before - default is by size)

    var vis = d3.select("#chart").append("svg:svg")
      .attr("width", width)
      .attr("height", height)
      .append("svg:g")
      .attr("id", "container")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");


     var arc = d3.svg.arc() //the below places them in space
      .startAngle(function(d) { return d.x; })
      .endAngle(function(d) { return d.x + d.dx; })
      .innerRadius(function(d) { return Math.sqrt(d.y); })
      .outerRadius(function(d) { return Math.sqrt(d.y + d.dy); });


    // Use d3.text and d3.csv.parseRows so that we do not need to have a header
    // row, and can receive the csv as an array of arrays.


    //TAKEN FROM A WEBPAGE ONLINE (did not write myself), and used below to remove elements from an array
    Array.prototype.remove = function(from, to) {
      var rest = this.slice((to || from) + 1 || this.length);
      this.length = from < 0 ? this.length + from : from;
      return this.push.apply(this, rest);
    };

    /* THE BELOW CODE DETERMINES which elements are shared between the two arrays and puts all common
    elements in a new array called "commonVariants" and deletes them from the original array*/
    var aiLength = objectArray1.length; // need to save this because this will change //do we still need this??
    var biLength = objectArray2.length;


    //need to create copy arrays (and populate them with original) 
    //javascript does not allow you to just equate them (array1copy = array1) because then it links them together
    var array1copy = [];
    var array2copy = [];

    for (var i = 0; i<objectArray1.length; i++) {
      array1copy.push(objectArray1[i]);
    }

    for (var i = 0; i<objectArray2.length; i++) {
      array2copy.push(objectArray2[i]);
    }

      

    /* THIS CODE SEPERATES DIFFERENT AND COMMON VARIANTS INTO SEPERATE ARRAYS
    It puts all common elements in the array called "commonVariants"*/
    var commonArray = [];

    for (var ai=0; ai<aiLength; ai++) {
      for (var bi=0; bi<biLength; bi++) {

        if (array1copy[ai].name == array2copy[bi].name) {
          //add the common variant object to the new object array:
          commonArray.push(array1copy[ai]);
          
          //delete the common variants from the first array and the second one:
          var elementRemoveArray1 = objectArray1.indexOf(array1copy[ai]);
          objectArray1.remove(elementRemoveArray1); //will remove work for objects?

          var elementRemoveArray2 = objectArray2.indexOf(array2copy[bi]);
          objectArray2.remove(elementRemoveArray2);
        }
      }
    } /*END OF SEPERATING DIFFERENT AND COMMON VARIANTS INTO SEPERATE ARRAYS*/


    /*ALL THE BELOW CODE HAS TO DO WITH TOGGLING:*/

    //when the radio buttons get clicked: 
    d3.select("#people_button").on('click', function() { filterButton("#people_filter")});
    d3.select("#impact_button").on('click', function() { filterButton("#impact_filter")});
    d3.select("#category_button").on('click', function() { filterButton("#category_filter")});
    d3.select("#evidence_button").on('click', function() { filterButton("#evidence_filter")});
    d3.select("#clinical_button").on('click', function() { filterButton("#clinical_filter")});
    d3.select("#carrier_button").on('click', function() { filterButton("#carrier_filter")});

    //shows/hides things depending on what the menu_id is
    function filterButton(menu_id) {
      showAll(); //to reset
      d3.selectAll(".filter").style("visibility", "hidden");
      d3.selectAll(".filter").each(function() { this.value="Show All";});
      d3.selectAll(".button").each(function() { d3.select(this).style("disabled", "false");
                                                d3.select(this).style("cursor", "pointer");});
      d3.selectAll('.bubble').style('opacity', '1');
      d3.select(menu_id).style("visibility", "visible");
    }


    //adding the event listeners:
    document.getElementById("people_filter").addEventListener("change", changePerson);
    document.getElementById("impact_filter").addEventListener("change", filterImpact);
    document.getElementById("category_filter").addEventListener("change", filterCategory);
    document.getElementById("evidence_filter").addEventListener("change", filterEvidence);
    

    /*This function will show everything. It will do this by setting all the variables (in all three arrays
      to be visible */
    function showAll() {
      //first data - set all visible
      for (var i=0; i<objectArray1.length; i++) {
        objectArray1[i].isVisible = true;
      }
      //second data - set all visible
      for (var i=0; i<objectArray2.length; i++) {
        objectArray2[i].isVisible = true;
      }
      //third data - set all visible
      for (var i=0; i<commonArray.length; i++) {
        commonArray[i].isVisible = true;
      }
      makeString(); //to make and create the visualization
    } /*closes showAllfunction*/


    /*This function determines which person should appear and changes the visibility based on the choice*/
    function changePerson() {
      console.log("switching person")

      var selected = document.getElementById("people_filter")
                            .options[people_filter.selectedIndex].value;

      console.log("person is: " + selected);

      if (selected == "Show All") {
      showAll();

      } else if (selected == "p1") { //show only the first person's data (do we also want the ones that they have in common?)
        //first data - set all visible
        for (var i=0; i<objectArray1.length; i++) {
          objectArray1[i].isVisible = true;
        }
        //second data - set all not visible
        for (var i=0; i<objectArray2.length; i++) {
          objectArray2[i].isVisible = false;
        }
        //third data - set all not visible
        for (var i=0; i<commonArray.length; i++) {
          commonArray[i].isVisible = false;
        }
      } else if (selected == "p2") { //show only the second person's data (do we also want the ones that they have in common?)
        //first data - set all not visible
        for (var i=0; i<objectArray1.length; i++) {
          objectArray1[i].isVisible = false;
        }
        //second data - set all visible
        for (var i=0; i<objectArray2.length; i++) {
          objectArray2[i].isVisible = true;
        }
        //third data - set all not visible
        for (var i=0; i<commonArray.length; i++) {
          commonArray[i].isVisible = false;
        }
      } else if (selected == "shared") { //show only common variants
        //first data - set all not visible
        for (var i=0; i<objectArray1.length; i++) {
          objectArray1[i].isVisible = false;
        }
        //second data - set all not visible
        for (var i=0; i<objectArray2.length; i++) {
          objectArray2[i].isVisible = false;
        }
        //third data - set all visible
        for (var i=0; i<commonArray.length; i++) {
          commonArray[i].isVisible = true;
        }
      }
      makeString();
    } /*closes setPerson function*/



    function filterEvidence() {

    if (document.getElementById("evidence_filter")
            .options[evidence_filter.selectedIndex].value == "Show All") {
      showAll();

    } else {

        var selected = document.getElementById("evidence_filter")
                            .options[evidence_filter.selectedIndex].value;
        //first data:
        for (var i=0; i<objectArray1.length; i++) {
          if (objectArray1[i].certainty_of_evidence == selected) { //do I need to pass "type" in differently?
            objectArray1[i].isVisible = true;
          } else {
            objectArray1[i].isVisible = false;
          }
        }
        //second data:
        for (var i=0; i<objectArray2.length; i++) {
          if (objectArray2[i].certainty_of_evidence == selected) {
            objectArray2[i].isVisible = true;
          } else {
            objectArray2[i].isVisible = false;
          }
        }
        //third data:
        for (var i=0; i<commonArray.length; i++) {
          if (commonArray[i].certainty_of_evidence == selected) {
            commonArray[i].isVisible = true;
          } else {
            commonArray[i].isVisible = false;
          }
        } //closes third data                     
      } //closes !=all
      makeString();
    }

    function filterCategory() {

      if (document.getElementById("category_filter")
              .options[category_filter.selectedIndex].value == "Show All") {

          showAll();

      } else {

          var selected = document.getElementById("category_filter")
                              .options[category_filter.selectedIndex].value;
          //first data:
        for (var i=0; i<objectArray1.length; i++) {
          for (var j=0; j<objectArray1[i].category.length; j++) {
            //console.log("LENGTH: " + objectArray1[i].category.length); // for testing purposes
            if (objectArray1[i].category[j] == selected) { //do I need to pass "type" in differently?
              objectArray1[i].isVisible = true;
            } else {
              objectArray1[i].isVisible = false;
            }
          }
        }
        //second data:
        for (var i=0; i<objectArray2.length; i++) {
          for (var j=0; j<objectArray2[i].category.length; j++) {
            if (objectArray2[i].category[j] == selected) { //do I need to pass "type" in differently?
              objectArray2[i].isVisible = true;
            } else {
              objectArray2[i].isVisible = false;
            }
          }
        }
        //third data:
        for (var i=0; i<commonArray.length; i++) {
          for (var j=0; j<commonArray[i].category.length; j++) {
            if (commonArray[i].category[j] == selected) { //do I need to pass "type" in differently?
              commonArray[i].isVisible = true;
            } else {
              commonArray[i].isVisible = false;
            }
          }
        } //closes third data

      } //closes !=all
      makeString();
    }


    function filterImpact() {

      if (document.getElementById("impact_filter")
              .options[impact_filter.selectedIndex].value == "Show All") { //shows all

          showAll();
      } else {

        var selected = document.getElementById("impact_filter")
                              .options[impact_filter.selectedIndex].value;

        //first data:
        for (var i=0; i<objectArray1.length; i++) {
          if (objectArray1[i].impact == selected) { //do I need to pass "type" in differently?
            objectArray1[i].isVisible = true;
          } else {
            objectArray1[i].isVisible = false;
          }
        }
        //second data:
        for (var i=0; i<objectArray2.length; i++) {
          if (objectArray2[i].impact == selected) {
            objectArray2[i].isVisible = true;
          } else {
            objectArray2[i].isVisible = false;
          }
        }
        //third data:
        for (var i=0; i<commonArray.length; i++) {
          if (commonArray[i].impact == selected) {
            commonArray[i].isVisible = true;
          } else {
            commonArray[i].isVisible = false;
          }
        } //closes third data
          
      } //closes !=all

      makeString();
    }

    /*The below function changes all toggles, except for the person one.
    It does this by switching the visibility depending on what type or choice
    is passed into the function.*/
    // function changeToggle(type, choice) {
    //   console.log("type is: " + type);
    //   console.log("choice is: " + choice);
    //   //resetting dropdown, based on what the type is: 
    //   if (type=="certainty_of_evidence") {
    //     $('#people').val("all");
    //     $('#effect').val("all");
    //     $('#category').val("all");
    //   } else if (type=="health_effect") {
    //     $('#people').val("all");
    //     $('#certOfEvidence').val("all");
    //     $('#category').val("all");
    //   } else {
    //     console.log("SOMETHING WENT WRONG WHEN PASSING IN VALUES!!!"); //error checking
    //   }
     
    //   if (choice == "all") {
    //     //sets all to visible (can just call the above function)
    //     showAll();
    //   } else {
    //     //first data:
    //     for (var i=0; i<objectArray1.length; i++) {
    //       if (objectArray1[i].type == choice) { //do I need to pass "type" in differently?
    //         objectArray1[i].isVisible = true;
    //       } else {
    //         objectArray1[i].isVisible = false;
    //       }
    //     }
    //     //second data:
    //     for (var i=0; i<objectArray2.length; i++) {
    //       if (objectArray2[i].type == choice) {
    //         objectArray2[i].isVisible = true;
    //       } else {
    //         objectArray2[i].isVisible = false;
    //       }
    //     }
    //     //third data:
    //     for (var i=0; i<commonArray.length; i++) {
    //       if (commonArray[i].type == choice) {
    //         commonArray[i].isVisible = true;
    //       } else {
    //         commonArray[i].isVisible = false;
    //       }
    //     } //closes third data
    //   } // closes !="all"
    //   makeString();
    // } /*closes changeToggle function*/

  
    /*The below function creates the string that will then be used to actually
    make the visualization (passes through each of the arrays so that it is ordered 
    correctly.*/
    function makeString() {

    console.log("making it into a string..."); //testing purposes
    
    //need to eliminate previous text string that was created and empty the container
    text = ""; 
    $("#container").empty();

    //CONSTRUCTING THE TEXT STRING TO SHOW THE DATA:
    //adding in the names: 
    //text+= "Jessie" + ";" + "Jamie" + "," + "10" + "\n";
    //DATA 1:
    //1. All the Pathogenic variants for data 1
    for (var i = 0; i<objectArray1.length; i++) { 
        if (objectArray1[i].impact == "Pathogenic" && objectArray1[i].carrier == false && objectArray1[i].isVisible == true) { 
          text +=  objectArray1[i].name + ";" + "," + objectArray1[i].size + "\n"; 
        }
    }
      //2. All the Pathogenic Carrier variants for data 1
      for (var i = 0; i<objectArray1.length; i++) { 
        if (objectArray1[i].impact == "Pathogenic" && objectArray1[i].carrier == true && objectArray1[i].isVisible == true) {
          text +=  objectArray1[i].name + ";" + "," + objectArray1[i].size + "\n"; 
        }
      }
      //3. All the Protective variants for data 1
      for (var i = 0; i<objectArray1.length; i++) { 
        if (objectArray1[i].impact == "Protective" && objectArray1[i].carrier == false && objectArray1[i].isVisible == true) { 
          text +=  objectArray1[i].name + ";" + "," + objectArray1[i].size + "\n"; 
        }
      }
      //4. All the Protective Carrier variants for data 1
      for (var i = 0; i<objectArray1.length; i++) { 
        if (objectArray1[i].impact == "Protective" && objectArray1[i].carrier == true && objectArray1[i].isVisible == true) { 
          text +=  objectArray1[i].name + ";" + "," + objectArray1[i].size + "\n"; 
        }
      }
      //5. All the Benign variants for data 1
      for (var i = 0; i<objectArray1.length; i++) { 
        if (objectArray1[i].impact == "Benign" && objectArray1[i].carrier == false && objectArray1[i].isVisible == true) { 
          text +=  objectArray1[i].name + ";" + "," + objectArray1[i].size + "\n"; 
        }
      }
      //6. All the Benign Carrier variants for data 1
      for (var i = 0; i<objectArray1.length; i++) { 
        if (objectArray1[i].impact == "Benign" && objectArray1[i].carrier == true && objectArray1[i].isVisible == true) { 
          text +=  objectArray1[i].name + ";" + "," + objectArray1[i].size + "\n"; 
        }
      }

      //DATA 2:
      //1. All the Pathogenic variants for data 1
      for (var i = 0; i<objectArray2.length; i++) { 
        if (objectArray2[i].impact == "Pathogenic" && objectArray2[i].carrier == false && objectArray2[i].isVisible == true) { 
          text +=  objectArray2[i].name+i.toString() + ";" + objectArray2[i].name + "," + objectArray2[i].size + "\n"; 
        }
      }
      //2. All the Pathogenic Carrier variants for data 1
      for (var i = 0; i<objectArray2.length; i++) { 
        if (objectArray2[i].impact == "Pathogenic" && objectArray2[i].carrier == true && objectArray2[i].isVisible == true) {
          text += objectArray2[i].name+i.toString() + ";" + objectArray2[i].name + "," + objectArray2[i].size + "\n"; 
        }
      }
      //3. All the Protective variants for data 1
      for (var i = 0; i<objectArray2.length; i++) { 
        if (objectArray2[i].impact == "Protective" && objectArray2[i].carrier == false && objectArray2[i].isVisible == true) {
          text +=  objectArray2[i].name+i.toString() + ";" + objectArray2[i].name + "," + objectArray2[i].size + "\n"; 
        }
      }
      //4. All the Protective Carrier variants for data 1
      for (var i = 0; i<objectArray2.length; i++) { 
        if (objectArray2[i].impact == "Protective" && objectArray2[i].carrier == true && objectArray2[i].isVisible == true) { 
          text +=  objectArray2[i].name+i.toString() + ";" + objectArray2[i].name + "," + objectArray2[i].size + "\n"; 
        }
      }
      //5. All the Benign variants for data 1
      for (var i = 0; i<objectArray2.length; i++) { 
        if (objectArray2[i].impact == "Benign" && objectArray2[i].carrier == false && objectArray2[i].isVisible == true) { 
          text +=  objectArray2[i].name+i.toString() + ";" + objectArray2[i].name + "," + objectArray2[i].size + "\n"; 
        }
      }
      //6. All the Benign Carrier variants for data 1
      for (var i = 0; i<objectArray2.length; i++) { 
        if (objectArray2[i].impact == "Benign" && objectArray2[i].carrier == true && objectArray2[i].isVisible == true) { 
          text +=  objectArray2[i].name+i.toString() + ";" + objectArray2[i].name + "," + objectArray2[i].size + "\n"; 
        }
      }
      //SHARED:
      //1. All the Pathogenic variants for data 1
      for (var i = 0; i<commonArray.length; i++) { 
        if (commonArray[i].impact == "Pathogenic" && commonArray[i].carrier == false && commonArray[i].isVisible == true) { 
          text +=  commonArray[i].name + ";" + commonArray[i].name + "," + commonArray[i].size + "\n"; 
        }
      }
      //2. All the Pathogenic Carrier variants for data 1
      for (var i = 0; i<commonArray.length; i++) { 
        if (commonArray[i].impact == "Pathogenic" && commonArray[i].carrier == true && commonArray[i].isVisible == true) {
          text +=  commonArray[i].name + ";" + commonArray[i].name + "," + commonArray[i].size + "\n"; 
        }
      }
      //3. All the Protective variants for data 1
      for (var i = 0; i<commonArray.length; i++) { 
        if (commonArray[i].impact == "Protective" && commonArray[i].carrier == false && commonArray[i].isVisible == true) { 
          text +=  commonArray[i].name + ";" + commonArray[i].name + "," + commonArray[i].size + "\n"; 
        }
      }
      //4. All the Protective Carrier variants for data 1
      for (var i = 0; i<commonArray.length; i++) { 
        if (commonArray[i].impact == "Protective" && commonArray[i].carrier == true && commonArray[i].isVisible == true) { 
          text +=  commonArray[i].name + ";" + commonArray[i].name + "," + commonArray[i].size + "\n"; 
        }
      }
      //5. All the Benign variants for data 1
      for (var i = 0; i<commonArray.length; i++) { 
        if (commonArray[i].impact == "Benign" && commonArray[i].carrier == false && commonArray[i].isVisible == true) { 
          text +=  commonArray[i].name + ";" + commonArray[i].name + "," + objectArray2[i].size + "\n";  
        }
      }
      //6. All the Benign Carrier variants for data 1
      for (var i = 0; i<commonArray.length; i++) { 
        if (commonArray[i].impact == "Benign" && commonArray[i].carrier == true && commonArray[i].isVisible == true) {
          text +=  commonArray[i].name + ";" + commonArray[i].name + "," + commonArray[i].size + "\n"; 
        }
      }

      //console.log("Text is: " + text);

      //creates the visualization (toggle should change here depending on text)
      var csv = d3.csv.parseRows(text);
      var json = buildHierarchy(csv);
      createVisualization(json);
    } /*Closes the function that determines which data gets displayed (clickToggle())*/


    
    /*The below function gets called once at the beginning*/
    function load() {
      showAll(); //this makes everything visible in the arrays already established
    } /*closes load function*/


    load();  //call load when the page first loads

    //call the clickToggle() function again if anything in the toggle changes
    // $("#all").on("change", alert("hi"));
    // $("#p1").on("change", alert("hi"));
    // $("#p2").on("change", alert("hi"));
    // $("#shared").on("change", alert("hi"));


    /* Main function to draw and set up the visualization, once we have the data.*/
    function createVisualization(json) {
    // Bounding circle underneath the sunburst, to make it easier to detect
    // when the mouse leaves the parent g.
    vis.append("svg:circle")
       .attr("r", radius)
       .style("opacity", 0);

    // Changed this -- we want to display ALL variants (even if it is smaller)
    var nodes = partition.nodes(json)
          .filter(function(d) {
          return (d.dx > 0.000); // changed from 0.005 radians = 0.29 degrees to 0.000 (so returns all)
          });

    var path = vis.data([json]).selectAll("path")
          .data(nodes)
          .enter().append("svg:path")
                  //.attr("transform", function(d) {return "rotate(" + (d.x + d.dx / 2 - Math.PI / 2) / Math.PI * 180 + ")";}) //Alexa's code
                  .attr("display", function(d) { return d.depth ? null : "none"; })
                  .attr("d", arc)
                  .attr("dy", 0)
                  .attr("name", function(d) {return d.name; })
                  .attr("summary", function(d) {return d.summary;})
                  .attr("certainty_of_evidence", function(d) {return d.certainty_of_evidence;})
                  .attr("health_effect", function(d) {return d.health_effect;})
                  .attr("impact", function(d) {return d.impact;})
                  .attr("rarity", function(d) {return d.rarity;})
                  .style("angularWidth", 100)
                  .style("fill", function(d) { if (colors[d.name]!=undefined) { return colors[d.name]; } else {return "white"; } })
                  .style("stroke", "#E8E8E8")//"#d3d3d3")
                  .style("stroke-width", 2)
                  //.style("stroke-dasharray", "5,5")
                  .style("opacity", 1)
                  .attr("class", function(d) { if (colors[d.name]=="white") {return "empty"}; })
                  .on("mouseover", hover)
                  .on("click", click);

    // Get total size of the tree = value of root node from partition.
    //  totalSize = path.node().__data__.value; //look
    }; /*Closes code for "CreateVisualization(json)"*/


    /*BELOW ARE THE PATTERNS for filling the carriers:
    Need to create them using images (should remake these later) and get appended to the
    whole svgContainer*/

    //the size of the pattern:
    var config = {
      "size" : 40
    }

    //the one for Jamie:
    svgContainer.append('defs')
                .append('pattern')
                .attr("id", 'Jamie')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("patternUnits", "userSpaceOnUse")
                .append("svg:image")
                .attr("xlink:href", 'jamie.png')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("x", 0)
                .attr("y", 0);

    //the one for Jessie:
    svgContainer.append('defs')
                .append('pattern')
                .attr("id", 'Jessie')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("patternUnits", "userSpaceOnUse")
                .append("svg:image")
                .attr("xlink:href", 'jessie.png')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("x", 0)
                .attr("y", 0);

    //the one for Pathogenic Carrier:
    svgContainer.append('defs')
                .append('pattern')
                .attr("id", 'PathDiag')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("patternUnits", "userSpaceOnUse")
                .append("svg:image")
                .attr("xlink:href", 'http://2.bp.blogspot.com/-QnFtbHKbeW8/U6wYza5m9dI/AAAAAAAAfOo/Ven4iGIDeXc/s1600/red_polka_dot_paper.jpg')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("x", 0)
                .attr("y", 0);

    //the one for Benign Carrier:
    svgContainer.append('defs')
                .append('pattern')
                .attr("id", 'BenDiag')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("patternUnits", "userSpaceOnUse")
                .append("svg:image")
                .attr("xlink:href", 'http://www.babybedding.com/images/fabric/white-and-gray-polka-dot-fabric_medium.jpg')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("x", 0)
                .attr("y", 0);

    //the one for Protective Carrier:
    svgContainer.append('defs')
                .append('pattern')
                .attr("id", 'ProtDiag')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("patternUnits", "userSpaceOnUse")
                .append("svg:image")
                .attr("xlink:href", 'http://www.featurepics.com/StockImage/20080825/baby-blue-polka-dots-stock-illustration-867492.jpg')
                .attr("width", config.size)
                .attr("height", config.size)
                .attr("x", 0)
                .attr("y", 0);


    //BELOW: Click and hover functions: 
    var clicked = false; //set variable clicked to false since nothing is currently clicked
    var prevClicked = ""; //create variable to store the name of the previous variable clicked

    /*The below function determines what should happen when an element is clicked*/
    function click(d) {
      //console.dir(this);
      //console.log("I clicked"); //for testing purposes
      if (clicked == false) { //nothing has been clicked yet

      //we need to save the name of the variable that was just clicked: 
      console.log("You just clicked: " + this.__data__.name);
      prevClicked = this.__data__.name; 

      //the below code is copied from the mouseover one that existed before
      //remove outlining from all segments 
      var sequenceArray = getAncestors(d);
      d3.selectAll("path")
        .style("stroke-width", 2)
        .style("stroke", "#E8E8E8");


      //Then highlight only those that are an ancestor of the current segment.
      vis.selectAll("path")
         .filter(function(node) {
            return (sequenceArray.indexOf(node) >= 0);
                  })
          .style("stroke-width", 2)
          .style("angularWidth", 0.2)
          .style("stroke", "yellow");

      //something is now clicked so we need to update clicked
      clicked = true; 

      show_details(this); //calls function that will make the information appear on the accordion

    } else { //clicked is true (so something is clicked)

        // in either of the below case, we need to remove all the highlighting from all the segments:
          var sequenceArray = getAncestors(d);
          d3.selectAll("path")
            .style("stroke-width", 2)
            .style("stroke", "#E8E8E8");

        if (this.__data__.name == prevClicked) { //the same element was clicked again (so we need to unclick)
          //update prevClicked (nothing is clicked)
          prevClicked = ""; //do we need this?
    
          //need to set click to false (nothing is clicked)
          clicked = false;

          //need to also hide the information in the accordion: 
          hide_details();

        } else { //another variant was clicked, so we need to unclick the previous one and highlight the new one

          //need to update prevClicked: 
          prevClicked = this.__data__.name;

          //Then highlight only those that are an ancestor of the current segment.
          vis.selectAll("path")
             .filter(function(node) {
                return (sequenceArray.indexOf(node) >= 0);
                      })
              .style("stroke-width", 2)
              .style("angularWidth", 0.2)
              .style("stroke", "yellow");

          //something is now clicked so we need to update clicked
          clicked = true; 

          show_details(this); //calls function that will make the information appear on the accordion
        } 
      }
    } /*closes click(d) function*/



    // Makes both this element and the next one get darker + shows info about variant?
    function hover(d) {
      //console.log("I hovered"); //for testing purposes

      if (clicked == false) { //nothing is selected, hovering should work

      //the below code is copied from the mouseover one that existed before
      var sequenceArray = getAncestors(d);
      //Fade all the segments.
      d3.selectAll("path")
        .style("stroke-width", 2)
        .style("stroke", "#E8E8E8");

      //Then highlight only those that are an ancestor of the current segment.
      vis.selectAll("path")
         .filter(function(node) {
            return (sequenceArray.indexOf(node) >= 0);
            })
         .style("stroke-width", 2)
         .style("stroke", "black");
        
      } else { //something is clicked
          //nothing should happen (since element is clicked)
        }

    }


    // Given a node in a partition layout, return an array of all of its ancestor
    // nodes, highest first, but excluding the root.
    function getAncestors(node) {
      var path = [];
      var current = node;
      while (current.parent) {
        path.unshift(current);
        current = current.parent;
      }
      return path;
    }


    // Take a 2-column CSV and transform it into a hierarchical structure suitable
    // for a partition layout. The first column is a sequence of step names, from
    // root to leaf, separated by hyphens. The second column is a count of how 
    // often that sequence occurred.
    function buildHierarchy(csv) {
      var root = {"name": "root", "children": []};
      for (var i = 0; i < csv.length; i++) {
        var sequence = csv[i][0]; //so it actually starts by reading in the first element in test1 (data1)
        var size = +csv[i][1];
        // if (isNaN(size)) { // e.g. if this is a header row
        //   continue;
        // }
        var parts = sequence.split(";");
        var currentNode = root;
        for (var j = 0; j < parts.length; j++) {
          
          var children = currentNode["children"];
          var nodeName = parts[j];
          var childNode;
          if (j + 1 < parts.length) {
            // Not yet at the end of the sequence; move down the tree.
     	      var foundChild = false;
     	      for (var k = 0; k < children.length; k++) {
     	        if (children[k]["name"] == nodeName) {
     	        childNode = children[k];
     	        foundChild = true;
     	        break;
     	        }
     	      }
            // If we don't already have a child node for this branch, create it.
   	        if (!foundChild) {
   	          childNode = {"name": nodeName, "children": []};
   	          children.push(childNode);
   	        }
   	        currentNode = childNode;
          } else {
   	        // Reached the end of the sequence; create a leaf node.
   	        childNode = {"name": nodeName, "size": size}; 
   	        children.push(childNode);
          }
        }
      }
      return root; 
    }; /*closes biuldHierarchy(csv) function*/


    /*ALL THE BELOW CODE IS COPIED FROM LAUREN'S CODE IN THE CURRENT VISUALIZATION (FOR THE ACCORDION)*/

    var saved_LW =[]; //create an array to store the elements that are saved

    /*The below function determines whether an element is stored, returning true if it is already 
    saved and false if not - taken from Lauren's code*/
    function is_saved_LW (variant_LW) {
      //ensure a variant is selected
      if (variant_LW === "Example Variant") {
        return true;
      }
      //check if variant is already saved
      for (var i = saved_LW.length - 1; i >= 0; i--) {
        console.log(saved_LW[i]);
        if (saved_LW[i] === variant_LW) {
          alert(variant_LW + " is already saved.")
          return true;
        }
      };
      //alert(variant_LW + " NOT SAVED YET!")
      return false;
    }

    //this is where the "accordion" gets updated?
    var $template = $(".template");
    var hash = 2;

    //the below arranges what happens when you click "Save"
    $(".btn-add-panel").on("click", function () {
      console.log("I clicked save");
      var panel_header = document.getElementById('var_info').innerHTML;
      console.log("panel_header: " + panel_header);
      console.log("saved_LW: " + saved_LW);
      if (!is_saved_LW(panel_header)) {
        console.log("should come in here after");
        var panel_contents = document.getElementById('second_info').innerHTML;
        //alert(panel_header);
        var $newPanel = $template.clone();
        $newPanel.find(".collapse").removeClass("in");
        $newPanel.find(".accordion-toggle").attr("href", "#" + (++hash))
            .text(panel_header);
        $newPanel.find(".panel-body").html(panel_contents);
        $newPanel.find(".panel-collapse").attr("id", hash);
        $newPanel.find(".glyphicon-remove-circle").attr("id", panel_header);
        $("#accordion").append($newPanel.fadeIn());
        saved_LW.push(panel_header);
        $("#clicked-variant").hide();
        //track_save (panel_header,'pin'); //should uncomment these later
      } 
    });

    $(document).on('click', '.glyphicon-remove-circle', function () {
      console.log("click?");
      //get the variant name stored in circle id
      var to_delete = $(this).attr('id'); //this will be a problem - no id with sunburst
      //remove variant from saved array
      var index = saved_LW.indexOf(to_delete);
      saved_LW.splice(index, 1);
      //remove panel from accordion
      $(this).parents('.panel').get(0).remove();
      //track_save (to_delete,'unpin'); //should uncomment these later
    });

    /* Function to show the details of a clicked variant (changed the information on the tooltop) 
    - adapted from Lauren's code*/
    function show_details(element) { 
      $(".saved-variant").removeClass("in");
      $("#collapseOne").collapse('show');
      $("#clicked-variant").show();
      //the below code adapts all the information in the html file
      var object;
      var variantName = element.__data__.name;
      //getting all the information for that variant: 
      for (var i=0; i<allObjects.length; i++) { //need to create this allObjects array (that has all objects)
        if (allObjects[i].name == variantName) {
          object = allObjects[i]; //sets it as the object
        }
      }

      //depending on which element (empty or not empty) is clicked:
      if (object != undefined) { //that it isn't an empty one that was clicked
      document.getElementById("var-intro").style.display="none";
      document.getElementById("var-details").style.display="block";
      document.getElementById("var_info").innerHTML=variantName;
      //if this is how we keep them, then we don't need to actually add them as attributes
      document.getElementById("var_summary").innerHTML=object.summary; 
      document.getElementById("var_certainty_of_evidence").innerHTML=object.certainty_of_evidence;
      document.getElementById("var_health_effect").innerHTML=object.health_effect;
      document.getElementById("var_impact").innerHTML=object.impact;
      document.getElementById("var_rarity").innerHTML=object.rarity;
      document.getElementById("var_category").innerHTML=object.category;
      } else {
        //do nothing (essentially, it is as if nothing was cliked so should still say "sample variant")
        console.log("clicked an empty variant");

        //remove the highlighting:
        // var sequenceArray = getAncestors(d);
        // d3.selectAll("path")
        //   .style("stroke-width", 2)
        //   .style("stroke", "#E8E8E8");
      } /*closes the else*/
    } /*closes the show_details(element) function*/

    /*CLOSES THE CODE COPIED FROM LAUREN'S FOR THE ACCORDION*/

    /*The below function removes all information from the accordion and displays the default intro*/
    function hide_details() {
      //changes the visibility settings
      document.getElementById("var-intro").style.display="block";
      document.getElementById("var-details").style.display="none";

      document.getElementById("var_info").innerHTML="Example Variant"; //sets the title to the default
    } /*closes hide_details function*/

    // tooltip for mouseover functionality
    var tooltip = CustomTooltip('gates_tooltip', 200);
    $('.btn-click').tooltip({trigger: "hover", placement: "top"});

  }); /*closes the first csv data*/
}); /*closes the second csv data*/