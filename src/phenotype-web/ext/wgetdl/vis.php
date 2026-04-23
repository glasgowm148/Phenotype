
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
    
    <script>
      $(function() {
        $( "#accordionGlossary" ).accordion({
          heightStyle: "content"
        });
      });
    </script>

    <script>
      $(function() {
        $("#instructions").accordion({
          active: false,
          collapsible: true,
          heightStyle: "content"
        });
      });
    </script>	
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

  <div style="padding-left:30px; width:65%;">
    <br>
<h2>Instructions</h2>
      <br>
        <p style="font-size:14px">Following is a report that is based on an individual's personal genomic information. For the purpose of this study we will name this individual Jamie. Read the explanation below carefully and then study Jamie's gene variant report. You will be asked questions about this report.
        <br><br>The report was created by comparing Jamie's genome and a database of gene variants that are known to be associated with medical conditions. Only gene variants that are found to be medically relevant are reported.
        <br><br>Instructions for reading this visualization of Jamie's genome can be found in the accordion below.
        <br><br>Feel free to open the instructions on how to read this visualization before or while interacting with Jamie's genome data. After exploring Jamie's genome data, please answer the questions below.</p>
    <br>
    <br>
  </div>

  <div style="margin-left:10px; width:90%">
    <div id="instructions">
      <h7 style="font-size:16">How to read the visualization</h7>
      <p style="font-size:14px">The report displays a bubble chart visualization of Jamie's gene variant report.  A gene variant controls a person's physical and medical traits. Each gene variant is represented by a bubble. 
      <br>
      <br>The “Overview” contains the results of Jamie's genome test. In the “Overview”, bubbles are organized by the certainty of the scientific evidence on a particular gene variant as well as by the potential health effect of the gene variant. There are three levels of certainty; uncertain, likely, and well-established. There are also three levels of potential health effect; low, medium, and high.  
      <br>
      <br>You may change the view to organize the chart by “By Category.” In the “By Category” view, gene variants may appear in multiple categories and therefore multiple bubbles will represent one gene variant.  When you click on a gene variant bubble in one category, all bubbles representing the same gene variant will be highlighted.  Also, if you change between the “By Category” and “Overview” views, the bubble will remain highlighted.  
      <br>
      <br>Please use the glossary of terms and the glossary of health categories to clarify any terms that you are not familiar with.  The glossary of terms provides more in depth explanations of all terms used in the visualization. The glossary of health categories provides explanations of the health categories used in the “By Category” view.  
      <br>
      <br>
      <img src="img/vis_instructions.jpg">
      <br>
      <br>
    </div>
  </div>



<!--************** VIS START ******************-->

  

 <div id="container" class="container"> 
    <div id="accordion" class="accordion_class" width="190px" style="float: right;  margin-top:240px; padding-right: 10px;">
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

 
  <!--  the three main buttons (tabs) -->
  <div id="view_selection" class="btn-group" style="">
    <a href="#" id="year" class="btn active" style="border-left: 5px solid #0f82f5; border-top: 5px solid #0f82f5;">Overview</a> 
    <a href="#" id="cata" class="btn" style="border-top: 5px solid #0f82f5;">By Category</a>
    <a href="#" id="glossary" class="btn" style="border-right: 5px solid #0f82f5;border-top: 5px solid #0f82f5;" >Glossary</a>
  </div>  <!-- end of #btn-group -->

   <br>
   <br>

  <!-- this creates the line at the top that is blue and makes it look like tabs -->
  <div id="topLine" class="btn-group" style="visibility: visible; border-bottom: 5px solid #0f82f5; width: 100%; height:5px; padding-left: 0px; padding-top: 0.9px; width: 1330px;">
  </div>

  <br>
  <br>
  <br>

  <!-- this saves a spot for where the glossary accordion is supposed to go when "glossary" is clicked -->
  <div id ="accordionPlace">
  </div>

  <div id="main" >
    <div id="title" style="width:1330px; padding-left: 10px;">
     <div id="bigTitle" style="font-size:35px; font-family:Raleway;">
      <br>
        <b>Gene Variant Report</b>
      </div><br>
      <br>
    <!-- the title starts of as this, this will change dynamically when you change tabs -->
    <span id="smallTitle" style="font-size:15px; font-family:Raleway;">
    Showing certainty of evidence and health effect of documented gene variants (July 2015) 
    </span><br> 
  </div> <!-- *** title ends here *** -->



  <!-- *** CERTAINTY TOOLTIP *** -->
  <div id="certainty_tooltip" class="btn-group" style="visibility: visible; margin-left: 340px; margin-top: 0px; width:180px;">
    &nbsp
    <a style="width: 22px; height: 22px;" id="certainty_qmark">
      <img src="img/certainty.png" alt="Info" height="35px" style="opacity: 1;" />
    </a>
  </div> <!-- *** CERTAINTY TOOLTIP ENDS HERE *** -->
    


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

    <span style="font-size:18px;">
      <b>Legend</b> 
    </span>

    <br><br>

    <form id="rarity_penetrance" style="padding-left: 0px; margin-bottom:0px; padding-bottom:0px;">
      <table style="font-size: 10px;">
        <tr>
          <td >
            <input id="pen" type="radio" name="size" value="pen" checked>&nbsp&nbspDisplay size by risk
          </td>
        </tr>
        <tr>
          <td>
            <input id="rar" type="radio" name="size" value="rar">&nbsp&nbspDisplay size by rarity
          </td>
        </tr>
      </table>
    </form>

  </div>

  <div id="info" style="padding-left:1030px; margin-top:-170px; width:300px" >
  </div> <!-- end of #info -->


