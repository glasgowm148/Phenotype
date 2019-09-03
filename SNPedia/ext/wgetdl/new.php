
<!DOCTYPE>
<html>
	<head>

		<title>Visualization</title>

		<!--original css-->
		<link rel="stylesheet" href="css/new.css">
		<!--font awesome css-->
		<link rel="stylesheet" href="css/font-awesome-4.4.0/css/font-awesome.min.css">
		<!--font-->
		<link href='http://fonts.googleapis.com/css?family=Raleway:500,700,400' rel='stylesheet' type='text/css'>
		<!--js-->
		<script type="text/javascript" src="js/new.js"></script>

		<!--tooltips-->
		<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  		<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

		<!-- ********* old header content ******* -->
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
    	<script src="js/libs/modernizr-2.0.6.min.js"></script>
	    <meta name="viewport" content="width=device-width, initial-scale=1">
	    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
	    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
	    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
	    <!-- .old header content-->

	    <!-- accordion code -->
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
	    <!-- end accordion code -->

	</head>

	<body>

		<header>
	      <div class="navbar navbar-fixed-top navbar-inverse">
	        <div class="navbar-inner">
	          <div class="container">
	            <span class="brand"><img src="assets/img/dna.png"> Genomix: Genome Visualization</span>
	          </div>
	        </div>
	      </div>
	    </header>

	    <!--tab code source: http://webdesignerhut.com/create-pure-css-tabs/ -->
	    <div class="tabs">
		   	<!-- Radio button and lable for #tab-content1 -->
			<input type="radio" name="tabs" id="tab1" checked>
			<label for="tab1">
				<span>Visualization</span>
			</label>

			<!-- Radio button and lable for #tab-content3 -->
			<input type="radio" name="tabs" id="tab3">
			<label for="tab3">
				<span>Glossary</span>
			</label>

			<!-- Radio button and lable for #tab-content4 -->
			<input type="radio" name="tabs" id="tab4">
			<label for="tab4">
				<span>Notebook</span>
			</label>

			<!-- ******************* OVERVIEW CONTENT ********************* -->

			<!-- Tab 1 Content-->
			<div id="tab-content1" class="tab-content">

		            <div id="accordion" class="accordion_class" width="190px" style="float: right; margin-top:10px; padding-right: 10px;">
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

		            <div id="main" style="z-index=-500;height:1px">

		              	<!-- *** CANVAS STARTS HERE *** -->
		              	<div id="canvas" class="canvas" style="margin-left: 140px; margin-top:0px;height:1px">
		                	<div id="myCanvas"  style= "padding-left:0px; margin-left:200px; margin-top:-50px; border-radius:5px; background-image:url(http://i62.tinypic.com/5ra1h.png); background-size: 490px 575px; width: 490px; height: 575px;">
		                	</div>
		              	</div> <!-- end of #canvas -->

		              	<div id="vis" style="margin-left:200px; margin-top:0px; height:1px" >
		              		<!-- stuff will get dynamically placed in here when bubbles start to get created -->
		              	</div> <!-- end of #vis -->

		              	<!-- *** LEGEND STARTS HERE *** -->
		              	<div id="legend" class="my-legend" style="margin-left: 5px; padding-top: 5px; height:605px; width: 165px; border: 1px dotted gray; border-radius: 5px; visbility: visible;">

		              		<br><br>

			              	<!--  the three main buttons (tabs) --> 
					        <div id="view_selection">
					          	<a href="#" id="year">Overview</a> 
					          	<a href="#" id="cata">Category</a>
					        </div>  <!-- end of #btn-group -->

			              	<div id="rarity_penetrance">
		                        <a href="#" id="pen">Risk</a> 
		                        <a href="#" id="rar">Rarity</a>
		                    </div>  <!-- end of #btn-group -->

            			</div>

			            <div id="info" style="padding-left:1030px; margin-top:-170px; width:300px" >
			            </div> <!-- end of #info -->

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

	    		<!--create graph-->
				<div class="overview">

		    		<div class="all_labels" style="z-index=-200;">

						<div id="certainty_tt" class="graph_labels" style="width:100%; text-align:right; padding-right:83%">
							<a href="#" data-toggle="tooltip" title="The certainty of a gene variant describes how well-established the scientific data is behind the effect of the gene variant.">
								<img src="img/certainty.png" alt="Certainty of Evidence" height="30px" style="opacity: 1;" />
							</a>
						</div>

						<table id="categoriesQ1" class="cat_labels" style="width:80%"> <!--4 column, 4 row table with indices (row, column)-->
							<tr>
								<!--Table Cell (0,0)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants associated with birth defects as well as gene variants associated with birth defects and genetic syndromes affecting multiple aspects of biology. (Ex. Increased or decreased susceptibility to cleft palate or dwarfism).">
		          						<img src="img/anatomical.png" alt="Anatomical and Congenial" height="45px" style="opacity: 1;" />
		         					</a>
		     					</td>
		     					<!--Table Cell (0,1)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants associated with the blood. (Ex. Increased or decreased susceptibility to Hemophilia or Anemia).">
		          						<img src="img/blood.png" alt="Blood" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
								<!--Table Cell (0,2)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants associated with the organs involved in breathing such as the lungs. (Ex. Increased or decreased susceptibility to Bronchitis or COPD).">
		          						<img src="img/breathing.png" alt="Breathing" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
								<!--Table Cell (0,3)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants associated with an increased or decreased risk of cancer. (Ex. Increased or decreased susceptibility to Breast cancer or Melanoma).">
		          						<img src="img/cancer.png" alt="Cancer" height="40px" style="opacity: 1;" />
		         					</a>
								</td>
							</tr>
						</table>

						<div id="well-established_tt" class="graph_labels" style="width:100%; text-align:right; padding-right:83%; height:20%">
							<a href="#" data-toggle="tooltip" title="The research behind the effect of a gene variant is well-established.">
								<img src="img/well-established.png" alt="Well-Established" height="35px" style="opacity: 1;"/>
							</a>
						</div>

						<table id="categoriesQ2" class="cat_labels" style="width:80%; height:5%">
							<tr>
								<!--Table Cell (1,0)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants that may affect how one reacts to medications.">
		          						<img src="img/drug.png" alt="Drug Response" height="35px" style="opacity: 1;" />
		         					</a>
		     					</td>
		     					<!--Table Cell (1,1)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants that are associated with the genitals and reproductive organs as well as gene variants that are associated with urinary system, which includes the kidneys. (Ex. Increased or decreased susceptibility to Kidney Disease or Endometriosis).">
		          						<img src="img/genital.png" alt="Genital and Urinary" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
								<!--Table Cell (1,2)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants that are associated with hearing and vision. (Ex. Increased or decreased susceptibility to Deafness or Age-related Macular Degeneration).">
		          						<img src="img/hearing.png" alt="Hearing and Vision" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
								<!--Table Cell (1,3)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants that are associated with the heart and the circulatory system that are not specifically associated with the blood. (Ex. Increased or decreased susceptibility to heart defects or arrhythmia).">
		          						<img src="img/heart.png" alt="Heart and Circulatory" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
							</tr>
						</table>

						<div id="likely_tt" class="graph_labels" style="width:100%; text-align:right; padding-right:83%; height:15%">
							<a href="#" data-toggle="tooltip" title="The research behind the effect of a gene variant is not as well-established, and therefore the effect described is only likely linked to the gene variant.">
								<img src="img/likely.png" alt="Likely" height="35px" style="opacity: 1;" />
							</a>
						</div>

						<table id="categoriesQ3" class="cat_labels" style="width:80%; height:17%">
							<tr>
								<!--Table Cell (2,0)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants that are associated with the immune system and autoimmune diseases. (Ex. Increased or decreased susceptibility to the flu or Celiac Sprue disease).">
		          						<img src="img/immune.png" alt="Immune System" height="35px" style="opacity: 1;" />
		         					</a>
		     					</td>
		     					<!--Table Cell (2,1)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants that are associated with mental and behavioral disorders. (Ex. Increased or decreased susceptibility to depression or schizophrenia).">
		          						<img src="img/mental.png" alt="Mental and Behavioral" height="40px" style="opacity: 1;" />
		         					</a>
								</td>
								<!--Table Cell (2,2)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants that are associated with the chemical transformations that happen throughout the body. (Ex. Increased or decreased susceptibility to Cushing’s Disease or high cholesterol).">
		          						<img src="img/metabolism.png" alt="Metabolism" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
								<!--Table Cell (2,3)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants associated with the teeth, gums, liver, and the rest of the digestive system. (Ex. Increased or decreased susceptibility to Crohn’s disease or gum disease).">
		          						<img src="img/mouth.png" alt="Mouth, Liver, and Digestive" height="45px" style="opacity: 1;" />
		         					</a>
								</td>
							</tr>
						</table>

						<div id="uncertain_tt" class="graph_labels" style="width:100%; text-align:right; padding-right:83%;">
							<a href="#" data-toggle="tooltip" title="The research behind the effect of a gene variant is uncertain, and therefore there is little evidence that links the effect to the gene variant.">
								<img src="img/uncertain.png" alt="Uncertain" height="35px" style="opacity: 1;" />
							</a>
						</div>

						<table id="categoriesQ4" class="cat_labels" style="width:80%; height:5%;">
							<tr>
								<!--Table Cell (3,0)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants associated with the muscles, bones, and connective tissue. (Ex. Increased or decreased susceptibility to Arthritis or Muscular Dystrophy).">
		          						<img src="img/muscular.png" alt="Muscular, Skeletal, and Connective Tissue" height="45px" style="opacity: 1;" />
		         					</a>
		     					</td>
		     					<!--Table Cell (3,1)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants associated with the brain and the spinal cord / nervous system. (Ex. Increased or decreased susceptibility to Seizures or Multiple Sclerosis).">
		          						<img src="img/nervous.png" alt="Nervous System" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
								<!--Table Cell (3,2)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants associated with the skin. (Ex. Increased or decreased susceptibility to Eczema or Psoriasis).">
		          						<img src="img/skin.png" alt="Skin" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
								<!--Table Cell (3,3)-->
								<td>
									<a href="#" data-toggle="tooltip" title="Contains gene variants that are benign, do not fit into the other health categories, or that may have been missed when sorted into health categories.">
		          						<img src="img/other.png" alt="Other" height="35px" style="opacity: 1;" />
		         					</a>
								</td>
							</tr>
						</table>

						<table id="health_labels" class="graph_labels" style="width:80%; float:right">
							<tr>
								<td></td>
								<td id="low_tt" >
									<a href="#" data-toggle="tooltip" title="LOW">
										<img src="img/low.png" alt="Well-Established" height="35px" style="opacity: 1;"/>
									</a>
								</td>
								<td id="medium_tt" style="width:20%">
									<a href="#" data-toggle="tooltip" title="MEDIUM">
										<img src="img/medium.png" alt="Likely" height="35px" style="opacity: 1;" />
									</a>
								</td>
								<td id="high_tt" style="width:20%">
									<a href="#" data-toggle="tooltip" title="HIGH">
										<img src="img/high.png" alt="Uncertain" height="35px" style="opacity: 1;" />
									</a>
								</td>
								<td id="high_tt" style="width:10%">
								</td>
								<td>
									<a href="#" data-toggle="tooltip" title="Health Effect is based on three different variables. Severity, treatability and risk of the disease associated with the variant. The higher the health effect score, the more important it is to discuss with a medical professional.">
										<img src="img/health.png" alt="Heath Effect" height="30px" style="opacity: 1;" />
									</a>
								</td>
							</tr>
						</table>
					
					</div> <!-- end #all-labels -->

				</div><!-- .overview -->

				
			

			</div> <!-- #tab-content1 -->

			<!-- Tab 3 Content-->
			<div id="tab-content3" class="tab-content">
				<h3>Glossary</h3>
				
				<div class="glossary">

					<!--***************GLOSSARY MECHANICS************************-->

				   	<!-- Radio button and lable for #tab-contentA -->
					<input type="radio" name="glossary" id="glossaryA" checked>
					<label for="glossaryA">
						<span>A</span>
					</label>

					<!-- Radio button and lable for #tab-contentB -->
					<input type="radio" name="glossary" id="glossaryB">
					<label for="glossaryB">
						<span>B</span>
					</label>

					<!-- Radio button and lable for #tab-contentC -->
					<input type="radio" name="glossary" id="glossaryC">
					<label for="glossaryC">
						<span>C</span>
					</label>

					<!-- Radio button and lable for #tab-contentD -->
					<input type="radio" name="glossary" id="glossaryD">
					<label for="glossaryD">
						<span>D</span>
					</label>

					<!-- Radio button and lable for #tab-contentE -->
					<input type="radio" name="glossary" id="glossaryE">
					<label for="glossaryE">
						<span>E</span>
					</label>

					<!-- Radio button and lable for #tab-contentF -->
					<input type="radio" name="glossary" id="glossaryF">
					<label for="glossaryF">
						<span>F</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentG -->
					<input type="radio" name="glossary" id="glossaryG">
					<label for="glossaryG">
						<span>G</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentH -->
					<input type="radio" name="glossary" id="glossaryH">
					<label for="glossaryH">
						<span>H</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentI -->
					<input type="radio" name="glossary" id="glossaryI">
					<label for="glossaryI">
						<span>I</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentJ -->
					<input type="radio" name="glossary" id="glossaryJ">
					<label for="glossaryJ">
						<span>J</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentK -->
					<input type="radio" name="glossary" id="glossaryK">
					<label for="glossaryK">
						<span>K</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentL -->
					<input type="radio" name="glossary" id="glossaryL">
					<label for="glossaryL">
						<span>L</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentM -->
					<input type="radio" name="glossary" id="glossaryM">
					<label for="glossaryM">
						<span>M</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentN -->
					<input type="radio" name="glossary" id="glossaryN">
					<label for="glossaryN">
						<span>N</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentO -->
					<input type="radio" name="glossary" id="glossaryO">
					<label for="glossaryO">
						<span>O</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentP -->
					<input type="radio" name="glossary" id="glossaryP">
					<label for="glossaryP">
						<span>P</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentQ -->
					<input type="radio" name="glossary" id="glossaryQ">
					<label for="glossaryQ">
						<span>Q</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentR -->
					<input type="radio" name="glossary" id="glossaryR">
					<label for="glossaryR">
						<span>R</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentS -->
					<input type="radio" name="glossary" id="glossaryS">
					<label for="glossaryS">
						<span>S</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentT -->
					<input type="radio" name="glossary" id="glossaryT">
					<label for="glossaryT">
						<span>T</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentU -->
					<input type="radio" name="glossary" id="glossaryU">
					<label for="glossaryU">
						<span>U</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentV -->
					<input type="radio" name="glossary" id="glossaryV">
					<label for="glossaryV">
						<span>V</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentW -->
					<input type="radio" name="glossary" id="glossaryW">
					<label for="glossaryW">
						<span>W</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentX -->
					<input type="radio" name="glossary" id="glossaryX">
					<label for="glossaryX">
						<span>X</span>
					</label>
					
					<!-- Radio button and lable for #tab-contentY -->
					<input type="radio" name="glossary" id="glossaryY">
					<label for="glossaryY">
						<span>Y</span>
					</label>

					<!-- Radio button and lable for #tab-contentZ -->
					<input type="radio" name="glossary" id="glossaryZ">
					<label for="glossaryZ">
						<span>Z</span>
					</label>

					<!--***************GLOSSARY CONTENT************************-->

					<!-- Tab A Content-->
					<div id="glossary-contentA" class="glossary-content">
						
						<h3>A</h3>

						<p><b>Anatomical and Congenital:</b> Contains gene variants associated with birth defects as well as gene variants associated with birth defects and genetic syndromes affecting multiple aspects of biology. (Ex. Increased or decreased susceptibility to cleft palate or dwarfism)

					</div> <!-- #glossary-contentA -->

					<!-- Tab B Content-->
					<div id="glossary-contentB" class="glossary-content">
						
						<h3>B</h3>

						<p><b>Benign:</b> Not associated to a disease.<br>
				       	<p><b>Blood:</b> Contains gene variants associated with the blood.  (Ex. Increased or decreased susceptibility to Hemophilia or Anemia).<br>
				       	<p><b>Breathing:</b> Contains gene variants associated with the organs involved in breathing such as the lungs. (Ex. Increased or decreased susceptibility to Bronchitis or COPD).

					</div> <!-- #glossary-contentB -->

					<!-- Tab C Content-->
					<div id="glossary-contentC" class="glossary-content">
						
						<h3>C</h3>
						
						<p><b>Cancer:</b> Contains gene variants associated with an increased or decreased risk of cancer.  (Ex. Increased or decreased susceptibility to Breast cancer or Melanoma).<br>
				    	<p><b>Carrier Status:</b> Carrier Status is important in determining the gene variant’s effect. Each person inherits two variants of each gene, one from their biological father and one from their biological mother. A person is either a carrier of or affected by each gene. <br>
				    	<p><b>Carrier:</b> A carrier for a particular gene variant is heterozygous for a gene variant with a recessive effect. This means that a carrier will not be affected by the gene variant; however if their child receives this gene variant from both parents, the child will potentially be affected.<br>
				    	<p><b>Certainty:</b> The certainty of a gene variant describes how well-established the scientific data is behind the effect of the gene variant. <br>
				    	<p><b>Compound Heterozygous:</b> The variants of two different genes work together to create the same effect as being homozygous for one of the genes.
					  	
					</div> <!-- #glossary-contentC -->

					<!-- Tab D Content-->
					<div id="glossary-contentD" class="glossary-content">
						
						<h3>D</h3>
						
						<p><b>Dominant:</b> Dominant variants are expected to have the reported impact when just one copy is inherited (heterozygous).<br>
						<p><b>Drug Response:</b> Contains gene variants that may affect how one reacts to medications.
  						
					</div> <!-- #glossary-contentD -->

					<!-- Tab E Content-->
					<div id="glossary-contentE" class="glossary-content">

						<h3>E</h3>

						<p>No words yet!

					</div> <!-- #glossary-contentE -->

					<!-- Tab F Content-->
					<div id="glossary-contentF" class="glossary-content">
						
						<h3>F</h3>
						
						<p>No words yet!

					</div> <!-- #glossary-contentF -->

					<!-- Tab G Content-->
					<div id="glossary-contentG" class="glossary-content">
						<h3>G</h3>
						
						<p><b>Genital and Urinary:</b> Contains gene variants that are associated with the genitals and reproductive organs as well as gene variants that are associated with urinary system, which includes the kidneys. (Ex. Increased or decreased susceptibility to Kidney Disease or Endometriosis).

					</div> <!-- #glossary-contentG -->

					<!-- Tab H Content-->
					<div id="glossary-contentH" class="glossary-content">
						
						<h3>H</h3>
						
						<p><b>Health Category:</b> The health category of the gene variant is aspect of individual biology and health that the gene variant may affect. Many times, gene variants affect multiple aspects of individual biology or multiple areas of the body, and therefore fall into/appear in multiple categories. <br>
						<p><b>Health Effect:</b> Health Effect is based on three different variables. Severity, treatability and risk of the disease associated with the variant. The higher the health effect score, the more important it is to discuss with a medical professional. <br>
						<p><b>Hearing and Vision:</b> Contains gene variants that are associated with hearing and vision. (Ex. Increased or decreased susceptibility to Deafness or Age-related Macular Degeneration). <br>
						<p><b>Heart and Circulatory:</b> Contains gene variants that are associated with the heart and the circulatory system that are not specifically associated with the blood.  (Ex. Increased or decreased susceptibility to heart defects or arrhythmia). <br>
						<p><b>Heterozygous:</b> The two variants of the gene are different (the person has two different variants). <br>
						<p><b>Homozygous:</b> The two variants of the gene are the same.

					</div> <!-- #glossary-contentH -->

					<!-- Tab I Content-->
					<div id="glossary-contentI" class="glossary-content">
						
						<h3>I</h3>
						
						<p><b>Immune System:</b> Contains gene variants that are associated with the immune system and autoimmune diseases. (Ex. Increased or decreased susceptibility to the flu or Celiac Sprue disease).
  						
					</div> <!-- #glossary-contentI -->

					<!-- Tab J Content-->
					<div id="glossary-contentJ" class="glossary-content">
						
						<h3>J</h3>
						
						<p>No words yet!

					</div> <!-- #glossary-contentJ -->

					<!-- Tab K Content-->
					<div id="glossary-contentK" class="glossary-content">
						
						<h3>K</h3>
						
						<p>No words yet!

					</div> <!-- #glossary-contentK -->

					<!-- Tab L Content-->
					<div id="glossary-contentL" class="glossary-content">
						
						<h3>L</h3>
						
						<p><b>Likely:</b> The research behind the effect of a gene variant is not as well-established, and therefore the effect described is only likely linked to the gene variant.
  						
					</div> <!-- #glossary-contentL -->

					<!-- Tab M Content-->
					<div id="glossary-contentM" class="glossary-content">
						
						<h3>M</h3>
						
						<p><b>Mental and Behavioral:</b> Contains gene variants that are associated with mental and behavioral disorders. (Ex. Increased or decreased susceptibility to depression or  schizophrenia).<br>
				      	<p><b>Metabolism:</b> Contains gene variants that are associated with the chemical transformations that happen throughout the body. (Ex. Increased or decreased susceptibility to Cushing’s Disease or high cholesterol). <br>
				      	<p><b>Mouth, Liver, and Digestive:</b> Contains gene variants associated with the teeth, gums, liver, and the rest of the digestive system. (Ex. Increased or decreased susceptibility to Crohn’s disease or gum disease). <br>
				      	<p><b>Muscular, Skeletal, and Connective Tissue:</b> Contains gene variants associated with the muscles, bones, and connective tissue. (Ex. Increased or decreased susceptibility to Arthritis or Muscular Dystrophy).
					  	
					</div> <!-- #glossary-contentM -->

					<!-- Tab N Content-->
					<div id="glossary-contentN" class="glossary-content">
						
						<h3>N</h3>
						
						<p><b>Nervous System:</b> Contains gene variants associated with the brain and the spinal cord / nervous system.  (Ex. Increased or decreased susceptibility to Seizures or Multiple Sclerosis).     
  						
					</div> <!-- #glossary-contentN -->

					<!-- Tab O Content-->
					<div id="glossary-contentO" class="glossary-content">
						<h3>O</h3>
						
						<p><b>Other:</b> Contains gene variants that are benign, do not fit into the other health categories, or that may have been missed when sorted into health categories. Variants defined as "other" encompasses various possibilities. Some variants have a strong effect when homozygous and a weaker effect when heterozygous, or others only seem to have an effect on traits when another variant is also present.
  						
					</div> <!-- #glossary-contentO -->

					<!-- Tab P Content-->
					<div id="glossary-contentP" class="glossary-content">

						<h3>P</h3>
						
						<p><b>Pathogenic:</b> May cause disease. <br>
  						<p><b>Pharmacogenetic / drug response:</b> May influence the effect of a medication. <br>
  						<p><b>Potential Effect:</b> The potential effect of a gene variant describes how it may influence a person's chances of developing a disease or what medication may work best for them. <br>
						<p><b>Potentially Affected:</b> Someone who is potentially affected by a gene variant has a higher risk or likelihood of developing the conditions associated with that gene variant.<br>
						<p><b>Protective:</b> May prevent disease.
  						
					</div> <!-- #glossary-contentP -->

					<!-- Tab Q Content-->
					<div id="glossary-contentQ" class="glossary-content">

						<h3>Q</h3>

						<p>No words yet!

					</div> <!-- #glossary-contentQ -->

					<!-- Tab R Content-->
					<div id="glossary-contentR" class="glossary-content">
						
						<h3>R</h3>

						<p><b>Rarity:</b> Rarity, also know as frequency in population or allele frequency, describes the percentage of the population that has this genetic variant. The smaller the frequency, the less common it is among the population and the more interesting it is to a healthcare professional. If there is “No Freq Recorded,”  the frequency of the gene variant is unknown. <br>
					    <p><b>Recessive:</b> Recessive variants are not expected to have the reported impact unless homozygous or compound heterozygous. <br>
					    <p><b>Risk:</b> Risk, also known as penetrance, describes how often individuals carrying the variant develop the associated disease. A variant with a higher penetrance means that a person with this variant is more likely to develop the associated disease. (Note: These scores are considered irrelevant for "benign" variants. Benign variants includes those which affect traits not considered to be medical/health issues, e.g. eye color.
					
					</div> <!-- #glossary-contentR -->

					<!-- Tab S Content-->
					<div id="glossary-contentS" class="glossary-content">
						
						<h3>S</h3>

						<p><b>Severity:</b> How severe the disease caused by a variant is, if left untreated. For protective variants this is the severity of the disease the variant protects against, and for pharmacogenetic variants it is the severity of consequences if the variant was not considered when administering a drug. <br>
    					<p><b>Skin:</b> Contains gene variants associated with the skin. (Ex. Increased or decreased susceptibility to Eczema or Psoriasis).
					
					</div> <!-- #glossary-contentS -->

					<!-- Tab T Content-->
					<div id="glossary-contentT" class="glossary-content">
						
						<h3>T</h3>

						<p><b>Treatability:</b> How treatable the disease caused by the variant is. A higher score indicates a more treatable effect. Variants which could be treated are considered to have higher clinical importance.
					
					</div> <!-- #glossary-contentT -->

					<!-- Tab U Content-->
					<div id="glossary-contentU" class="glossary-content">
						
						<h3>U</h3>

						<p><b>Uncertain:</b> The research behind the effect of a gene variant is uncertain, and therefore there is little evidence that links the effect to the gene variant.
					
					</div> <!-- #glossary-contentU -->

					<!-- Tab V Content-->
					<div id="glossary-contentV" class="glossary-content">
						
						<h3>V</h3>

						<p>No words yet!
					
					</div> <!-- #glossary-contentV -->

					<!-- Tab W Content-->
					<div id="glossary-contentW" class="glossary-content">
						
						<h3>W</h3>

						<p><b>Well-established:</b> The research behind the effect of a gene variant is well-established.
					
					</div> <!-- #glossary-contentW -->

					<!-- Tab X Content-->
					<div id="glossary-contentX" class="glossary-content">
						
						<h3>X</h3>

						<p>No words yet!
					
					</div> <!-- #glossary-contentX -->

					<!-- Tab Y Content-->
					<div id="glossary-contentY" class="glossary-content">
						
						<h3>Y</h3>

						<p>No words yet!
					
					</div> <!-- #glossary-contentY -->

					<!-- Tab Z Content-->
					<div id="glossary-contentZ" class="glossary-content">
						
						<h3>Z</h3>

						<p>No words yet!
					
					</div> <!-- #glossary-contentZ -->

				</div> <!-- #glossary -->


			</div> <!-- #tab-content3 -->

		</div> 

		<!-- ******************* NOTEBOOK CONTENT ********************* -->

		<!-- Tab 4 Content-->
		<div id="tab-content4" class="tab-content">
				
		</div> <!-- #tab-content4 -->



		<!--tooltip script-->
		<script>
			$(document).ready(function(){
    			$('[data-toggle="tooltip"]').tooltip();  
			});
		</script>

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

