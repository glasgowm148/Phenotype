d3.csv("data/test1.csv", function(data1) {
  d3.csv("data/test2.csv", function(data2) {

function bubbleChart() {
  // Constants for sizing
  var width = 1056;
  var height = 757;
  variantNodes = [];

  var bubbleColors = {"Protective": "#89b4fd",
                      "Benign": "#cccccc",
                      "Pathogenic": "#ff6666",
                      "PathCarrier": "url(#PathDiag)", //for the carrier
                      "BenCarrier": "url(#BenDiag)", //for the carrier
                      "ProtCarrier": "url(#ProtDiag)", //for the carrier
                      "NotPresent": "white",
                      "Pharmacogenetic": "purple",
                      "PharmCarrier": "url(#PharmDiag)", //for the carrier
                      "Unknown": "url(#UnkDiag)" //special diag for unknown
                    };

  // tooltip for mouseover functionality
  var tooltip = floatingTooltip('gates_tooltip', 240);

  // Locations to move bubbles towards, depending
  // on which view mode is selected.
  var center = { x: width / 2, y: height / 2.2 };

  var columnCenters = {
    1: { x: width / 3.05, y: height / 2.2 },
    2: { x: width / 2.1, y: height / 2.2 },
    3: { x: 2 * width / 3, y: height / 2.2 }
  };

  // X locations of the year titles.
  var columnTitleX = {
    "Mother": 250,
    "Similarities": width / 2,
    "Son": width - 300
  };

  // Used when setting up force and
  // moving around nodes
  var damper = 0.102;

  // These will be set in create_nodes and create_vis
  var svg = null;
  var bubbles = null;
  var nodes = [];

  // Charge function that is called for each node.
  // Charge is proportional to the diameter of the
  // circle (which is stored in the radius attribute
  // of the circle's associated data.
  // This is done to allow for accurate collision
  // detection with nodes of different sizes.
  // Charge is negative because we want nodes to repel.
  // Dividing by 8 scales down the charge to be
  // appropriate for the visualization dimensions.
  function charge(d) {
    return -Math.pow(d.radius, 2.0) / 8;
  }

  // Here we create a force layout and
  // configure it to use the charge function
  // from above. This also sets some contants
  // to specify how the force layout should behave.
  // More configuration is done below.
  var force = d3.layout.force()
    .size([width, height])
    .charge(charge)
    .gravity(-0.01)
    .friction(0.9);


  // Sizes bubbles based on their area instead of raw radius
  var radiusScale = d3.scale.pow()
    .exponent(0.5)
    .range([2, 14]);



  /*--------------------------------------------------------------
    setRadius (HELPER FUNCTION)
    -------------------------------------------------------------*/

  function setRadius(frequency) {
  /*Calculates a radius based on a variant's frequency/rarity*/
      var radius;

      /*Overwrite variant frequency if it's unlisted or 1.0*/
      if (frequency == "" || frequency == "1.0")
          frequency = 0.9;

      radius = -Math.log(frequency);
      if (radius < 1)
          radius = 0.8;

      return radius
 }

 /*--------------------------------------------------------------
   setColumn (HELPER FUNCTION)
   -------------------------------------------------------------*/

 function setColumn(variant, array, num) {
 /*Determines which column of the venn diagram a variant belongs to
   and returns the variant's column number. */

    var column = num; //column number of a participant's unique variants

    /*Check to see if the given variant is shared between both participants
    by looping through a given array of shared variants.*/
    for(i = 0; i < array.length; i++) {
       if (variant == array[i])
          column = 2; //column number for shared variants
    }

     return column;
}


  /*----------------------------------------------------------------------
    createNodes FUNCTION
  -----------------------------------------------------------------------*/

  function createNodes() {
  /*This data manipulation function takes the raw data from both CSV files
    and converts it into an array of unique node objects (shared variants
    are only listed once in the array). Each node will store data and
    visualization values to visualize a bubble.*/

    /*-------------------------------------------------------------------
      Using the data from both csv files, create an array that
      lists the names of all shared variants.
    -----------------------------------------------------------------*/

      var variants1 = [];
      var variants2 = [];
      var commonVariants = [];

      /*Push all variant names from first csv file to an array*/
      data1.forEach(function(d) {
        variants1.push(d.variant.replace(/-/g, ''));
      });

      /*Push all variant names from second csv file to an array*/
      data2.forEach(function(d) {
        variants2.push(d.variant.replace(/-/g, ''));
      });

      /*Push all shared variants into the commonVariants array*/
      for (i = 0; i < variants1.length; i++) {
        for (j = 0; j < variants2.length; j++) {

          if (variants1[i] == variants2[j])
            commonVariants.push(variants1[i]);
        }
      }

    /*--------------------------------------------------------------------------------
      DATA FROM FIRST CSV FILE: Create an object "bubbleNode" that
      represents each variant (and its attributes) from the csv file
    --------------------------------------------------------------------------------*/

      data1.forEach(function(d) {

          var bubbleNode = {
            name: d.variant.replace(/-/g, ''),
            type: d.type,
            impact: d.impact,
            zygosity: d.zygosity,
            inheritance: d.inheritance,
            group: null,
            comment: d.summary,
            url: d.getev_report_url,
            radius: radiusScale(setRadius(d.frequency)),
            color: null,
            column: setColumn(d.variant.replace(/-/g, ''), commonVariants, 1),
            x: Math.random() * 900,
            y: Math.random() * 800,
          };

        variantNodes.push(bubbleNode);
      });

    /*--------------------------------------------------------------------------------
      DATA FROM SECOND CSV FILE: Create an object "bubbleNode" that
      represents variants (and its attributes) that are unique to
      the second csv file and not shared with the first csv file
    --------------------------------------------------------------------------------*/

      data2.forEach(function(d) {

          /*Determine the column number of each variant read-in from file*/
          var column = setColumn(d.variant.replace(/-/g, ''), commonVariants, 3);

          /*Only create a bubbleNode for variants unique to second csv to
            avoid creating repeat nodes*/

          if (column == 3) {
            var bubbleNode = {
              name: d.variant.replace(/-/g, ''),
              type: d.type,
              impact: d.impact,
              zygosity: d.zygosity,
              inheritance: d.inheritance,
              group: null,
              comment: d.summary,
              url: d.getev_report_url,
              radius: radiusScale(setRadius(d.frequency)),
              color: null,
              column: column,
              x: Math.random() * 900,
              y: Math.random() * 800,
            };

          variantNodes.push(bubbleNode);
        }
      });

  /*Sort nodes to prevent occlusion of smaller bubble nodes*/
  variantNodes.sort(function (a, b) { return b.value - a.value; });

  return variantNodes;
}

/*----------------------------------------------------------------------
  PREPARING BUBBLE CHART
-----------------------------------------------------------------------*/

  var chart = function chart(selector) {
  /*Function prepares the data for visualization by adding an svg element
    to the provided selector and starting the visualization creation process.
    Selector is a DOM element or CSS selector that points to the parent element
    of the bubble chart.*/

    nodes = createNodes();

    /*Set the force's nodes to our newly created nodes array.*/
    force.nodes(nodes);

    /*Create a SVG element inside the provided selector with desired size.*/
    svg = d3.select(selector)
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    /*Bind nodes data to what will become DOM elements to represent them.*/
    bubbles = svg.selectAll('.bubble')
      .data(nodes, function (d) { return d.name; });

    /*Create new circle elements each with class "bubble". There will be
      one circle.bubble for each object in the nodes array. Initially,
      their radius (r attribute) will be 0.*/
      //function to create  a generic pattern
       //takes inputs of idName and color

   function createPattern1(idName, color) {
            svg.append('defs')
               .append('pattern')
               .attr('id', idName)
               .attr('patternUnits', 'userSpaceOnUse')
               .attr('width', 4)
               .attr('height', 4)
               .append('path')
               .attr('d',
                   'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
               .attr('fill', 'orange')
               .attr('stroke', color)
               .attr('stroke-width', 2);
       }
       //creating the patterns. nothing further needs to be done for these to work.
   createPattern1('PathDiag', '#ff6666 ');
   createPattern1('BenDiag', '#cccccc ');
   createPattern1('ProtDiag', '#89b4fd ');
   createPattern1('PharmDiag', "purple");
   createPattern1('UnkDiag', "green");

   /*--------------------------------------------------------------
     setColor (HELPER FUNCTION)
     -------------------------------------------------------------*/

   function setColor(d, impact, inheritance, zygosity) {
   /*Determine a bubble's color based on impact, inheritance, and zygosity*/

       var color;

       if (zygosity == "Heterozygous" && inheritance == "Recessive") { //determining if the person is a carrier
           if (impact == "Pathogenic") {
               d.group = "PathCarrier";
              //  color = "PathCarrier";
           }
           if (impact == "Protective") {
              d.group = "ProtCarrier"
           }
           if (impact == "Benign" || impact == "Not Reviewed") {
              d.group = "BenCarrier";
           }
           if (impact == "Pharmacogenetic") {
               d.group = "PharmCarrier";
           }
           if (impact == "Not Reviewed" ||
              (inheritance == "Unknown" ||inheritance == "Complex/Other")) {
               d.group = "Unknown";
           }
       } else //if the person is not a carrier
           d.group = impact;

       return bubbleColors[d.group];
     }



      //  if ((impact == "Pharmacogenetic" || impact == "Not Reviewed") ||
      //      (inheritance == "Unknown" || inheritance == "Complex/Other")) {
      //      color = "BenCarrier";
      //
      //  } else if (zygosity == "Heterozygous" && inheritance == "Recessive") {
      //      if (impact == "Pathogenic"){
      //          color = "PathCarrier";
      //      }
      //      if (impact == "Protective"){
      //          color = "ProtCarrier";
      //      }
      //      if (impact == "Benign" || impact == "Not Reviewed")
      //          color = "BenCarrier"
      // } else
      //    color = impact;

  //    return bubbleColors[color];
  //  }

  //  function stroke_color(color_categ) {
  //     var color;
   //
  //     if (color_categ == "PathCarrier" || color_categ == "Pathogenic")
  //       color = bubbleColors["Pathogenic"];
   //
  //     else if (color_categ == "ProtCarrier" || color_categ == "Protective")
  //       color = bubbleColors["Protective"];
   //
  //     else if (color_categ == "BenCarrier" || color_categ == "Benign")
  //       color = bubbleColors["Benign"];
   //
  //     return color;
  //  }



    bubbles.enter().append('circle')
      .classed('bubble', true)
      .attr('r', 0)
      .attr('fill', function (d) {
           console.log("Group: " + d.group);
           return setColor(d, d.impact, d.inheritance, d.zygosity); })
      .attr('stroke', function (d) { return d3.rgb("#000").darker(); })
      .attr('stroke-width', 2)
      .on('mouseover', showDetail)
      .on('mouseout', hideDetail);


    /*Fancy transition to make bubbles appear, ending with the correct radius*/
    bubbles.transition()
      .duration(2000)
      .attr('r', function (d) { return d.radius; });

    /*Set initial layout to single group.*/
    groupBubbles();
  };


/*----------------------------------------------------------------------
  FUNCTIONS FOR SINGLE GROUP MODE
-----------------------------------------------------------------------*/

  function groupBubbles() {
  /*Sets visualization in "single group mode". The huID labels are hidden
    and the force layout tick function is set to move all nodes to the
    center of the visualization.*/

    hideYears();

    force.on('tick', function (e) {
      bubbles.each(moveToCenter(e.alpha))
        .attr('cx', function (d) { return d.x; })
        .attr('cy', function (d) { return d.y; });
    });

    force.start();
  }

  /*---------------HELPER FUNCTION--------------------*/
  function moveToCenter(alpha) {
  /*Returns a function that takes the data for a single node
    and adjusts the position values of that node to move it
    toward the center of the visualization.*/

    return function (d) {
      d.x = d.x + (center.x - d.x) * damper * alpha;
      d.y = d.y + (center.y - d.y) * damper * alpha;
    };
  }


/*----------------------------------------------------------------------
  FUNCTIONS FOR VENN DIAGRAM MODE
-----------------------------------------------------------------------*/
  function splitBubbles() {
  /*Sets visualization in "venn diagram mode". The huId labels are shown
    and the force layout tick function is set to move nodes to the
    columnCenter of the venn diagram.*/

    showYears();

    force.on('tick', function (e) {
      bubbles.each(moveToYears(e.alpha))
        .attr('cx', function (d) { return d.x; })
        .attr('cy', function (d) { return d.y; });
    });

    force.start();
  }

  /*
   * Helper function for "split by year mode".
   * Returns a function that takes the data for a
   * single node and adjusts the position values
   * of that node to move it the year center for that
   * node.
   *
   * Positioning is adjusted by the force layout's
   * alpha parameter which gets smaller and smaller as
   * the force layout runs. This makes the impact of
   * this moving get reduced as each node gets closer to
   * its destination, and so allows other forces like the
   * node's charge force to also impact final location.
   */

  /*---------------HELPER FUNCTION--------------------*/
  function moveToYears(alpha) {
  /*Returns a function that takes the data for a single
    node and adjusts the position values of that node to
    move it the column  center for that node.*/

    return function (d) {
      var target = columnCenters[d.column];
          if (d.impact == "Pathogenic") {
              d.x = d.x + (target.x - d.x) * damper * alpha * 1.1;
              d.y = d.y + (target.y - d.y - 50) * damper * alpha * 1.1;
              if (d.group == "PathCarrier") {
                d.x = d.x + (target.x - d.x - 20) * damper * alpha * 1.1;
                d.y = d.y + (target.y - d.y - 50) * damper * alpha * 1.1;
                if (d.column == 1)
                  d.x = d.x + (target.x - d.x - 220) * damper * alpha * 1.1;
              }

          } else if (d.impact == "Protective") {
              d.y = d.y + (target.y - d.y - 20) * damper * alpha * 1.1;
              d.x = d.x + (target.x -d.x) * damper * alpha * 1.1;
              if (d.group == "ProtCarrier")
                  d.x = d.x + (target.x - d.x - 20) * damper * alpha * 1.1;

          } else if (d.impact == "Benign") {
              d.y = d.y + (target.y - d.y + 10) * damper * alpha * 1.1;
              d.x = d.x + (target.x -d.x) * damper * alpha * 1.1;
              if (d.group == "BenCarrier")
                d.x = d.x + (target.x - d.x - 20) * damper * alpha * 1.1;

          } else {
              d.x = d.x + (target.x -d.x) * damper * alpha * 1.1;
              d.y = d.y + (target.y - d.y + 40) * damper * alpha * 1.1;
          }

    };
  }
  // {"Protective": "#89b4fd",
  //                     "Benign": "#cccccc",
  //                     "Pathogenic": "#ff6666",
  //                     "PathCarrier": "url(#PathDiag)", //for the carrier
  //                     "BenCarrier": "url(#BenDiag)", //for the carrier
  //                     "ProtCarrier": "url(#ProtDiag)", //for the carrier
  //                     "NotPresent": "white",
  //                     "Pharmacogenetic": "purple",
  //                     "PharmCarrier": "url(#PharmDiag)", //for the carrier
  //                     "Unknown": "url(#UnkDiag)" //special diag for unknown
  //                   };


  /*
   * Hides Year title displays.
   */
  function hideYears() {
    svg.selectAll('.year').remove();
  }

  /*
   * Shows Year title displays.
   */
  function showYears() {
    // Another way to do this would be to create
    // the year texts once and then just hide them.
    var yearsData = d3.keys(columnTitleX);
    var years = svg.selectAll('.year')
      .data(yearsData);
    console.log("Years: " + years);

    years.enter().append('text')
      .attr('class', 'year')
      .attr('x', function (d) { return columnTitleX[d]; })
      .attr('y', 40)
      .attr('text-anchor', 'middle')
      .text(function (d) { return d; });
  }


  /*
   * Function called on mouseover to display the
   * details of a bubble in the tooltip.
   */
  function showDetail(d) {
    // change outline to indicate hover state.
    d3.select(this).attr('stroke', 'black');

    var content = '<span class="name">Variant: </span><span class="value">' +
                  d.name +
                  '</span><br/>' +
                  '<span class="name">Health Impact: </span><span class="value">$' +
                  addCommas(d.impact) +
                  '</span><br/>' +
                  '<span class="name">Summary: </span><span class="value">' +
                  d.comment +
                  '</span>';
    tooltip.showTooltip(content, d3.event);
  }

  /*
   * Hides tooltip
   */
  function hideDetail(d) {
    // reset outline
    d3.select(this)
      .attr('stroke', d3.rgb(d.color).darker());

    tooltip.hideTooltip();
  }

  /*
   * Externally accessible function (this is attached to the
   * returned chart function). Allows the visualization to toggle
   * between "single group" and "split by year" modes.
   *
   * displayName is expected to be a string and either 'year' or 'all'.
   */
  chart.toggleDisplay = function (displayName) {
    if (displayName === 'venn_all') {
      document.getElementById("vis").style.background="url('images/venn.png') no-repeat";
      splitBubbles();
    } else {
      document.getElementById("vis").style.background="none";
      groupBubbles();
    }
  };


  // return the chart function from closure.
  return chart;
}

/*
 * Below is the initialization code as well as some helper functions
 * to create a new bubble chart instance, load the data, and display it.
 */

var myBubbleChart = bubbleChart();

/*
 * Function called once data is loaded from CSV.
 * Calls bubble chart function to display inside #vis div.
 */
function display() {
  // if (error) {
  //   console.log(error);
  // }

  myBubbleChart('#vis');
}

/*
 * Sets up the layout buttons to allow for toggling between view modes.
 */
function setupButtons() {
  d3.select('#toolbar')
    .selectAll('.button')
    .on('click', function () {
      // Remove active class from all buttons
      d3.selectAll('.button').classed('active', false);
      // Find the button just clicked
      var button = d3.select(this);

      // Set it as the active button
      button.classed('active', true);

      // Get the id of the button
      var buttonId = button.attr('id');

      // Toggle the bubble chart based on
      // the currently clicked button.
      myBubbleChart.toggleDisplay(buttonId);
    });
}

/*
 * Helper function to convert a number into a string
 * and add commas to it to improve presentation.
 */
function addCommas(nStr) {
  nStr += '';
  var x = nStr.split('.');
  var x1 = x[0];
  var x2 = x.length > 1 ? '.' + x[1] : '';
  var rgx = /(\d+)(\d{3})/;
  while (rgx.test(x1)) {
    x1 = x1.replace(rgx, '$1' + ',' + '$2');
  }

  return x1 + x2;
}

// Display chart
display();

// setup the buttons.
setupButtons();

});
});