</div> <!-- end of #container -->



<!-- *** the first FOUR categories *** -->
 <div id="categoriesQ1" class="btn-group" style="visibility: visible; float: left; width: 1040px; height:50px; margin-left: 210px; margin-top: 10px; ">

            <a style="width: 22px; height: 22px;" id="cat1_tooltip">
        <img src="img/anatomical.png" id="testing123" alt="Info" height="50px" style="opacity: 1;" />
         </a>



      <a style="width: 22px; height: 22px; padding-left: 60px;" id="cat2_tooltip">
        <img src="img/blood.png" alt="Info" height="40px" style="opacity: 1;" />
         </a>


       <a style="width: 22px; height: 22px; padding-left: 70px;" id="cat3_tooltip">
        <img src="img/breathing.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>


       <a style="width: 22px; height: 22px; padding-left: 65px;" id="cat4_tooltip">
        <img src="img/cancer.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>

  </div> <!-- *** the first FOUR categories end here *** -->




<div id="infoblurb" style="width:300px; padding: 15px" >  <!--not used but keep because of the space breaks are in the page -->

  <td id="more" style="display:none;"></td>
  <br>
  <br>
  <br>
  <br>

</div>





<!-- *** all the rest of the legends start here (grouped seperately because of how they are displayed) *** -->
<div id="legend" class="my-legend">


<div id="AllLegends" class="legend-scale" >
<b>Color Key</b>


<span id="color" >
    <a style = "width: 22px; height: 22px;" id="color_tooltip">
        <img src="img/info.png" alt="Info" width="13px" height="13px" style="opacity: 0.3;" />
    </a>
  </span>


<!-- *** WELL-ESTABLISHED TOOLTIP STARTS HERE *** -->
<span id="well-established" style="visibility: visible; border-radius: 5px; margin-left: 115px; padding: 3px; width:125px;">
 <img src="img/well-established.png" alt="Info" height="35px" style="opacity: 1;" />
</span> <!-- *** WELL-ESTABLISHED TOOLTIP ENDS HERE *** -->


  <ul class="legend-labels">
    <li><span style='background:#cccccc;'></span>Benign</li>
    <li><span style='background:#ff6666;'></span>Pathogenic</li>
    <li><span style='background:#89b4fd;'></span>Protective</li>
    <li><span style='background:#e77ee7;'></span>Pharma/Drug Response</li>



