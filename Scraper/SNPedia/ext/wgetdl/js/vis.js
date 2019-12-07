

var tracklight ="";
var prevTracklight = "";
var original_color = ""; //to save the original color so that it can be accessed later
var prevOriginalColor = "";
var exited = false;
// var ridofGene = ""; this needs to be substring of splice -4 (Gene) 

//for the check if saved then add part of code
var varExists = false;  //boolean initialzied as false
var savedVariants = [];  //array 
var allNodes = [];


function removeBlack(thang){

var subThang = thang.substring(thang.length-4,thang.length);

if (subThang=="Gene"){
  thang=thang.substring(0, thang.length-4); //starting off at the beginning 
}
console.log(subThang);

// this is removing the variant from the array on exit so when you reclick it then it is able to resave 
var index2remove= savedVariants.indexOf(thang); 
var test=savedVariants.splice(index2remove,1); 
console.log(index2remove);
// console.log(test); 
// console.log(savedVariants);

 //  console.log(thang);



 //console.log("THANG IS: " + document.getElementsByName(thang)[1].(" "));

var clickedArray1 = document.getElementsByName(thang);
var clickedArray2 = document.getElementsByName(thang + " 1");
var clickedArray3 = document.getElementsByName(thang + " 2");

if (clickedArray1.length != 0) {
  //  hide_details2(clickedArray1[0]);
  
    clickedArray1[0].setAttribute("stroke", document.getElementsByName(thang)[0].getAttribute("oStroke"));
    clickedArray1[0].setAttribute("stroke-width", 2);
    


  }

  if (clickedArray2.length != 0) {
   // hide_details2(clickedArray2[0]);
    clickedArray2[0].setAttribute("stroke", document.getElementsByName(thang)[0].getAttribute("oStroke"));
    clickedArray2[0].setAttribute("stroke-width", 2);

  }

  if (clickedArray3.length != 0) {

    clickedArray3[0].setAttribute("stroke", document.getElementsByName(thang)[0].getAttribute("oStroke"));
    clickedArray3[0].setAttribute("stroke-width", 2);

   // hide_details2(clickedArray3[0]);
  }


          //AJAX:

         var variant_name = document.getElementsByName(thang)[0];
         console.log("object below:");
         console.log(variant_name);

            var status = "affected";
            if (variant_name.getAttribute("fill")=="#ffffff") {
              status = "carrier";
            }

       var dbData = {userId: variant_report, variant: thang, filter: "", status: status, tab: "", action: "unsave"};


       console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
                console.log("succesfully saved: save button");
              }
            });

}

// var food = [];

      function hide_details2(element) { //HIDES ELEMENT ELEMENT!!!

        console.log(element);

   //the below is what is making the mouse on and mouse off work but seems to be not working for click and unclick?

   //element.setAttribute("stroke", original_color);
   element.setAttribute("stroke", element.getAttribute("oStroke"));
   element.setAttribute("stroke-width", 2);

    var names_original =[];
    var names_other = [];


   if (element.getAttribute("name")!=null) {  //this null is preventing the bubble borders to switch back.... need to fix but don't know how. 
     names_original = element.getAttribute("name").split(" ");
   }

  }

  var opened = false;

  function backToOrigin(clickedthing) {
console.log("nodes is: " + allNodes);



//making all without black borders
       for (var g=0; g<allNodes.length; g++) {
       document.getElementsByName(allNodes[g].name)[0].setAttribute("stroke", document.getElementsByName(allNodes[g].name)[0].getAttribute("oStroke"));
       document.getElementsByName(allNodes[g].name)[0].setAttribute("stroke-width", 2);
    }

    // if (opened == false ) {


//making the one clicked have a black border
var variantNAME = clickedthing.innerText.split(" ")[1].substring(1,clickedthing.innerText.split(" ")[1].length);

var circleElm1 = document.getElementsByName(variantNAME);
var circleElm2 = document.getElementsByName(variantNAME + " 1");
var circleElm3 = document.getElementsByName(variantNAME + " 2");

  if (circleElm1.length != 0) {
  //  hide_details2(clickedArray1[0]);
    circleElm1[0].setAttribute("stroke", "black");
    circleElm1[0].setAttribute("stroke-width", 4);


  }

  if (circleElm2.length != 0) {
    circleElm2[0].setAttribute("stroke", "black");
    circleElm2[0].setAttribute("stroke-width", 4);

  }

  if (circleElm3.length != 0) {

    circleElm3[0].setAttribute("stroke", "black");
    circleElm3[0].setAttribute("stroke-width", 4);

    }

    $( "#Ace" ).accordion( "option", "active","false"  );

    opened = true;
  // } else if (opened == true ) {
  //   opened = false;
  // }

  }

