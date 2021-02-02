
<!DOCTYPE>
<html class="no-js" lang="en">
	<!--
	Wellesley HCI PGP 
	Lauren Westendorf
	Summer 2015
	Bub Vis Opinion Questions
	-->
	
<html>
	<head>
		<title>Visualization</title>
    <link href='http://fonts.googleapis.com/css?family=Raleway:500,700,400' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" type="text/css" href="vis_style.css">
		<script type="text/javascript" charset="utf8" src="../pghci/vis/resource/js/jquery-1.10.2.js"></script>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<meta name="description" content="">
		<meta name="author" content="">
		<meta name="viewport" content="width=device-width,initial-scale=1">
		<!-- CSS concatenated and minified via ant build script-->
		<link rel="stylesheet" href="css/reset.css">
		<link rel="stylesheet" href="css/bootstrap.min.css">
		<link rel="stylesheet" href="css/style.css">
    <!-- end CSS-->
    <script src="js/libs/modernizr-2.0.6.min.js"></script>

    <script>
      $(document).ready(function() {
        $('[data-toggle="tooltip"]').tooltip();
      });
    </script>

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>

    <script>

      var okay = 1;

      $(document).ready(function() {

        function createAccordion() {
          //creates the accordions so they show up 
          $("#Queen").accordion();
          $("#Queen").accordion("option", "active", ":last");
          createAccordion();
        } 

        $( ".bread" ).accordion({     //class of the Ace (first) accordion
          header: "> div > h3",
          collapsible: true,
          active: false,
          autoHeight: false, 
          autoActivate: true
        });

        $( ".sandwich" ).accordion({   //class of the King (second) accordion
          header: "> div > h3",
          collapsible: true,
          active: false,
          autoHeight: false, 
          width: 400,
          autoActivate: true
        });
    
        $( ".bread" ).sortable({
          axis: "y",
          handle: "h3",
          items: "div",
          receive: function(event, ui) {
            $(ui.item).removeClass();
            $(ui.item).removeAttr("style");
            $( ".bread" ).accordion("add", "<div>" + ui.item.hmtl() + "</div>");
          }
        });

        $( ".sandwich" ).sortable({
          axis: "y",
          handle: "h3",
          items: "div",
          receive: function(event, ui) {}
        });

        //the first accordion that will only have one element, where you can add to the second accordion
        $( "#Ace" ).accordion({       
          header: "> div > h3",
          collapsible: true,
          active: false,
          autoHeight: false
        });

        //second accordion, contains all the saved variant panels
        $( "#King" ).accordion({   
          header: "> div > h3",
          collapsible: true,
          active: false,
          autoHeight: false
        });

        $( "button" ).button();

      });

      window.foo = function(e) {
        e.stopPropagation();
        document.getElementById("saveButton").disabled = true; //this disabled the save button
      }

    </script>

    <meta charset="utf-8">
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <link rel="stylesheet" href="/resources/demos/style.css">


	
  	</head>

    <body>
      <header>
        <div class="navbar navbar-fixed-top navbar-inverse">
          <div class="navbar-inner">
            <div class="container">
              <span class="brand"><img src="assets/img/dna.png"> Visualization</span>
            </div>
          </div>
        </div>
      </header>

      <br>
      <br>
      <br>
      <br>