<!-- the second FOUR categories -->
<div id="categoriesQ2" class="btn-group" style="visibility: visible; width: 1000px; padding-left: 200px; padding-top: 0px;">

          <a style="width: 22px; height: 22px;" id="cat5_tooltip">
          <img src="img/drug.png" alt="Info" height="35px" style="opacity: 1;" />
         </a>

      <a style="width: 22px; height: 22px; padding-left: 40px;" id="cat6_tooltip">
        <img src="img/genital.png" alt="Info" height="40px" style="opacity: 1;" />
         </a>

       <a style="width: 22px; height: 22px; padding-left: 10px;" id="cat7_tooltip">
        <img src="img/hearing.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>

       <a style="width: 22px; height: 22px; padding-left: 10px;" id="cat8_tooltip">
        <img src="img/heart.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>

  </div> <!-- *** the second four categories end here *** -->
   


    <b>Filled vs. Hollow Key </b> 

    <a style = "width: 22px; height: 22px;" id="hollow_tooltip">
        <img src="img/info.png" alt="Info" width="13px" height="13px" style="opacity: 0.3;" />
    </a>

 
  <span id="likely" style="visibility: visible; border-radius: 5px; margin-left: 120px; padding: 3px; width:125px;">
 <img src="img/likely.png" alt="Info" height="35px" style="opacity: 1;" />
</span>
</span>


    <br> 
    <li> &nbsp
    <img id="circle" src="img/filled.png" width="30px" alt="Rarity"/>
    &nbsp &nbsp &nbsp &nbsp 
    <img id="circle" src="img/hallow.png" width="30px" alt="Rarity"/>
    &nbsp &nbsp &nbsp &nbsp 
    <img id="circle" src="img/dotted.png" width="30px" alt="Dotted"/>
    </li> 
    <li>Potentially &nbsp &nbsp  Carrier &nbsp &nbsp &nbsp &nbsp No Freq<br>
    <li>Affected &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp  Recorded </li>



<!-- the third FOUR categories -->
       <div id="categoriesQ3" class="btn-group" style="visibility: visible; width: 1000px; height: 10px; padding-top: 0px;"> 

            <a style="width: 22px; height: 22px; padding-left: 200px;" id="cat9_tooltip">
        <img src="img/immune.png" alt="Info" height="40px" style="opacity: 1;" />
         </a>


      <a style="width: 22px; height: 22px; padding-left: 30px" id="cat10_tooltip">
        <img src="img/mental.png" alt="Info" height="40px" style="opacity: 1;" />
         </a>


       <a style="width: 22px; height: 22px; padding-left: 20px;" id="cat11_tooltip">
        <img src="img/metabolism.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>




       <a style="width: 22px; height: 22px; padding-left: 45px;" id="cat12_tooltip">
        <img src="img/mouth.png" alt="Info" height="50px" style="opacity: 1;" />
    </a>

  </div> <!-- *** the third four categories end here *** -->

  <br><br>

  


<!-- RISK KEY STARTS -->
    <div id="risk_key">
    <b>Size by Risk Key </b> 


    <a style = "width: 22px; height: 22px;" id="risk_tooltip">
        <img src="img/info.png" alt="Info" width="13px" height="13px" style="opacity: 0.3;" />
    </a>



    <li><img id="circle" src="img/circlesizing.png" width="150px" alt="Risk"/></li> <!-- need to change this image -->
    <li>Less Risk &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp More Risk </li>

  <span id="uncertain" style="border-radius: 5px; margin-left: 240px; padding: 3px; width:125px;">
 <img src="img/uncertain.png" alt="Info" height="35px" style="opacity: 1;" />
</span>



<!-- the fourth three categories -->
  <div id="categoriesQ4" class="btn-group" style="width: 1000px; height:10px; padding-left: 180px; padding-top: 0px;">


      <a style="width: 22px; height: 22px;" id="cat13_tooltip">
        <img src="img/muscular.png" alt="Info" height="50px" style="opacity: 1;" />
         </a>

      <a style="width: 22px; height: 22px; padding-left: 10px;" id="cat14_tooltip">
        <img src="img/nervous.png" alt="Info" height="40px" style="opacity: 1;" />
         </a>

       <a style="width: 22px; height: 22px; padding-left: 45px;" id="cat15_tooltip">
        <img src="img/skin.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>

       <a style="width: 22px; height: 22px; padding-left: 100px;" id="cat16_tooltip">
        <img src="img/other.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>

  </div> <!-- the fourth three categories end here -->



