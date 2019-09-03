    // dimensions of svg canvas   
    var width = 600;
    var height = 400;
    // dataset to play with
    var dataset = [[50, "benign"], [40, "protective"], [80, "pathogenic"], [20, "carrier"]];
    var dataValues = dataset.map(function(v){return v[0]})
    // setting up plotting arrays for d3
    // each sub array is structured [width, xValue, fillColor, strokeColor]
    var dataSum = dataValues.reduce(function(a, b){return a+b});
    var datasetScaledValues = dataValues.map(function(a){return a / (dataSum + 2 * (dataset.length-1)) * width});
    var rectangleColors = {"protective" : ["#89b4fd", "black"],
                           "benign" : ["#cccccc", "black"],
                           "pathogenic" : ["#ff6666", "black"],
                           "carrier" : ["#ffffff", "red"]};
    var xValue = 1;
    dataArrays = []
    for ( i = 0 ; i < dataset.length ; i++ ){
        var dataArray = [];

        dataArray.push(datasetScaledValues[i]);
        if (i > 0){
            xValue += datasetScaledValues[i-1] + 2;
        }        

        // if (i == 0){
        //     var xValue = 0;
        // }
        // if (i == 1){
        //     xValue = datasetScaledValues[0];
        // }
        // else {
        //     xValue = datasetScaledValues.slice(0, i).reduce(function(a, b){return a + b});
        // }

        dataArray.push(xValue);
        dataArray.push(rectangleColors[dataset[i][1]]);

        dataArrays.push(dataArray);



    }
    // var scale = d3.scale.linear()
    //                     .domain(xMin, xMax)
    //                     .range(0, width);
	//Make an SVG Container
 	var svgContainer = d3.select("body").append("svg")
                                    	 .attr("width", width)
                                    	 .attr("height", height);
 
 	//Draw the Rectangle


    var rectHeight = 0.25 * height;
//    var rectX = dataset.slice(0, i).reduce(add, 0)

    svgContainer.selectAll("rect")
                .data(dataArrays)
                .enter()
                .append("rect")
                .attr("x", function(d){ return d[1] })
                .attr("y", 75)
                .attr("width", function(d) { return d[0] })
                .attr("height", rectHeight)
                .attr("fill", function(d) { return d[2][0] })
                .attr("stroke", function(d){ return d[2][1]})
                .attr("stroke-width", 2);


   

svgContainer
  .append('defs')
  .append('pattern')
    .attr('id', 'redDiagonal')
    .attr('patternUnits', 'userSpaceOnUse')
    .attr('width', 4)
    .attr('height', 4)
  .append('path')
    .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
    .attr('stroke', 'red')
    .attr('stroke-width', 1);

// svgContainer.append("rect")
//       .attr("x", 0)
//       .attr("width", 100)
//       .attr("height", 100)
//       .style("fill", 'yellow');
  
svgContainer.append("rect")
    .attr("x", 0)
    .attr("width", 100)
    .attr("height", 100)
    .attr('fill', 'url(#redDiagonal)');


	// var rectangle1 = svgContainer.append("rect")
 //                         	    .attr("x", 5)
 //                         	    .attr("y", 10)
 //                         	    .attr("width", 50)
 //                         	    .attr("height", 100)
 //                         	    .attr("fill", "gray")
 //                         	    .attr("stroke", "black")
 //                         	    .attr("stroke-width", 2);
 //    rectangle1.on("click", function () {
 //    	rectangle1.attr("height", 120)
 //    			.attr("y",0);
 //        rectangle2.attr("height", 100)
 //        .attr("y", 10);
 //        rectangle3.attr("height", 100)
 //        .attr("y", 10);
        
 //    });

 //    var rectangle2 = svgContainer.append("rect")
 //                         	    .attr("x", 55)
 //                         	    .attr("y", 10)
 //                         	    .attr("width", 40)
 //                         	    .attr("height", 100)
 //                         	    .attr("fill", "red")
 //                         	    .attr("stroke", "black")
 //                         	    .attr("stroke-width", 2);
 //    rectangle2.on("click", function () {
 //    	rectangle2.attr("height", 120)
 //    			.attr("y",0);
 //    	rectangle1.attr("height", 100)
 //        .attr("y", 10);
 //        rectangle3.attr("height", 100)
 //        .attr("y", 10);
 //    });

 //    var rectangle3 = svgContainer.append("rect")
 //                         	    .attr("x", 95)
 //                         	    .attr("y", 10)
 //                         	    .attr("width", 60)
 //                         	    .attr("height", 100)
 //                         	    .attr("fill", "blue")
 //                         	    .attr("stroke", "black")
 //                         	    .attr("stroke-width", 2);

 //    rectangle3.on("click", function () {
 //    	rectangle3.attr("height", 120)
 //    			.attr("y",0);
 //        rectangle1.attr("height", 100)
 //        .attr("y", 10);
 //        rectangle2.attr("height", 100)
 //        .attr("y", 10);
 //    });