<!--************** VIS START ******************-->

      <!--  the three main buttons (tabs) --> 
      <div id="view_selection">
          <a href="#" id="year">Overview</a> 
          <a href="#" id="cata">By Category</a>
          <a href="#" id="glossary">Glossary</a>
      </div>  <!-- end of #btn-group -->

          <div id="container" class="container"> 
                <div id="accordion" class="accordion_class" width="190px" style="float: right;  margin-top:10px; padding-right: 10px;">
                    <div id="both_suits" style="height: 590px; padding-top: 5px;">

                      <div style="font-size:18px; padding-bottom:10px;">
                          <b>Variant Information</b>
                      </div>

                      <div  id="Ace"class="bread" style="visibility:hidden;" >
                          <div>

                            <h3 style="float:right;" onclick='$("#King").accordion( "option", "active","false");' class="toolbar ui-widget-header ui-corner-all">
                                <a href="#" id="var_info"></a>
                                <button style="float:right" data-role="button" id="saveButton" size="10px"onclick="document.getElementById('saveButton').disabled = true;">SAVE</button>
                            </h3>

                            <div  id="second_info" style="float: right; height: false;padding-right: 50px;">
                                <br>
                            </div> 

                          </div>
                      </div>
                
                      <div id="King" class= "sandwich" style="margin-top:65px;">
                      <!-- gets filled dynamically in NewDiv() in save Button function -->
                      </div>

            </div> <!--both suits div end-->
          </div>
         
              <div id="ahead_1"  class="accord_header" style="visibility: hidden;" style="display:inline;" >
                <!--  <a href="#" id="var_info" class="btn"><button type="var_info" onclick="console.log('hii reveal'); console.log(this.parent);" width="20px"></button></a>  -->
                <a href="#"   class="accord_header" width="20px"></a>                 
                <a href="#" id="save" ><img src="img/save.png" width=".0px"/></a> 
                <a href="#" style="visibility:hidden;" id="exit"></a> 
              </div>   

              <div id= "acontent_1" class = "accord_content" style="visibility: hidden;">
                <div id="second_info" ></div>
              </div>

              <div id="ahead_2"class = "accord_header" style="visibility: hidden;">Section 2</div>

              <br>
              <br>
              <br>

              <div id="main" >

                  <!-- *** CANVAS STARTS HERE *** -->
                  <div id="canvas" class="canvas" style="margin-left: 140px; margin-top:0px">
                    <div id="myCanvas"  style= "padding-left:0px; margin-left:200px; margin-top:-50px; border-radius:5px; background-image:url(http://i62.tinypic.com/5ra1h.png); background-size: 490px 575px; width: 490px; height: 575px;">
                    </div>
                  </div> <!-- end of #canvas -->

                  <div id="vis" style="padding-left:90px; margin-top:-200px;" >
                    <!-- stuff will get dynamically placed in here when bubbles start to get created -->
                  </div> <!-- end of #vis -->

                  <!-- *** LEGEND STARTS HERE *** -->
                  <div id="legend" class="my-legend" style="margin-left: 5px; padding-top: 5px; height:605px; width: 165px; border: 1px dotted gray; border-radius: 5px; visbility: visible;">

                    <br><br>

                    <!--<form id="rarity_penetrance" style="padding-left: 0px; margin-bottom:0px; padding-bottom:0px;">
                      <table style="font-size: 10px;">
                          <tr>
                            <td>
                                <input id="pen" type="radio" name="size" value="pen" checked>&nbsp&nbspDisplay size by risk
                            </td>
                          </tr>
                          <tr>
                            <td>
                                <input id="rar" type="radio" name="size" value="rar">&nbsp&nbspDisplay size by rarity
                            </td>
                          </tr>
                      </table>
                    </form> -->

                     <div id="rarity_penetrance">
                          <a href="#" id="pen">Risk</a> 
                          <a href="#" id="rar">Rarity</a>
                      </div>  <!-- end of #btn-group -->

                </div>

                <div id="info" style="padding-left:1030px; margin-top:-170px; width:300px" >
                </div> <!-- end of #info -->

            </div> <!-- end of #container -->

          <!-- *** all the rest of the legends start here (grouped seperately because of how they are displayed) *** -->
          <div id="legend" class="my-legend">

                  <div id="AllLegends" class="legend-scale" >

                      <ul class="legend-labels">
                        <!-- RISK KEY STARTS -->
                        <div id="risk_key">
                            <b>Size by Risk Key </b> 
                            <a style = "width: 22px; height: 22px;" id="risk_tooltip">
                                <img src="img/info.png" alt="Info" width="13px" height="13px" style="opacity: 0.3;" />
                            </a>
                            <li><img id="circle" src="img/circlesizing.png" width="150px" alt="Risk"/></li> <!-- need to change this image -->
                            <li>Less Risk &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp More Risk </li>

                            <br>
                        </div> <!-- the health labels END: -->

                        <!-- RARITY KEY STARTS!!!! (ENCOMPASSES A LOT OF STUFF THAT WAS REPEATED ABOVE BECAUSE IT OVERRIDES RISK TOOLTIP ABOVE!!): -->
                        <div id="rarity_key" style="visibility: hidden;">
                          <b>Size by Rarity Key</b>
                          <a style = "width: 22px; height: 22px;" id="rarity_tooltip">
                              <img src="img/info.png" alt="Info" width="13px" height="13px" style="opacity: 0.3;" />
                          </a>
                          <li><img id="circle" src="img/circlesizing.png" width="150px" alt="Rarity"/></li> 
                          <li>Less Rare &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp More Rare </li>

                        </div> <!-- the health labels tooltip ends -->

                    </ul>  <!-- stops all lists -->

                  </div>  <!-- end of #legend-scale -->

              </div> <!-- end of #my-legend -->
            
          </div> <!-- end of #main -->



    <script>window.jQuery || document.write('<script src="js/libs/jquery-1.6.2.min.js"><\/script>')</script>

    <script defer src="js/plugins.js"></script>
    <script defer src="js/script.js"></script>
    <script src="js/CustomTooltip.js"></script>
    <script src="js/libs/coffee-script.js"></script>
    <script src="js/libs/d3.js"></script>
    <script type="text/javascript" src="js/new.js"></script>
    <script type="text/javascript">

    var variant_report = "huMTURK";
    //var variant_report = "hu0A4518"; //hu2DBF2D


      //to make the correct report appear:
      function setVariantReport() {

        variant_report=document.getElementById("variantReport").value;

        //clear: ++++ need to clear the side info thing! 
        document.getElementById('vis').innerHTML = "";

        d3.csv("data/csv_genome_reports/"+variant_report+".csv", function(data) {
          custom_bubble_chart.init(data);
          custom_bubble_chart.toggle_view('year');       
        });
      }

      d3.csv("data/csv_genome_reports/"+variant_report+".csv", function(data) {
        custom_bubble_chart.init(data);
        custom_bubble_chart.toggle_view('year');       
      });
 
      $(document).ready(function() {
        $('#view_selection a').click(function() {
          var view_type = $(this).attr('id');
          $('#view_selection a').removeClass('active');
          $(this).toggleClass('active');
          custom_bubble_chart.toggle_view(view_type);
          return false;
        });
      });

      //this is for the rarity/penetrance, it makes the things actually get "clicked"
      $(document).ready(function() {
        $('#rarity_penetrance a').click(function() {
          var secview_type = $(this).attr('id');
          $('#rarity_penetrance a').removeClass('active');
          $(this).toggleClass('active');
          custom_bubble_chart.toggle_view(secview_type);
          return false;
        });
      });

    </script>

	</body>
</html>