<!-- HEALTH TOOLTIP BEGINS -->
 <div id="health_tooltip" class="btn-group" style="margin-left: 690px; margin-top: 10px; width:125px;">
&nbsp
            <a style="width: 22px; height: 22px;" id="health_qmark">
        <img src="img/health.png" alt="Info" height="35px" style="opacity: 1;" />
         </a>
  </div> <!-- HEALTH TOOLTIP ENDS -->

<br>

<!-- the health labels: -->
<span id="health_labels" style= "padding-left: 30%;">
    <span id="low" style="padding: 3px; width:10%;">
 <img src="img/low.png" alt="Info" height="35px" style="opacity: 1;" />
</span>

<span id="medium" style="border-radius: 5px; padding: 3px; width:10%px;">
 <img src="img/medium.png" alt="Info" height="35px" style="opacity: 1; padding-left: 7%;" />
</span>

<span id="high" style="border-radius: 5px; padding: 3px; width:10%;">
 <img src="img/high.png" alt="Info" height="35px" style="opacity: 1; padding-left: 8%;" />
</span>

</span> <!-- the health labels END: -->



<!-- RARITY KEY STARTS!!!! (ENCOMPASSES A LOT OF STUFF THAT WAS REPEATED ABOVE BECAUSE IT OVERRIDES RISK TOOLTIP ABOVE!!): -->

    <div id="rarity_key" style="visibility: hidden;">
    <b>Size by Rarity Key</b>

    <a style = "width: 22px; height: 22px;" id="rarity_tooltip">
        <img src="img/info.png" alt="Info" width="13px" height="13px" style="opacity: 0.3;" />
    </a>

    <li><img id="circle" src="img/circlesizing.png" width="150px" alt="Rarity"/></li> 
    <li>Less Rare &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp More Rare </li>

    <span id="uncertain" style="border-radius: 5px; margin-left: 240px; padding: 3px; width:125px;">
 <img src="img/uncertain.png" alt="Info" height="35px" style="opacity: 1;" />
</span>



<!-- the fourth three categories -->
  <div id="categoriesQ5" class="btn-group" style="width: 1000px; height:10px; padding-left: 180px; padding-top: 0px;">


            <a style="width: 22px; height: 22px;" id="cat13_tooltip">
        <img src="img/muscular.png" alt="Info" height="50px" style="opacity: 1;" />
         </a>



      <a style="width: 22px; height: 22px; padding-left: 10px;" id="cat14_tooltip">
        <img src="img/nervous.png" alt="Info" height="40px" style="opacity: 1;" />
         </a>



       <a style="width: 22px; height: 22px; padding-left: 45px;" id="cat15_tooltip">
        <img src="img/skin.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>


       <a style="width: 22px; height: 22px; padding-left: 100px;" id="cat16_tooltip">
        <img src="img/other.png" alt="Info" height="40px" style="opacity: 1;" />
    </a>

  </div> <!-- the fourth three categories END -->



<!-- the health certainty tooltip -->
   <div id="health_tooltip" class="btn-group" style="margin-left: 690px; margin-top: 10px; width:125px;">

&nbsp
            <a style="width: 22px; height: 22px;" id="health_qmark">
        <img src="img/health.png" alt="Info" height="35px" style="opacity: 1;" />
         </a>
  </div> <!-- the health certainty tooltip ENDS -->

<br>



<!-- the health labels tooltip -->
<span id="health_labels2" style= "padding-left: 380px;">
    <span id="low" style="padding: 3px; width:125px;">
 <img src="img/low.png" alt="Info" height="35px" style="opacity: 1;" />
</span>

<span id="medium" style="border-radius: 5px; padding: 3px; width:125px;">
 <img src="img/medium.png" alt="Info" height="35px" style="opacity: 1; padding-left: 90px;" />
</span>

<span id="high" style="border-radius: 5px; padding: 3px; width:125px;">
 <img src="img/high.png" alt="Info" height="35px" style="opacity: 1; padding-left: 105px;" />
</span>

</span> <!-- the health labels tooltip ends -->




  </ul>  <!-- stops all lists -->




</div>  <!-- end of #legend-scale -->



</div>  <!-- end of #legend-title -->

