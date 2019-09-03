
//dataset array gets made outside
var dataset = []
rectangleArray=[]; //to empty it when put in new number

//dimensions of svg canvas   
var width = 900;
var height = 200;


//reads in the data from this csv
d3.csv("data.csv", function(data) {

//function custom_chart(data) {
//have a global variable: prev clicked so that you can just minimize that one after. 
    

      
           
    //Ideally this is whre you'd want to initialize a variable, "y" that you can manipulate after evey pass through the
    //"for each" function. But, for some reason global variables cannot be accessed inside the "for each" function (why?)

    //This is where the rectangles get the information passed through from the csv file
    data.forEach(function(d){
      //The variable below is an object "rect", which holds all the attributes from the csv file
      var rect = {
        id: d.id,
        size: d.size,
        name: d.id,
        //name: d.variant, //will be added later
        comment: d.summary,
        group: d.impact, //impact = benign etc
        type: d.type,
        clicked: false,
        y: (height - rectHeight) / 2, 
        x: 50 //need to figure this out later (for some reason, using global variables outside of the "forEach" function does not work -- CLARISSA FIX THISSSS)

      };

    //this is where the global "y" variable should get updated

    //adds the rectangle made to the array
    rectangleArray.push(rect);
  });




    // dataset to play with
    // [rectangle size, impact, inheritance, zygosity]
    var dataset2 = [[50, "Benign", "Dominant", "Homozygous", "Although one report speculated that this variant may cause dominant, early-onset sensorineural hearing loss, the findings lacked statistical significance. Notably, this gene is not a clinically tested gene and another of the eight variants reported by these authors (S797F) has since been observed in a PGP participant with no symptoms of hearing loss."], 
                   [40, "ProtCarrier", "Recessive", "Heterozygous", "Reported to cause mild dysfunction of the cystic fibrosis gene, it may result in cystic fibrosis when combined with more severe variants."], 
                   [80, "Pathogenic", "Recessive", "Heterozygous", "Associated with increased risk of Barrett's esophagus and/or esophageal cancer. Our very rough estimate is that the increased risk may be around 4x (25% risk of Barrett's esophagus, assuming population average is 5%, and 1.2% lifetime risk of esophageal cancer compared to average .4% risk)."], 
                   [38, "Protective", "Recessive", "Homozygous", "This nonsynonymous SNP is associated with Wolfram Syndrome (known as DIDMOAD), which is characterized by early-onset non-autoimmune diabetes mellitus, diabetes insipidus, optic atrophy, and deafness) and to adult Type Two Diabetes Mellitus.  The WFS1 gene maps to chromosome 4p16.3.  The variant has been shown to be statistically associated with type II diabetes in six UK studies and one study of Ashkenazi Jews (Sandhu, M., et al., Minton et al.)."], 
                   [20, "BenCarrier", "Dominant", "Heterozygous", "Reported to be associated with increased susceptibility to prostate cancer, but later studies weaken the hypothesis. Xu et al.'s meta-analysis concludes that there is a small but significant increased risk (OR = 1.13). Assuming a lifetime risk of 16% for prostate cancer we calculate this leads to an increased risk of ~1.5% (17.5% total)."], 
                   [12, "Benign", "Recessive", "Heterozygous", "Severe variants in this gene are associated with holoprosencephaly disorders when combined with loss-of-function variants in SHH. Haploinsufficiency was identified in some families with this condition. It is unclear how likely this variant is to occur in combination with an SHH variant, or what phenotypic effect the variant would have on its own."],
                   [23, "PathCarrier", "Dominant", "Heterozygous", "Some authors report this rare variant as a nonpathogenic polymorphism, others suggest it may cause renal glucosuria in a recessive manner when compound heterozygous with other pathogenic variants."]];


    

    var dataValues2 = dataset2.map(function(v){return v[0]})

    // setting up plotting arrays for d3
    // each sub array is structured [width, xValue, [fillColor, strokeColor], ID]
    var dataSum2 = dataValues2.reduce(function(a, b){return a+b});
    var datasetScaledValues2 = dataValues2.map(function(a){return a / (dataSum2 + 2 * (dataset2.length-1)) * width});

    //Variable that holds all the colors, depending on what the data says
    var rectangleColors = {"Protective" : ["#89b4fd"],
                           "Benign" : ["#cccccc"],
                           "Pathogenic" : ["#ff6666"],
                           "PathCarrier" : ["url(#PathDiag)"], //for the carrier
                           "BenCarrier" : ["url(#BenDiag)"], //for the carrier
                           "ProtCarrier" : ["url(#ProtDiag)"]}; //for the carrier

    var xValue2 = 1;

    
    dataArrays2 = [];
   
    // This for loop should at some point get deleted. Instead, all of this should be calculated above an put in the Object "rect"
    // made above. 
    // For data 2: 
    // each sub array is structured [width, xValue, [fillColor, strokeColor], carrier status, information]
    for ( i = 0 ; i < dataset2.length ; i++ ){
        var dataArray2 = [];

        //adding one by one the information about each rectangle
        dataArray2.push(datasetScaledValues2[i]);
        if (i > 0){
            xValue2 += datasetScaledValues2[i-1] + 2;
        }        
        var rectangleColor = rectangleColors[dataset2[i][1]];
        dataArray2.push(xValue2);

        var information = dataset2[i][4];
        var name = dataset2[i][5];
        
        dataArray2.push(rectangleColor);
        dataArray2.push(information);
        dataArray2.push(name);
        dataArrays2.push(dataArray2);
    }

   
    //Appending each container (one for each person) to the svg
 	var svgContainer1 = d3.select("body").append("svg")
                                    	 .attr("width", width)
                                    	 .attr("height", height);

    var svgContainer2 = d3.select("body").append("svg")
                                         .attr("width", width)
                                         .attr("height", height);

 
 	// rectangle variables
    var rectHeightFactor = 0.7;
    var rectHeight = rectHeightFactor * height;
    var rectYCoor1 = (height - rectHeight) / 2;


    //for the second linear one:
    var rectYCoor2 = (height - rectHeight) / 2; //this needs to change so that we can actually see them


    rectangleArray.sort(function(a, b) {return b.value- a.value; });

    // creating a variable with the spots for the rectangles

    //There are two different ones because there are two different svg containers 
    //The first one takes in the rectangleArray that was made through the csv files above
    var rectangles1 = svgContainer1.selectAll("rect")
                                 .data(rectangleArray);

    //The second one takes in the data that was made by putting the data in an array (Clarrisa made this one)
    var rectangles2 = svgContainer2.selectAll("rect")
                                 .data(dataArrays2);

                        

    //For the first data: Takes in the data that was taken in from the csv above (careful, need to do d.x from the above, not the csv)
    rectangles1.enter().append("rect")
                .attr("x", function(d) { return datasetScaledValues2[d.id]}) //need to figure out how to pass this as d. something
                .attr("y", rectYCoor1)
                .attr("width", function(d) { return d.size }) //CLARISSA DO THIS THING
                .attr("height", rectHeight)
                // .attr("id", function(d){return d[3]})
                .attr("fill", function(d) { return rectangleColors[d.group]}) 
                //.attr("fill", "url(#PathDiag)")
                .attr("stroke", function(d){ return rectangleColors[d.group]})
                .attr("stroke-width", 2)
                .attr("info", function(d){ return d.comment}) //takes in the information from the dataArrays 
                .attr("clicked", false) //this is so that we can know whether that one has been clicked or not
                .on("mouseover", growRectangle)
                .on("mouseout", shrinkRectangle)
                .on("click", clickRectangle);


    //For the second data:
    //Giving attributes to rectangles, and specifying functions
    rectangles2.enter().append("rect")
                .attr("x", function(d){ return d[1] })
                .attr("y", rectYCoor2)
                .attr("width", function(d) { return d[0] })
                .attr("height", rectHeight)
                // .attr("id", function(d){return d[3]})
                .attr("fill", function(d) { return d[2][0]}) 
                //.attr("fill", "url(#PathDiag)")
                .attr("stroke", function(d){ return d[2][1]})
                .attr("stroke-width", 2)
                .attr("info", function(d){ return d[3]}) //takes in the information from the dataArrays 
                .attr("clicked", false) //this is so that we can know whether that one has been clicked or not
                .on("mouseover", growRectangle)
                .on("mouseout", shrinkRectangle)
                .on("click", clickRectangle);


    


    // growth factor for click function
    var rectGrowthFactor = 1.2; //This should be determine by Madeleine etc (and will be relatively hard coded)





    /* Below are all the functions for growing and shrinking rectangles (on hover and on click)*/

    /*This function grows the rectangle when hovered over. However, before, we need to determine whether it was already clicked. 
    If not, then it should grow when hovered. If yes, then it should not grow because then it will grow 2 times as much as it should.*/
    function growRectangle(d) {
        

        //saves clicked rectange into this variable (for easier use)
        var object = d3.select(this);

        //first want to change what the cursor looks like (doesn't matter if it actually grows or shrinks)
        object.style("cursor","pointer")

        //need to get the old height: 
        var oldHeight = object.attr("height");

        if (object.attr("clicked") == "false") {
        //changes the height and the y 
        object
            .attr("height", rectHeight * rectGrowthFactor)
            .attr("y", (height - oldHeight)/4);  
            } else {
                //do nothing - should not grow
            }   
    }


    /*This function shrinks the rectangle. However, before we shrink it, we need to determine
    whether it was clicked. If yes, then it should not shrink (nothing will happen)*/
    function shrinkRectangle(d) {
       
        var object = d3.select(this);
    
        if (object.attr("clicked") == "false") { //should shrink
        object.attr("height", rectHeight)
          .attr("y", rectYCoor1);
        } else {
            //do nothing - should not shrink
        }
    }


    /*This function happens when you click a rectangle. 
    It checks to see if it was already clicked: 
    If yes, then it needs to minimize it. 
    If not, it needs to get bigger.*/
    function clickRectangle(d) {
        
        //saves clicked rectange into this variable (for easier use)
        var object = d3.select(this);

        //need to get the old height: 
        var oldHeight = d3.select(this).attr("height");
        //has it already been clicked?
        if (object.attr("clicked") == "false") {//needs to grow - 

        rectangles1.each(shrinkAllRectangles);
        rectangles2.each(shrinkAllRectangles);
        //changes the height and the y and the clicked
        object
            .attr("clicked", true)
            .attr("height", rectHeight * rectGrowthFactor)
            .attr("y", 15);    //(height - oldHeight)/4 //but honestly can hard code this


        //names_original = element.getAttribute("name").split(" ");
      for (var i=0; i<rectangleArray.length; i++) {
        console.log("one:" + rectangleArray);

        var comp = rectangleArray.id;

      if (object.id == comp) {
        console.log(document.getElementsByName(comp));
        document.getElementsByName(comp)
                                    .setAttribute("clicked", true)
                                    .setAttribute("height", rectHeight * rectGrowthFactor)
                                    .setAttribute("y", 15);    //(height - oldHeight)/4 //but honestly can hard code this
        
      }
    }

        //also need to show information about variant: 
        document.getElementById("info").innerHTML = "<br><u>Selected Variant:</u> " + object.attr("info");
        } else { //it needs to be minimized
        //changes the height and the y and the clicked
        object
            .attr("clicked", false)
            .attr("height", rectHeight)
            .attr("y", rectYCoor1);

        document.getElementById("info").innerHTML = "";

        }  
    }


    /*This function happens when you click a rectangle: it shrinks all the rectangles so 
    that only the one you will have clicked will be big*/
    function shrinkAllRectangles(d) {
        //shrinking the object
        var object = d3.select(this);
    
        object.attr("height", rectHeight)
                .attr("clicked", false)
                .attr("y", rectYCoor1);
    }


    /*The below lines of code create hatched patterns for carrier (created three separate ones, 
    in different colors so that each pattern is a different color)*/

    //This one is for the Pathogenic ones (red)
    svgContainer1.append('defs')
                .append('pattern')
                .attr('id', 'PathDiag')
                .attr('patternUnits', 'userSpaceOnUse')
                .attr('width', 4)
                .attr('height', 4)
                .append('path')
                .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
                .attr('stroke', "#ff6666")
                .attr('stroke-width', 1);


    //This one is for the Benign ones (gray)
    svgContainer1.append('defs')
                .append('pattern')
                .attr('id', 'BenDiag')
                .attr('patternUnits', 'userSpaceOnUse')
                .attr('width', 4)
                .attr('height', 4)
                .append('path')
                .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
                .attr('stroke', "#cccccc")
                .attr('stroke-width', 1);

    //This one is for the Benign ones (gray)
    svgContainer1.append('defs')
                .append('pattern')
                .attr('id', 'ProtDiag')
                .attr('patternUnits', 'userSpaceOnUse')
                .attr('width', 4)
                .attr('height', 4)
                .append('path')
                .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
                .attr('stroke', "#89b4fd")
                .attr('stroke-width', 1);

    /*All the below ones are for the second svg containers -- need to at some point make this into a loop*/
    //This one is for the Pathogenic ones (red)
    svgContainer2.append('defs')
                .append('pattern')
                .attr('id', 'PathDiag')
                .attr('patternUnits', 'userSpaceOnUse')
                .attr('width', 4)
                .attr('height', 4)
                .append('path')
                .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
                .attr('stroke', "#ff6666")
                .attr('stroke-width', 1);


    //This one is for the Benign ones (gray)
    svgContainer2.append('defs')
                .append('pattern')
                .attr('id', 'BenDiag')
                .attr('patternUnits', 'userSpaceOnUse')
                .attr('width', 4)
                .attr('height', 4)
                .append('path')
                .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
                .attr('stroke', "#cccccc")
                .attr('stroke-width', 1);

    //This one is for the Benign ones (gray)
    svgContainer2.append('defs')
                .append('pattern')
                .attr('id', 'ProtDiag')
                .attr('patternUnits', 'userSpaceOnUse')
                .attr('width', 4)
                .attr('height', 4)
                .append('path')
                .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
                .attr('stroke', "#89b4fd")
                .attr('stroke-width', 1);

    
            
        
    //do not think this is necessary
    // function carrierStatus(d) {
    //     console.log("i am in carrier status");
    //     svgContainer.append('rect')
    //             .attr("x", function(d){ return d[1] })
    //             .attr("y", rectYCoor)
    //             .attr("width", function(d) { return d[0] })
    //             .attr("height", rectHeight)
    //             //.attr("fill", 'url(#' + type + 'Diag')
    //             .attr("fill", 'url(#PathDiag)')
    //             .attr("stroke", function(d){ return d[2][1]})
    //             .attr("stroke-width", 2)
    //             .on("mouseover", growRectangle)
    //             .on("mouseout", shrinkRectangle);
    //     }
//}
});