var custom_bubble_chart = (function(d3, CustomTooltip) {

  "use strict";


 
  var width = 800,
      height = 800, 
      tooltip = CustomTooltip("gates_tooltip", 200),
      layout_gravity = -0.01,
      damper = 0.1,
      nodes = [], 
      categories = [],
      vis, force, circles, radius_scale;

//NEW GLOBAL VARIABLE TRACKING THE HIGHTLIGHTED CIRCLE VARIANT 


var clicked = false;
var object;


 
  var center = {x: width / 2, y: height / 2};
 
  var year_centers = { //this is where the nodes are told where to go on the graph
      "Anatomical and congenital": {x: width/9 + 160, y: height/10-200},
      "Blood": {x: width/3.6 + 160, y: height/10-20+200},
      "Breathing": {x: width/2.1 + 160, y: height/10-20+200}, 
      "Cancer": {x: width/1.53 + 160, y: height/10-20+200},

      "Drug response": {x: width/9 + 160, y: height/4.7+230},
      "Genital and urinary": {x: width/3.6 + 160, y: height/4.7+230},
      "Hearing and vision": {x: width/2.1 + 160, y: height/4.7+230},
      "Heart and circulatory": {x: width/1.53 + 160, y: height/4.7+230},

      "Immune system": {x: width/9 + 160, y: height/3 +270},
      "Mental and behavioral": {x: width/3.6 + 180, y: height/3 +270},
      "Metabolism": {x: width/2.1 + 160, y: height/3 +270},
      "Mouth, liver, and digestive": {x: width/1.53 + 160, y: height/3 +270},

      "Muscular, skeletal, and connective tissue": {x: width/9 +160, y: height/2.2+320},
      "Nervous system": {x: width/3.6 + 160, y: height/2.2+320},
      "Skin": {x: width/2.1 + 160, y: height/2.2+320},
      "Other": {x: width/1.53 + 180, y: height/2.2+320}, 
      "": {x: width/1.53 + 160, y: height/2.2+320}, //this should be removed later
    };


    var health_centers = { //only x matters here
      "Low": {x: width/3.94 + 150, y: height/4},
      "Moderate": {x: width/2.6 + 160, y: height/4},
      "High": {x: width/1.89 + 170, y: height/4}
    };

    var like_centers = { //only y matters here
      "Well-established": {x: width/3.94, y: height/6 + 130}, 
      "Likely": {x: width/3.94, y: height/3.5 + 170}, 
      "Uncertain": {x: width/3.94, y: height/2.6 + 220} 
    };
 
  var fill_color = d3.scale.ordinal()
                  .domain(["Protective", "Benign", "Pharma", "Pathogenic", "Carrier", "Not Reviewed"])  //is not reviewed pharma or something else?
                  .range(["#89b4fd", "#cccccc", "#e77ee7", "#ff6666", "#ffffff", "#cccccc"]); //order: blue, gray, purple, red, gray

                  var appear = false;
               
 var freq_group;
 var pen_group;
  function custom_chart(data) {
    var max_amount = d3.max(data, function(d) { return parseInt(freq_group/10, 10); } );
    radius_scale = d3.scale.pow().exponent(0.5).domain([0, max_amount]).range([2, 85]);
 
    nodes=[]; //to empty it when put in new number
           
var ID_num = 0;
    data.forEach(function(d){

       //rarity group (0-7): ++ need to deal with empty ones to be what type of middle size????
       if (d.rarity=="") {freq_group=50} //works -- need to decide how big we want these to be
       else if (d.frequency*100<0.1) {freq_group=0} //biggest bubble // 0
       else if (d.frequency*100>0.1 && d.frequency*100<0.3) {freq_group=3}  //1
       else if (d.frequency*100>0.3 && d.frequency*100<1) {freq_group=4} //2
       else if (d.frequnecy*100>1 && d.frequency*100<3) {freq_group=5} //3
       else if (d.frequency*100>3 && d.frequency*100<10) {freq_group=6} //4
       else if (d.frequency*100>10 && d.frequency*100<30) {freq_group=8} //6
       else if (d.frequency*100>30) {freq_group=9} //smallest bubble //7


//penetrance group (0-7): (just 5 exist)
      if (d.penetrance_score == 1) {pen_group = 8}
      else if (d.penetrance_score == 2) {pen_group=7} 
      else if (d.penetrance_score == 3) {pen_group=6}
      else if (d.penetrance_score == 4) {pen_group=4}
      else if (d.penetrance_score >= 5) {pen_group=2} //biggest bubble
      else {pen_group=9} //smallest bubble
      
      categories = d.category.split(";"); //seperate the categories where the semicolons are

      var node = {
        size: 150-(freq_group*10), //based on the frequency
        pen_size: 150-(pen_group*10),
        radius: radius_scale(parseFloat(150-(freq_group*10), 10.0)),
        rarity: d.frequency,
        name: d.variant,
        penetrance: d.penetrance_score, //risk
        comment: d.summary,
        group: d.impact,
        year: categories, //'year' needs to change + need to read in more than one
        like: d.evidence,
        health: d.clinical_importance,
        zygosity: d.zygosity,
        inheritance: d.inheritance,
        copynumber: 0,  //0 means it is the original (not a copy)

        x: Math.random() * 900,
        y: Math.random() * 800

      };



      nodes.push(node); 
      ID_num++;

      var iterate;

      data.forEach(function(d){
        
       //rarity group (0-7): ++ need to deal with empty ones to be what type of middle size????
       if (d.rarity=="") {freq_group=50} //works -- need to decide how big we want these to be
       else if (d.frequency*100<0.1) {freq_group=0} //biggest bubble // 0
       else if (d.frequency*100>0.1 && d.frequency*100<0.3) {freq_group=3}  //1
       else if (d.frequency*100>0.3 && d.frequency*100<1) {freq_group=4} //2
       else if (d.frequnecy*100>1 && d.frequency*100<3) {freq_group=5} //3
       else if (d.frequency*100>3 && d.frequency*100<10) {freq_group=6} //4
       else if (d.frequency*100>10 && d.frequency*100<30) {freq_group=8} //6
       else if (d.frequency*100>30) {freq_group=9} //smallest bubble //7


//penetrance group (0-7): (just 5 exist)
      if (d.penetrance_score == 1) {pen_group = 8}
      else if (d.penetrance_score == 2) {pen_group=7} 
      else if (d.penetrance_score == 3) {pen_group=6}
      else if (d.penetrance_score == 4) {pen_group=4}
      else if (d.penetrance_score >= 5) {pen_group=2} //biggest bubble
      else {pen_group=9} //smallest bubble

      categories = d.category.split(";"); //splits categories


      if (categories.length > 1){  //creates baby nodes! 

        for(iterate=1; iterate <categories.length; iterate++){  //start at 1 to get rid of beginning at 0

            var copynode = {
            size: 150-(freq_group*10), //based on the frequency
            pen_size: 150-(pen_group*10),
            radius: radius_scale(parseFloat(150-(freq_group*10), 10.0)),
            rarity: d.frequency,
            name: d.variant + " " + iterate, 
            penetrance: d.penetrance_score,
            comment: d.summary,
            group: d.impact,
            year: categories, //'year' needs to change!!!!
            like: d.evidence,
            health: d.clinical_importance,
            zygosity: d.zygosity,
            inheritance: d.inheritance,
            copynumber: iterate,  //added this attrubute that takes iterate (the index of what catergory in the array its in)

            x: Math.random() * 900,
            y: Math.random() * 800
      };

      nodes.push(copynode); 
        }
      }
    });
 
    });
 
    nodes.sort(function(a, b) {return b.value- a.value; }); //rarity??
 
    vis = d3.select("#vis").append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("name", "svg_vis");
 
    circles = vis.selectAll("circle")
                 .data(nodes, function(d) { return d.name ;});



      circles.enter().append("circle")
      .attr("r", 0)
      .attr("fill", function(d) { if (d.inheritance == "Recessive" && d.zygosity == "Heterozygous") {return fill_color("Carrier") } else { return fill_color(d.group);}})
      .attr("stroke-width", 2)
      .attr("stroke", function(d) { return d3.rgb(fill_color(d.group)).darker();})
      .attr("oStroke", function(d) { return d3.rgb(fill_color(d.group)).darker();})

      .attr("name", function(d) { return  d.name; }) //took out: "bubble_" + d.name




      .on("click", function(d,i) { 
        //resets everything
       allNodes = nodes;
      // console.log(allNodes);
       hide_tooltip();

       rarity_info_appears = false;
       risk_info_appears = false;

       clicked = true;

// if (tracklight!==undefined) {
//     document.getElementsByName(tracklight)[0].setAttribute("stroke", original_color);
//     document.getElementsByName(tracklight)[0].setAttribute("stroke-width", 2);
// }
    //   tracklight = this.getAttribute("name");

      for (var g=0; g<nodes.length; g++) {
        console.log(nodes[g].name[0]);
       document.getElementsByName(nodes[g].name)[0].setAttribute("stroke", document.getElementsByName(nodes[g].name)[0].getAttribute("oStroke"));
       document.getElementsByName(nodes[g].name)[0].setAttribute("stroke-width", 2);
    }




    //   console.log("tracklight is set as: " + tracklight);
        if (appear == false) {
          object=this;
          show_details(d,i,this);  //this allows it to scroll through it
          appear=true; 
          name=d.name; 

          //AJAX CODE : ACTION : CLICK
          var variant_clicked = object.getAttribute("name").split(" ")[0];

            var status = "affected";
            if (object.getAttribute("fill")=="#ffffff") {
              status = "carrier";
            }
 

            
            var dbData = {userId: variant_report, variant: variant_clicked, filter: rr_filter, status: status, tab: tab, action: "click"};
         //   console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
                //if data is posted succesfully then do stuff in here...
                //console.log("succesfully saved: CLICK");
              }
            });

            //---- end of ajax code



document.getElementById("exit").className="saveExit";
document.getElementById("save").className="saveExit";
        } 

        //this is so that you can unclick it by pressing on its duplicate
        else if (appear==true) {
         
        //  hide_details(d,i,object);
          object=this;
          show_details(d,i,this);

           //AJAX CODE : ACTION : UNCLICK
          var variant_clicked = object.getAttribute("name").split(" ")[0];

            var status = "affected";
            if (object.getAttribute("fill")=="#ffffff") {
              status = "carrier";
            }

            
            var dbData = {userId: variant_report, variant: variant_clicked, filter: rr_filter, status: status, tab: tab, action: "click"};
           // console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
                //if data is posted succesfully then do stuff in here...
              //  console.log("succesfully saved: CLICK");
              }
            });

            //---- end of ajax code


        }

      });

  }



  //.on("click", function(d,i) { 



  function charge(d) {
    return -Math.pow(d.radius-15, 2.0) / 7; //this makes them go closer + farther away from each other (the more -- the more far away)  this was: /8
  } 
 
  function start() {
    force = d3.layout.force()
            .nodes(nodes)

            .size([width, height]);
  }



  function changeForce(charge, gravity) {
    force.charge(charge).gravity(gravity); 
  } 
 

 
  function display_by_year() { //size by rarity
    height = 600;

    force.gravity(layout_gravity)
         .charge(charge)
         .friction(0.9)
         .on("tick", function(e) {
          circles.each(move_towards_year(e.alpha))
                 .attr("cx", function(d) {return d.x;})
                 .attr("cy", function(d) {return d.y;})
                 .attr("r", function(d) { return ((parseFloat((d.size)))/4)/1.5; }) //by rarity
                
                 .style("stroke-dasharray", function(d) {if (d.rarity=="") { return ("10,5") } else { return ("0,0")}})  //dashed 
        });

    force.start();
    hide_category();
    display_years();
  }


 

  function display_by_year_pen() { //size by penetrance
    
    height = 600;

    force.gravity(layout_gravity)
         .charge(charge)
         .friction(0.9)
         .on("tick", function(e) {
          circles.each(move_towards_year(e.alpha))
                 .attr("cx", function(d) {return d.x;})
                 .attr("cy", function(d) {return d.y;})
                 .attr("r", function(d) {return (d.pen_size/4)/1.5; }) //by penetrance   
                 .style("stroke-dasharray", "0,0"); 
        });

    force.start();
    hide_category();
    display_years();



  }
 


  function move_towards_year(alpha) {
    return function(d) {

      if (d.copynumber == 0){ //if it is not a copynode then display in the "graph" tab

      
      var target_y = like_centers[d.like];
      var target_x = health_centers[d.health];
      d.x = d.x + (target_x.x - d.x) * (damper + 0.02) * alpha * 1.1;
      d.y = d.y + (target_y.y - d.y) * (damper + 0.02) * alpha * 1.1; 
    }
     else{
      d.x= width+100;  
      d.y = height+100;
    }

    };
  }
 
 
  function display_years() {
      var years_x = {}; 
    

      var years_y = {};
      var years_data = d3.keys(years_x);
      var years = vis.selectAll(".years")
                 .data(years_data);


      years.enter().append("text")
                   .attr("class", "years")
                   .attr("x", function(d) { return years_x[d]; }  )
                   .attr("y", function(d) { return years_y[d]; })
                   .attr("text-anchor", "middle")
                   .text(function(d) { return d;});

//label for x-axis:
      years.enter().append("text")
                  .attr("class", "years")
                  .attr("text-anchor", "end")
                  .attr("x", width/1.5)
                  .attr("y", height - 110) 
                  .text("HEALTH EFFECT");

  }


 
  function hide_years() {
      var years = vis.selectAll(".years").remove();
  }
 

 //code to create the categories!!! 
 function display_by_category() { //by rarity

  height = 800;


    force.gravity(layout_gravity)
         .charge(charge)
         .friction(0.9)
        .on("tick", function(e) {
          circles.each(move_towards_category(e.alpha))
                 .attr("cx", function(d) {return d.x;})
                 .attr("cy", function(d) {return d.y;})
                 .attr("r", function(d) {return ((parseFloat((d.size)))/4)/1.5; }) //by rarity
                 .style("stroke-dasharray", function(d) {if (d.rarity=="") { return ("10,5") } else { return ("0,0")}})  //dashed 
     
        });
    force.start();
    hide_years();
    display_category();


  }


   function display_by_category_pen() { //by penetrance (risk)

    height = 800;


    force.gravity(layout_gravity)
         .charge(charge)
         .friction(0.9)
         .on("tick", function(e) {

          circles.each(move_towards_category(e.alpha))
                 .attr("cx", function(d) {return d.x;})
                 .attr("cy", function(d) {return d.y;})
                 .attr("r", function(d) {return (d.pen_size/4)/1.5; }) //by penetrance
                 .style("stroke-dasharray", "0,0"); 
        });
    force.start();
    hide_years();
    display_category();

  }

 

  function move_towards_category(alpha) {
    return function(d) {  //takes a node and tells it where to go
      var target;

       //this is the loaction
       target = year_centers[d.year[d.copynumber]]; //copynumber is an attrubute in copynode d.index of copy number choses the index

       //now setting the x and y value of that node
       d.x = d.x + (target.x - (d.x)) * (damper + 0.02) * alpha * 1.1;
       d.y = d.y + (target.y - (d.y)) * (damper + 0.02) * alpha * 1.1;
    };
  }
 
 

  function display_category() {  //this is the display 
      var years_x = {};
     
      var years_y = {};
      

      var years_data = d3.keys(years_x);
      var years = vis.selectAll(".years")
                 .data(years_data);
 
      years.enter().append("text")
                   .attr("class", "years")
                   .attr("x", function(d) { return years_x[d]; }  )
                   .attr("y", function(d) { return years_y[d]; })
                   .attr("text-anchor", "middle")
                   .text(function(d) { return d;});
  }
 


  function hide_category() {
      var years = vis.selectAll(".years").remove();
  }


  



    function hide_details(data, i, element) {


   var color_stroke = function(d) { return d3.rgb(fill_color(d.group)).darker();};
   

   //the below is what is making the mouse on and mouse off work but seems to be not working for click and unclick?
   element.setAttribute("stroke", original_color);
   element.setAttribute("stroke-width", 2);

    var names_original =[];
    var names_other = [];


   if (element.getAttribute("name")!=null) {  //this null is preventing the bubble borders to switch back.... need to fix but don't know how. 
     names_original = element.getAttribute("name").split(" ");
   }

      for (var g=0; g<nodes.length; g++) {

         names_other = nodes[g].name.split(" ");

      if (names_original[0] == names_other[0]) {
       document.getElementsByName(nodes[g].name)[0].setAttribute("stroke", original_color);
       element.setAttribute("stroke-width", 2);
      }
    }
  }





  function exit_varName(){
    document.getElementById("second_info").innerHTML="";
    document.getElementById("var_info").style.visibility="hidden";
    document.getElementById("exit").style.visibility="hidden";
    document.getElementById("save").style.visibility="hidden";
    document.getElementById("second_info").style.visibility="hidden";
    }

  function copyDiv() {
     var divHeader = document.getElementById('var_info');
    var divContent = document.getElementById('second_info');
    document.getElementById("empty_header").innerHTML = divHeader.innerHTML;
    document.getElementById("empty_content").innerHTML =divContent.innerHTML; //this is going in as the header! WRONG should be the body
  }

  function save_bottom(){  //moves the item to the bottom 
    var newHeader = document.createElement("newHeader");
    newHeader.className = "accord_header";
    newHeader.id += "emptyHeader"+ "second_info";

    var newContent = document.createElement("newContent");
    newContent.className = "accord_content";
    newContent.id= "emptyContent";

    document.getElementById("empty_insert").innerHTML = newHeader + newContent + "empty_insert";

  }
  
  function show_details(data, i, element, y) { 
    $("#King").accordion( "option", "active","false");
    original_color = element.getAttribute("stroke");
    element.setAttribute("stroke", "black");
    element.setAttribute("stroke-width", 4)

    var names_original =[];
    var names_other = [];

    names_original = element.getAttribute("name").split(" ");
      for (var g=0; g<nodes.length; g++) {

        names_other = nodes[g].name.split(" ");

        if (names_original[0] == names_other[0]) {
          document.getElementsByName(nodes[g].name)[0].setAttribute("stroke", "black");
          document.getElementsByName(nodes[g].name)[0].setAttribute("stroke-width", 4)
        }
      }

      var risk ="";
      //only "risk" if it is pathogenic
      if (data.group == "Pathogenic") {
        if (data.penetrance == 0) {
          risk = "Up to 0.1% increased risk (extremely low penetrance)";
        } else if (data.penetrance == 1) {
          risk = "0.1% - 1% increased risk (very low penetrance)";
        } else if (data.penetrance == 2) {
          risk = "1% - 5% increased risk (low penetrance)";
        } else if (data.penetrance == 3) {
          risk = "5% - 20% increased risk (moderate penetrance)";
        } else if (data.penetrance == 4) {
          risk = "20% - 50% increased risk (moderately high penetrance)";
        } else if (data.penetrance == 5) {
          risk = "50% - 100% increased risk (complete or highly penetrant)";
        } else {
          risk = "Unknown.";
        }
      } else { //not pathogenic, use "chance"
        if (data.penetrance == 0) {
          risk = "Up to 0.1% increased chance (extremely low penetrance)";
        } else if (data.penetrance == 1) {
          risk = "0.1% - 1% increased chance (very low penetrance)";
        } else if (data.penetrance == 2) {
          risk = "1% - 5% increased chance (low penetrance)";
        } else if (data.penetrance == 3) {
          risk = "5% - 20% increased chance (moderate penetrance)";
        } else if (data.penetrance == 4) {
          risk = "20% - 50% increased chance (moderately high penetrance)";
        } else if (data.penetrance == 5) {
          risk = "50% - 100% increased chance (complete or highly penetrant)";
        } else {
          risk = "Unknown.";
        }
      }

      var rare="";
      var data_rarity = data.rarity*100; //save the right decimal point of data.rarity
      if (data.rarity == "") {
        rare = "Unknown.";
      } else if (data.zygosity == "Heterozygous") {  //This person is heterozygous
        var rare_number = (2 * data.rarity * (1-data.rarity))*100;
        //getting the right decimal point for rare_number
        if (rare_number>=10) {
        rare_number = rare_number.toFixed(0);
        } else if (rare_number>=1 && rare_number<10) {
          rare_number = rare_number.toFixed(1);
        } else if (rare_number>=0.1 && rare_number<1) {
          rare_number = rare_number.toFixed(2);
        } else if (rare_number>=0.01 && rare_number<0.1) {
          rare_number = rare_number.toFixed(3);
        } else if (rare_number>=0.001 && rare_number<0.01) {
          rare_number = rare_number.toFixed(3);
        } 

        //getting the right decimal point for data_rarity
        if (data_rarity>=10) {
        data_rarity = data_rarity.toFixed(0);
        } else if (data_rarity>=1 && data_rarity<10) {
          data_rarity = data_rarity.toFixed(1);
        } else if (data_rarity>=0.1 && data_rarity<1) {
          data_rarity = data_rarity.toFixed(2);
        } else if (data_rarity>=0.01 && data_rarity<0.1) {
          data_rarity = data_rarity.toFixed(3);
        } else if (data_rarity>=0.001 && data_rarity<0.01) {
          data_rarity = data_rarity.toFixed(4);
        } 

        rare = rare_number + "% of people have one copy of this, like you ("+ data_rarity + "% allele frequency)";
      } else if (data.zygosity == "Homozygous") { //This person is homozygous
        var rare_number = (data.rarity*data.rarity)*100;
      
        //getting the right decimal point for rare_number
        if (rare_number>=10) {
        rare_number = rare_number.toFixed(0);
        } else if (rare_number>=1 && rare_number<10) {
          rare_number = rare_number.toFixed(1);
        } else if (rare_number>=0.1 && rare_number<1) {
          rare_number = rare_number.toFixed(2);
        } else if (rare_number>=0.01 && rare_number<0.1) {
          rare_number = rare_number.toFixed(3);
        } else if (rare_number>=0.001 && rare_number<0.01) {
          rare_number = rare_number.toFixed(4);
        } 

        //getting the right decimal point for data_rarity
        if (data_rarity>=10) {
        data_rarity = data_rarity.toFixed(0);
        } else if (data_rarity>=1 && data_rarity<10) {
          data_rarity = data_rarity.toFixed(1);
        } else if (data_rarity>=0.1 && data_rarity<1) {
          data_rarity = data_rarity.toFixed(2);
        } else if (data_rarity>=0.01 && data_rarity<0.1) {
          data_rarity = data_rarity.toFixed(3);
        } else if (data_rarity>=0.001 && data_rarity<0.01) {
          data_rarity = data_rarity.toFixed(4);
        } 

        rare = rare_number + "% of people have two copies of this, like you ("+ data_rarity + "% allele frequency)";
      }

      //making the categories print pretty: 
      var categories_string = "";
      for (var i = 0; i<data.year.length; i++) {
        categories_string += data.year[i];
        if (i+1<data.year.length) {
          categories_string += ", ";
        }
      }

      var content="<span class><b>Variant:</b> " + data.name + "<br></span>";
      var content="<span class><b>Gene Variant:</b> " + data.name + "<br></span>";
      content +="<span class><b>Summary:</b> " + data.comment + "</span><br>";
      content +="<span class><b>Certainty of Evidence:</b> " + data.like + "</span><br>";
      content +="<span class><b>Health Effect:</b> " + data.health + "</span><br>";
      content +="<span class><b>Impact:</b> " + data.group + "</span><br>";
      content +="<span class><b>Rarity:</b> " + rare + "</span><br>";
      content +="<span class><b>Risk:</b> " + risk + "<br>";
      content +="<span class><b>Category:</b> " + categories_string + "</span>"; //function that returns the string

      document.getElementById("var_info").style.visibility="visible";
      document.getElementById("second_info").innerHTML=content;
      document.getElementById("exit").className="saveExit";

      //to test if they are already saved so if the button "saved" should be shown as clicked
      var variant_clicked = object.getAttribute("name").split(" ")[0];
            
      $.get("./js/is_saved.php", {userId: variant_report, variant: variant_clicked}, function (saved) {

      if (saved === "false") { //not saved
        document.getElementById("save").className="saveExit"; 
      } else if (saved === "true" ) { //is saved
        document.getElementById("save").className="saveExit active";
      }

    });

    document.getElementById("var_info").innerHTML= "<b><i>Variant &nbsp</i></b>" + data.name;
    //<span style='\'display:inline-block class=\'ui-icon ui-icon-circle-plus accordionAdd\'</span>"

    $( "#Ace" ).accordion( "option", "active", 0 ); //so when Ace is active King is not 

    //this undo my thing in the window foo
    document.getElementById('accordion').style.marginTop ="240px";  //this makes sure the height is the same even when clicking a variant, b4 it shifted up for some reason
    document.getElementById('Ace').style.visibility = "visible";
    document.getElementById("saveButton").disabled = false;

   //**************************

  }



  function hide_tooltip() { //same for all 
    tooltip.hideTooltip();
  }
  

  function show_rarityTooltip(x, y) {

    var content ="<span class=\"name\">Rarity:</span><span class=\"value\"> Rarity, also know as frequency in population or allele frequency, describes the percentage of the population that has this genetic variant. The smaller the frequency, the less common it is among the population and the more interesting it is to a healthcare professional.</span><br/>";
    document.getElementById("gates_tooltip").style.width = "200px";
    document.getElementById("gates_tooltip").style.border = "2px solid #000";
    tooltip.showTooltip(content, x, y);
  }

  function show_riskTooltip(x, y) {

    var content ="<span class=\"name\">Risk:</span><span class=\"value\"> how often individuals carrying the variant develop the associated disease</span><br/>";
    document.getElementById("gates_tooltip").style.width = "200px";
    document.getElementById("gates_tooltip").style.border = "2px solid #000";
    tooltip.showTooltip(content, x, y);
  }



  $('#saveButton').click( function() {
    var variant_clicked = object.getAttribute("name").split(" ")[0];
  var clickedArray1 = document.getElementsByName(variant_clicked);
  var clickedArray2 = document.getElementsByName(variant_clicked + " 1");
  var clickedArray3 = document.getElementsByName(variant_clicked + " 2");

  if (clickedArray1.length != 0) {
    hide_details2(clickedArray1[0]);
  }

  if (clickedArray2.length != 0) {
    hide_details2(clickedArray2[0]);
  }

  if (clickedArray3.length != 0) {
    hide_details2(clickedArray3[0]);
  }

  //AJAX:
  var status = "affected";
  if (object.getAttribute("fill")=="#ffffff") {
    status = "carrier";
  }

  var dbData = {userId: variant_report, variant: variant_clicked, filter: rr_filter, status: status, tab: tab, action: "save"};

  $.ajax({
    url: './js/ajax.php', //link to php file
    type: 'POST',
    data: dbData, //needs to be an array
    success: function (success) {
      console.log("succesfully saved: save button");
    }
  });
         

  var varHeader = document.getElementById('var_info').innerHTML;
  var secondContent = document.getElementById('second_info').innerHTML;
    
  //randomly generated number 10,000-20,000 so its five digits long and it with def be unique
  //div will not be kool, it will be div-(randomnumber), and button wont be myClicker= button-(randommunber) (once button is clicked gets ran num)
  //and you will know which div to remove 
  var rando = Math.floor((Math.random() * 20000) + 10000);

  document.getElementById('Ace').style.visibility = "hidden";
  document.getElementById('var_info').style.visibility = "hidden";

  var currentVar = document.getElementById('var_info').innerHTML.split('&nbsp;</i></b>')[1];

  for (var i = 0; i < savedVariants.length; i++) { 
    if (savedVariants[i] == currentVar){
      varExists = true;
      break;
      }
    } 
    var newDiv = "<div id="+rando+" ><h3 onclick='console.log(\"Tracklight is: \" + tracklight); backToOrigin(this); console.log(\"Header click event\");' style='float:right; padding-right:3px; font-size:12.5px; height:43.625px; margin-left=300px;'><div style='float:right; margin-right:5px;' id="+rando+" onclick='exited = true; console.log(\"Exit click event\"); foo(event); var frank = $(this).closest(\"div\"); var head = frank.prev(\"h3\"); removeBlack(getElementById("+rando+").innerText.split(\" \")[1].substring(1,getElementById("+rando+").innerText.split(\" \")[1].length)); frank.add(head).fadeOut(\"slow\",function(){$(getElementById("+rando+")).remove();  });'> <img src='img/close.png' width='20px'></div>" + varHeader + "</h3><div id=\'accordian_"+okay+"\' class='accordionList'>" + secondContent + "</div></div>";
    if (!varExists){
      savedVariants.push(currentVar);
      $('.sandwich').append(newDiv); //only append it if it is not in the saved group
      console.dir(savedVariants);
    } else { 
      alert("Cannot add, already Saved!");
      varExists=false; //reset it back to false
    }
    $('.sandwich').accordion("refresh");  
    $('#King').accordion("refresh");
    $('.bread').accordion("refresh");      
  });

  var my_mod = {};
  my_mod.init = function (_data) {
    custom_chart(_data);
    start();
  };

  var rr_filter = "risk";
  var tab = "graph";
  var riskKey = document.getElementById("risk_key").innerHTML;
  var rarityKey = document.getElementById("rarity_key").innerHTML + "<br><br><br><br><br><br><br><br><br>";
  var rarity_info_appears = false;
  var risk_info_appears = false;

 

  my_mod.display_year = display_by_year;
  my_mod.display_category = display_by_category;
  my_mod.toggle_view = function(view_type) { //BUG: does not reset the risk + rarity properly... why. 

  if (view_type == 'year')  {
    tab = "graph";
    document.getElementById('main').style.visibility = 'visible';
    document.getElementById('rarity_penetrance').style.visibility = 'visible';
    document.getElementById('legend').style.visibility = 'visible';
    document.getElementById('AllLegends').style.marginTop= "110px";
    document.getElementById('AllLegends').style.visibility= "visible";
    document.getElementById('myCanvas').style.backgroundImage= "url(http://i62.tinypic.com/5ra1h.png)";
    document.getElementById('myCanvas').style.marginLeft= "200px";
    document.getElementById('myCanvas').style.marginTop= "-50px";
    document.getElementById('myCanvas').style.width= "490px";
    document.getElementById('myCanvas').style.height= "575px";
    document.getElementById('myCanvas').style.borderLeft= "0px";
    document.getElementById('myCanvas').style.borderBottom= "0px";
    document.getElementById('legend').style.height = '605px';
    document.getElementById('both_suits').style.height = '590px';
    document.getElementById('accordion').style.marginTop ="240px";  //this makes sure the height is the same even when clicking a variant, b4 it shifted up for some reason
       
    hide_tooltip();

    rarity_info_appears = false;
    risk_info_appears = false;


    document.getElementById("risk_key").innerHTML=riskKey;


    //to make the "pen" active (resets)
    document.getElementById("pen").checked = "true";

   
      
    display_by_year_pen(); 

    //the tooltips: 






  var rarityqmark = document.getElementById("rarity_tooltip");

  rarityqmark.onclick = function() {
    if (color_info_appears == true) {
      hide_tooltip();
      color_info_appears = false;
    } else if (hollow_info_appears == true) {
      hide_tooltip();
      hollow_info_appears = false;
    } else if (risk_info_appears == true) {
      hide_tooltip();
      risk_info_appears = false;
    } else if (health_info_appears == true) {
      hide_tooltip();
      health_info_appears = false;
    } else if (certainty_info_appears == true) {
      hide_tooltip();
      certainty_info_appears = false;
    }

    if (rarity_info_appears == false) {
      show_rarityTooltip(this.offsetLeft, this.offsetTop);
      rarity_info_appears = true;
    } else if (rarity_info_appears == true) {
      hide_tooltip();
      rarity_info_appears = false;
    }
  }

  var riskqmark = document.getElementById("risk_tooltip");

  riskqmark.onclick = function() {
    if (color_info_appears == true) {
      hide_tooltip();
      color_info_appears = false;
    } else if (hollow_info_appears == true) {
      hide_tooltip();
      hollow_info_appears = false;
    } else if (rarity_info_appears == true) {
      hide_tooltip();
      risk_info_appears = false;
    } else if (certainty_info_appears == true) {
      hide_tooltip();
      certainty_info_appears = false;
    } else if (health_info_appears == true) {
      hide_tooltip();
      health_info_appears = false;
    }
    
    if (risk_info_appears == false) {
      show_riskTooltip(this.offsetLeft, this.offsetTop);
      risk_info_appears = true;
    } else if (risk_info_appears == true) {
      hide_tooltip();
      risk_info_appears = false;
    }
  }
      
  //ajax code: -------------- (TAB)
  //empty variant and status
  var dbData = {userId: variant_report, variant: "", filter: rr_filter, status: "", tab: tab, action: "tab"};    
  $.ajax({
    url: './js/ajax.php', //link to php file
    type: 'POST',
    data: dbData, //needs to be an array
    success: function (success) {
    //  console.log("succesfully saved: TAB (GRAPH)");
    }
  });
//---------------


  var foo = document.getElementById("pen");
  foo.onclick = function() {


  //reset all tooltips: 
  hide_tooltip();

  rarity_info_appears = false;
  risk_info_appears = false;


  rr_filter = "risk";
  display_by_year_pen(); //penetrance

  //to change the key:
  document.getElementById("risk_key").innerHTML=riskKey; //this is correct -- do not change.


  var riskqmark = document.getElementById("risk_tooltip");

  riskqmark.onclick = function() {
    if (color_info_appears == true) {
      hide_tooltip();
      color_info_appears = false;
    } else if (hollow_info_appears == true) {
      hide_tooltip();
      hollow_info_appears = false;
    } else if (rarity_info_appears == true) {
      hide_tooltip();
      risk_info_appears = false;
    } else if (certainty_info_appears == true) {
      hide_tooltip();
      certainty_info_appears = false;
    } else if (health_info_appears == true) {
      hide_tooltip();
      health_info_appears = false;
    }
    
    if (risk_info_appears == false) {
      show_riskTooltip(this.offsetLeft, this.offsetTop);
      risk_info_appears = true;
    } else if (risk_info_appears == true) {
      hide_tooltip();
      risk_info_appears = false;
    }
  }



      //ajax code: -------------- (FILTER)
            //empty variant and status
            var dbData = {userId: variant_report, variant: "", filter: rr_filter, status: "", tab: tab, action: "filter"};
          //  console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
            //  console.log("succesfully saved: FILTER (risk)");
              }
            });