<div id="fillGlossary"style="visibility:hidden;">
  
   <div id="accordionGlossary" >
    <h8>A</h8>
  <div>
    <p><b>Anatomical and Congenital:</b> Contains gene variants associated with birth defects as well as gene variants associated with birth defects and genetic syndromes affecting multiple aspects of biology. (Ex. Increased or decreased susceptibility to cleft palate or dwarfism)</p>
  </div>
  <h8>B</h8>
  <div>
    <p><b>Benign:</b> Not associated to a disease.<br>
       <b>Blood:</b> Contains gene variants associated with the blood.  (Ex. Increased or decreased susceptibility to Hemophilia or Anemia).<br>
       <b>Breathing:</b> Contains gene variants associated with the organs involved in breathing such as the lungs. (Ex. Increased or decreased susceptibility to Bronchitis or COPD).
    </p>
  </div>

    <h8>C</h8>
  <div>
    <p><b>Cancer:</b> Contains gene variants associated with an increased or decreased risk of cancer.  (Ex. Increased or decreased susceptibility to Breast cancer or Melanoma).<br>
    <b>Carrier Status:</b> Carrier Status is important in determining the gene variant’s effect. Each person inherits two variants of each gene, one from their biological father and one from their biological mother. A person is either a carrier of or affected by each gene. <br>
    <b>Carrier:</b> A carrier for a particular gene variant is heterozygous for a gene variant with a recessive effect. This means that a carrier will not be affected by the gene variant; however if their child receives this gene variant from both parents, the child will potentially be affected.<br>
    <b>Certainty:</b> The certainty of a gene variant describes how well-established the scientific data is behind the effect of the gene variant. <br>
    <b>Compound Heterozygous:</b> The variants of two different genes work together to create the same effect as being homozygous for one of the genes.
  </p>
  </div>

      <h8>D</h8>
  <div>
    <p><b>Dominant:</b> Dominant variants are expected to have the reported impact when just one copy is inherited (heterozygous).<br>
    <b>Drug Response:</b> Contains gene variants that may affect how one reacts to medications.
  </p>
  </div>

  <h8>G</h8>
  <div>
    <p><b>Genital and Urinary:</b> Contains gene variants that are associated with the genitals and reproductive organs as well as gene variants that are associated with urinary system, which includes the kidneys. (Ex. Increased or decreased susceptibility to Kidney Disease or Endometriosis).
  </p>
  </div>

  <h8>H</h8>
  <div>
    <p><b>Health Category:</b> The health category of the gene variant is aspect of individual biology and health that the gene variant may affect. Many times, gene variants affect multiple aspects of individual biology or multiple areas of the body, and therefore fall into/appear in multiple categories. <br>
      <b>Health Effect:</b> Health Effect is based on three different variables. Severity, treatability and risk of the disease associated with the variant. The higher the health effect score, the more important it is to discuss with a medical professional. <br>
      <b>Hearing and Vision:</b> Contains gene variants that are associated with hearing and vision. (Ex. Increased or decreased susceptibility to Deafness or Age-related Macular Degeneration). <br>