//---------------


            }

            var foo = document.getElementById("rar");
            foo.onclick = function() {



              //reset all tooltips: 
       hide_tooltip();

       rarity_info_appears = false;
       risk_info_appears = false;



              rr_filter = "rarity";
              display_by_year(); //rarity

              //to change the key:
              document.getElementById("risk_key").innerHTML=rarityKey;




      //ajax code: -------------- (FILTER)
            //empty variant and status
            var dbData = {userId: variant_report, variant: "", filter: rr_filter, status: "", tab: tab, action: "filter"};
         //   console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
          //      console.log("succesfully saved: FILTER (rarity)");
              }
            });

      //---------------

      //repeat because it gets reset??? 
var rarityqmark = document.getElementById("rarity_tooltip");

      rarityqmark.onclick = function() {
        if (color_info_appears == true) {
          hide_tooltip();
          color_info_appears = false;
        } else if (hollow_info_appears == true) {
          hide_tooltip();
          hollow_info_appears = false;
        } else if (risk_info_appears == true) {
          hide_tooltip();
          risk_info_appears = false;
        }

        if (rarity_info_appears == false) {
          show_rarityTooltip(this.offsetLeft, this.offsetTop);
          rarity_info_appears = true;
        } else if (rarity_info_appears == true) {
          hide_tooltip();
          rarity_info_appears = false;
        }
      }






            }

            //when clicking save in the variants: 
            var saved = document.getElementById("save");
            saved.onclick = function() {

            // document.getElementById("save").className="btn";  //just put this in, now appears to indent but unsure if AJAX working
            //save_bottom(); 
            copyDiv();         
            // var variant_clicked = object.getAttribute("name").split(" ")[0];
            // var variant_inheritance = object.getAttribute("inheritance");
            // var variant_zygosity= object.getAttribute("zygosity");
            // var status = "affected";
 
            // if (variant_inheritance=="Recessive" && variant_zygosity == "Heterozygous") {
            // status = "carrier";
            // } 

                      var variant_clicked = object.getAttribute("name").split(" ")[0];

            var status = "affected";
            if (object.getAttribute("fill")=="#ffffff") {
              status = "carrier";
            }

            //to test if they are already saved
            $.get("./js/is_saved.php", {userId: variant_report, variant: variant_clicked}, function (saved) {

            if (saved === "false") { //not working


              
           //   console.log("is not saved... so we save...");


            var dbData = {userId: variant_report, variant: variant_clicked, filter: rr_filter, status: status, tab: tab, action: "save"};
          //  console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
                //if data is posted succesfully then do stuff in here...
               // console.log("succesfully saved: SAVE");
              }
            });

         } else if (saved === "true" ) {
          //need to make it look unclicked: 

          

          document.getElementById("save").className="saveExit";


           var dbData = {userId: variant_report, variant: variant_clicked, filter: rr_filter, status: status, tab: tab, action: "unsave"};
          //  console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
                //if data is posted succesfully then do stuff in here...
             //   console.log("succesfully saved: UNSAVE");
              }
            });
          }
           });

            //need to save it to the acordion



            }

            var closed = document.getElementById("exit");
            closed.onclick = function(d, i) {

            hide_details(d, i, object);
            exit_varName(); //this will remove the var_info
            appear = false;

            //AJAX CODE : ACTION : UNCLICK
            // var variant_clicked = object.getAttribute("name").split(" ")[0];
            // var variant_inheritance = object.getAttribute("inheritance");
            // var variant_zygosity= object.getAttribute("zygosity");
            // var status = "affected";
 
            // if (variant_inheritance=="Recessive" && variant_zygosity == Heterozygous) {
            // status = "carrier";
            // } 

                      var variant_clicked = object.getAttribute("name").split(" ")[0];

            var status = "affected";
            if (object.getAttribute("fill")=="#ffffff") {
              status = "carrier";
            }

            
            var dbData = {userId: variant_report, variant: variant_clicked, filter: rr_filter, status: status, tab: tab, action: "click"};
         //   console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
                //if data is posted succesfully then do stuff in here...
            //    console.log("succesfully saved: UNCLICK (graph)");
              }
            });

            //---- end of ajax code


            }

    } 

    //glossary starts

    if (view_type == 'glossary') {
      //$( "div.legend-labels" ).replaceWith( "<h2>New heading</h2>" );

      tab = "glossary";

      document.getElementById('accordion').style.marginTop ="138px";  //this makes sure the height is the same even when clicking a variant, b4 it shifted up for some reason
   


        var dbData = {userId: variant_report, variant: "", filter: "", status: "", tab: tab, action: "tab"};
           // console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
            //    console.log("succesfully saved: TAB (glossary)");
              }
            });



       //reset all tooltips: 
       hide_tooltip();

       rarity_info_appears = false;
       risk_info_appears = false;



     
/*      if (glossary_info_appears == false) {
      console.log("GLOSSARY");
      glossary_info_appears = true;
      show_glossaryTooltip(0, 110);

      } else if (glossary_info_appears == true) {
      hide_tooltip();
      glossary_info_appears = false;
      document.getElementById('glossary').className="btn";

      //reset whichever button they had clicked on before (tab)
      if (tab == "graph") {
      document.getElementById("year").className="btn active";
      } else if (tab == "categories") {
    document.getElementById("cata").className="btn active";
        }
          }*/
document.getElementById('main').style.visibility = 'hidden';
document.getElementById('rarity_penetrance').style.visibility = 'hidden';

document.getElementById('legend').style.visibility = 'hidden';
document.getElementById('AllLegends').style.marginTop= "-550px";
document.getElementById('AllLegends').style.visibility= "hidden";



make_glossary_appear();

    }

    //glossary ends


    if (view_type =='cata'){

      //resets locations/visibility
      document.getElementById('main').style.visibility = 'visible';
      document.getElementById('rarity_penetrance').style.visibility = 'visible';
      document.getElementById('legend').style.visibility = 'visible';
      document.getElementById('legend').style.height = '670px';
      document.getElementById('both_suits').style.height = '655px';
      document.getElementById('AllLegends').style.visibility= "visible";
      document.getElementById('AllLegends').style.marginTop= "110px";
      document.getElementById('myCanvas').style.backgroundImage= "";
      document.getElementById('myCanvas').style.marginLeft= "55px";
      document.getElementById('myCanvas').style.marginTop= "-50px";
      document.getElementById('myCanvas').style.width= "730px";
      document.getElementById('myCanvas').style.height= "675px";
      document.getElementById('myCanvas').style.borderLeft= "1px dotted gray";
      document.getElementById('myCanvas').style.borderBottom= "1px dotted gray";
        document.getElementById('accordion').style.marginTop ="240px";  //this makes sure the height is the same even when clicking a variant, b4 it shifted up for some reason
   



       //initialize all tooltips to not show
       hide_tooltip();

       rarity_info_appears = false;
       risk_info_appears = false;



       //tab var
      tab = "categories";

      //sets to risk key (since tab changes)
      document.getElementById("risk_key").innerHTML=riskKey;


      //to make the "pen" active + change the filter back to "risk" (resets)
      document.getElementById("pen").checked = "true";
    //  document.getElementById("rar").className = "btn";
      rr_filter = "risk";





      var informationButton = document.getElementById("testing123");




      var rarityqmark = document.getElementById("rarity_tooltip");

      rarityqmark.onclick = function() {
        if (color_info_appears == true) {
          hide_tooltip();
          color_info_appears = false;
        } else if (hollow_info_appears == true) {
          hide_tooltip();
          hollow_info_appears = false;
        } else if (risk_info_appears == true) {
          hide_tooltip();
          risk_info_appears = false;
        }

        if (rarity_info_appears == false) {
          show_rarityTooltip(this.offsetLeft, this.offsetTop);
          rarity_info_appears = true;
        } else if (rarity_info_appears == true) {
          hide_tooltip();
          rarity_info_appears = false;
        }
      }

      var riskqmark = document.getElementById("risk_tooltip");

      riskqmark.onclick = function() {
        if (color_info_appears == true) {
          hide_tooltip();
          color_info_appears = false;
        } else if (hollow_info_appears == true) {
          hide_tooltip();
          hollow_info_appears = false;
        } else if (rarity_info_appears == true) {
          hide_tooltip();
          risk_info_appears = false;
        }
        
        if (risk_info_appears == false) {
          show_riskTooltip(this.offsetLeft, this.offsetTop);
          risk_info_appears = true;
        } else if (risk_info_appears == true) {
          hide_tooltip();
          risk_info_appears = false;
        }
      }
      

      display_by_category_pen();



            //ajax code: -------------- (TAB)
            //variant and status can be empty -- all this is necessary
            var dbData = {userId: variant_report, variant: "", filter: rr_filter, status: "", tab: tab, action: "tab"};
         //   console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
            //    console.log("succesfully saved: TAB (categories)");
              }
            });

            //---------------------- end of ajax code



              var foo = document.getElementById("pen");
              foo.onclick = function() {


       hide_tooltip();

       rarity_info_appears = false;
       risk_info_appears = false;




              rr_filter = "risk";
              display_by_category_pen(); //penetrance

              //to change the key:
              document.getElementById("risk_key").innerHTML=riskKey; //this is correct -- do not change.
              console.log("at pen tab: " + riskKey);


      //ajax code: -------------- (FILTER)
            //empty variant and status
            var dbData = {userId: variant_report, variant: "", filter: rr_filter, status: "", tab: tab, action: "filter"};
          //  console.log(dbData);
           
            $.ajax({
              url: './js/ajax.php', //link to php file
              type: 'POST',
              data: dbData, //needs to be an array
              success: function (success) {
            //    console.log("succesfully saved: FILTER (risk)");
              }
            });
//---------------

//repeat because it gets reset??? 


var rarityqmark = document.getElementById("rarity_tooltip");

      rarityqmark.onclick = function() {
        if (color_info_appears == true) {
          hide_tooltip();
          color_info_appears = false;
        } else if (hollow_info_appears == true) {
          hide_tooltip();
          hollow_info_appears = false;
        } else if (risk_info_appears == true) {
          hide_tooltip();
          risk_info_appears = false;
        }

        if (rarity_info_appears == false) {
          show_rarityTooltip(this.offsetLeft, this.offsetTop);
          rarity_info_appears = true;
        } else if (rarity_info_appears == true) {
          hide_tooltip();
          rarity_info_appears = false;
        }
      }

      var riskqmark = document.getElementById("risk_tooltip");

      riskqmark.onclick = function() {
        if (color_info_appears == true) {
          hide_tooltip();
          color_info_appears = false;
        } else if (hollow_info_appears == true) {
          hide_tooltip();
          hollow_info_appears = false;
        } else if (rarity_info_appears == true) {
          hide_tooltip();
          risk_info_appears = false;
        }
        
        if (risk_info_appears == false) {
          show_riskTooltip(this.offsetLeft, this.offsetTop);
          risk_info_appears = true;
        } else if (risk_info_appears == true) {
          hide_tooltip();
          risk_info_appears = false;
        }
      }
    }

    var foo = document.getElementById("rar");
    foo.onclick = function() {
      hide_tooltip();

      rarity_info_appears = false;
      risk_info_appears = false;


      rr_filter = "rarity";
      display_by_category(); //rarity

      //to change the key:
      document.getElementById("risk_key").innerHTML=rarityKey;
      console.log("at rarity: " + rarityKey);

      //ajax code: -------------- (FILTER)
      //empty variant and status
      var dbData = {userId: variant_report, variant: "", filter: rr_filter, status: "", tab: tab, action: "filter"};
           
      $.ajax({
        url: './js/ajax.php', //link to php file
        type: 'POST',
        data: dbData, //needs to be an array
        success: function (success) {
        }
      });
      //---------------







      var rarityqmark = document.getElementById("rarity_tooltip");

      rarityqmark.onclick = function() {
        if (color_info_appears == true) {
          hide_tooltip();
          color_info_appears = false;
        } else if (hollow_info_appears == true) {
          hide_tooltip();
          hollow_info_appears = false;
        } else if (risk_info_appears == true) {
          hide_tooltip();
          risk_info_appears = false;
        }

        if (rarity_info_appears == false) {
          show_rarityTooltip(this.offsetLeft, this.offsetTop);
          rarity_info_appears = true;
        } else if (rarity_info_appears == true) {
          hide_tooltip();
          rarity_info_appears = false;
        }
      }
      
            }


  }
      };

 
  return my_mod;
})(d3, CustomTooltip);