<b>Heart and Circulatory:</b> Contains gene variants that are associated with the heart and the circulatory system that are not specifically associated with the blood.  (Ex. Increased or decreased susceptibility to heart defects or arrhythmia). <br>
<b>Heterozygous:</b> The two variants of the gene are different (the person has two different variants). <br>
<b>Homozygous:</b> The two variants of the gene are the same.
  </p>
  </div>

  <h8>I</h8>
  <div>
    <p><b>Immune System:</b> Contains gene variants that are associated with the immune system and autoimmune diseases. (Ex. Increased or decreased susceptibility to the flu or Celiac Sprue disease).
  </p>
  </div>

    <h8>L</h8>
  <div>
    <p><b>Likely:</b> The research behind the effect of a gene variant is not as well-established, and therefore the effect described is only likely linked to the gene variant.
  </p>
  </div>

      <h8>M</h8>
  <div>
    <p><b>Mental and Behavioral:</b> Contains gene variants that are associated with mental and behavioral disorders. (Ex. Increased or decreased susceptibility to depression or  schizophrenia).<br>
      <b>Metabolism:</b> Contains gene variants that are associated with the chemical transformations that happen throughout the body. (Ex. Increased or decreased susceptibility to Cushing’s Disease or high cholesterol). <br>
      <b>Mouth, Liver, and Digestive:</b> Contains gene variants associated with the teeth, gums, liver, and the rest of the digestive system. (Ex. Increased or decreased susceptibility to Crohn’s disease or gum disease). <br>
      <b>Muscular, Skeletal, and Connective Tissue:</b> Contains gene variants associated with the muscles, bones, and connective tissue. (Ex. Increased or decreased susceptibility to Arthritis or Muscular Dystrophy).
  </p>
  </div>

        <h8>N</h8>
  <div>
    <p><b>Nervous System:</b> Contains gene variants associated with the brain and the spinal cord / nervous system.  (Ex. Increased or decreased susceptibility to Seizures or Multiple Sclerosis).     
  </p>
  </div>

        <h8>O</h8>
  <div>
    <p><b>Other:</b> Contains gene variants that are benign, do not fit into the other health categories, or that may have been missed when sorted into health categories. Variants defined as "other" encompasses various possibilities. Some variants have a strong effect when homozygous and a weaker effect when heterozygous, or others only seem to have an effect on traits when another variant is also present.
  </p>
  </div>

          <h8>P</h8>
  <div>
    <p><b>Pathogenic:</b> May cause disease. <br>
      <b>Pharmacogenetic / drug response:</b> May influence the effect of a medication. <br>
      <b>Potential Effect:</b> The potential effect of a gene variant describes how it may influence a person's chances of developing a disease or what medication may work best for them. <br>
<b>Potentially Affected:</b> Someone who is potentially affected by a gene variant has a higher risk or likelihood of developing the conditions associated with that gene variant.<br>
<b>Protective:</b> May prevent disease.

  </p>
  </div>

            <h8>R</h8>
  <div>
    <p><b>Rarity:</b> Rarity, also know as frequency in population or allele frequency, describes the percentage of the population that has this genetic variant. The smaller the frequency, the less common it is among the population and the more interesting it is to a healthcare professional. If there is “No Freq Recorded,”  the frequency of the gene variant is unknown. <br>
      <b>Recessive:</b> Recessive variants are not expected to have the reported impact unless homozygous or compound heterozygous. <br>
      <b>Risk:</b> Risk, also known as penetrance, describes how often individuals carrying the variant develop the associated disease. A variant with a higher penetrance means that a person with this variant is more likely to develop the associated disease. (Note: These scores are considered irrelevant for "benign" variants. Benign variants includes those which affect traits not considered to be medical/health issues, e.g. eye color.

  </p>
  </div>


            <h8>S</h8>
  <div>
    <p><b>Severity:</b> How severe the disease caused by a variant is, if left untreated. For protective variants this is the severity of the disease the variant protects against, and for pharmacogenetic variants it is the severity of consequences if the variant was not considered when administering a drug. <br>
    <b>Skin:</b> Contains gene variants associated with the skin. (Ex. Increased or decreased susceptibility to Eczema or Psoriasis).
  </p>
  </div>

            <h8>T</h8>
  <div>
    <p><b>Treatability:</b> How treatable the disease caused by the variant is. A higher score indicates a more treatable effect. Variants which could be treated are considered to have higher clinical importance.
  </p>
  </div>

            <h8>U</h8>
  <div>
    <p><b>Uncertain:</b> The research behind the effect of a gene variant is uncertain, and therefore there is little evidence that links the effect to the gene variant.
  </p>
  </div>

              <h8>W</h8>
  <div>
    <p><b>Well-established:</b> The research behind the effect of a gene variant is well-established.
  </p>
  </div>


    </div>
</div>


<style type='text/css'>
 
</style>


  </div> <!-- end of #my-legend -->
  </div> <!-- end of #main -->



  <script>window.jQuery || document.write('<script src="js/libs/jquery-1.6.2.min.js"><\/script>')</script>

  <script defer src="js/plugins.js"></script>
  <script defer src="js/script.js"></script>
  <script src="js/CustomTooltip.js"></script>
  <script src="js/libs/coffee-script.js"></script>
  <script src="js/libs/d3.js"></script>
  <script type="text/javascript" src="js/vis.js"></script>
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