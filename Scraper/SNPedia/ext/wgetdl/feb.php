
<!DOCTYPE>
<html>
	<head>

		<title>Visualization</title>

		<!--original css-->
		<link rel="stylesheet" href="css/feb.css">
		<!--font awesome css-->
		<link rel="stylesheet" href="css/font-awesome-4.4.0/css/font-awesome.min.css">
		<!--font-->
		<link href='http://fonts.googleapis.com/css?family=Raleway:500,700,400' rel='stylesheet' type='text/css'>
		<!--js-->
		<script type="text/javascript" src="js/feb.js"></script>

		<!--tooltips-->
		<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  		<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

  		<!-- font awesome -->
  		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">

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
    	<script src="js/libs/modernizr-2.0.6.min.js"></script>
	    <meta name="viewport" content="width=device-width, initial-scale=1">
	    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
	    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
	    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
	    <!-- .old header content-->

	    <!-- need for tooltips -->
	    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
  		<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>

	    <script>

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
	            <span class="brand" style="font-size:24px; padding-left:40px !important"><img src="assets/img/dna.png"> Genomix: Genome Visualization</span>
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

				<div class="row">

		    		<div class="col-sm-2" style="background-color:#f2f2f2;">
		    			<div style="background-color:#f2f2f2;height:77%">


<!-- ************* K E Y *************** -->

		    			<br>

		    			<b>Graph type:
				        <div id="view_selection">
				          	<a href="#" id="year"><button>Overview</button></a> 
				          	<a href="#" id="cata"><button>Category</button></a>
				        </div>  <!-- end of #btn-group -->

				        <br>Display size by:
		              	<div id="rarity_penetrance">
	                        <a href="#" id="pen"><button>Risk</button></a> 
	                        <a href="#" id="rar"><button>Rarity</button></a>
	                    </div>  <!-- end of #btn-group -->
	                    </b>
	                    

	                    <h3>Key</h3>

<!-- @@@@ note to self: come back and clean this with css @@@@-->

	                    <!-- *** all the rest of the legends start here (grouped seperately because of how they are displayed) *** -->

            			<div id="AllLegends" class="legend-scale" >

            				<button class="btn btn-click btn-md" title="The potential effect of a gene variant describes how it may influence a persons chances of developing a disease or what medication may work best for them.">
	            				<b>Color </b> 
							    <i class="fa fa-info-circle fa-lg"></i>
							</button>

            				<table class="legend-table">
            					<tr>
            						<td><div style='background-color:#cccccc;height:16px;width:30px;border:1px solid #999'></div></td>
            						<td>Benign</td>
            					</tr>
            					<tr>
            						<td><div style='background-color:#ff6666;height:16px;width:30px;border:1px solid #999'></div></td>
            						<td>Pathogenic</td>
            					</tr>
            					<tr>
            						<td><div style='background-color:#89b4fd;height:16px;width:30px;border:1px solid #999'></div></td>
            						<td>Protective</td>
            					</tr>
            					<tr>
            						<td><div style='background-color:#e77ee7;height:16px;width:30px;border:1px solid #999'></div></td>
            						<td>Pharma/Drug Response</td>
            					</tr>
            				</table>

            				<br>

						    <div>
						    	<button class="btn btn-click btn-md" title="Carrier Status is important in determining the gene variant’s effect. Each person inherits two variants of each gene, one from their biological father and one from their biological mother. A person is either a carrier of or affected by each gene.">
								    <b>Filled vs. Hollow</b> 
								    <i class="fa fa-info-circle fa-lg"></i>
								</button>

							    <br><img id="circle" src="img/filled.png" width="20px" alt="Rarity"/>&nbspPotentially Affected
							    <br><img id="circle" src="img/hallow.png" width="20px" alt="Rarity"/>&nbspCarrier
						    </div>

						    <br>

						    <!-- RISK KEY STARTS -->
            				<div id="risk_key">
            					<button class="btn btn-click btn-md" title="How often individuals carrying the variant develop the associated disease">
	              					<b>Size by Risk</b>
	              					<i class="fa fa-info-circle fa-lg"></i>
	              				</button>
              					<a id="risk_tooltip"></a>
              					<br><img id="circle" src="img/circlesizing.png" width="100%" alt="Risk"/> <!-- need to change this image -->
              					<br><span style="float:left">Less Risk</span><span style="float:right">More Risk</span>            				
              				</div> <!-- end risk key-->

            				<!-- RARITY KEY STARTS!!!! (ENCOMPASSES A LOT OF STUFF THAT WAS REPEATED ABOVE BECAUSE IT OVERRIDES RISK TOOLTIP ABOVE!!): -->
            				<div id="rarity_key" style="visibility: hidden;">
            					<button class="btn btn-click btn-md" title="Rarity, also know as frequency in population or allele frequency, describes the percentage of the population that has this genetic variant. The smaller the frequency, the less common it is among the population and the more interesting it is to a healthcare professional.">
	            					<b>Size by Rarity</b>
	            					<i class="fa fa-info-circle fa-lg"></i>
	            				</button>
	            				<a id="rarity_tooltip"></a>
				                <br><img id="circle" src="img/circlesizing.png" width="100%" alt="Rarity"/>
				                <br><span style="float:left">Less Rare</span><span style="float:right">More Rare</span>
          					</div> <!-- end rarity key -->

          				</div>  <!-- end of #legend-scale -->

		    		</div></div> <!-- end col-sm-2 (legend bootstrap) -->


<!-- ****************  E N D   O F   K E Y  *************************** -->

		    		<div class="col-sm-7">
		    			<div id="overview_background" class="overview_background">

		    			<!--bubbles dynamically added here-->
		    			<div id="main" style="z-index=-500;height:1px;width:1px">

			              	<!-- *** CANVAS STARTS HERE *** -->
			              	<div id="canvas" class="canvas" style="margin-top:0px;height:1px;width:1px">
			                	<div id="myCanvas"  style= "height:1px;weight:1px">
			                	</div>
			              	</div> <!-- end of #canvas -->

			              	<div id="vis" style="margin-top:0px; height:1px" >
			              		<!-- stuff will get dynamically placed in here when bubbles start to get created -->
			              	</div> <!-- end of #vis -->

		    			</div> <!-- end of #main -->

					    <!--create graph-->
						<div class="overview">

							<div id="categoriesQ1" class="cat_labels row" style="visibility:hidden">
								<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants associated with birth defects as well as gene variants associated with birth defects and genetic syndromes affecting multiple aspects of biology. (Ex. Increased or decreased susceptibility to cleft palate or dwarfism).">
		          						Anatomical
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants associated with the blood. (Ex. Increased or decreased susceptibility to Hemophilia or Anemia).">
		          						Blood
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants associated with the organs involved in breathing such as the lungs. (Ex. Increased or decreased susceptibility to Bronchitis or COPD).">
		          						Breathing
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants associated with an increased or decreased risk of cancer. (Ex. Increased or decreased susceptibility to Breast cancer or Melanoma).">
		          						Cancer
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>
	         				</div>

	         				<div id="certainty_tt" class="graph_label row" style="height:20%">
								<div class="col-sm-1"></div>
								<button class="btn btn-click btn-md col-sm-4" title="The certainty of a gene variant describes how well-established the scientific data is behind the effect of the gene variant.">
									CERTAINTY OF EVIDENCE 
									<i class="fa fa-info-circle fa-lg"></i>
								</button>
							</div>

							<div id="well-established_tt" class="graph_labels row">
								<div class="col-sm-3">
									<button class="btn btn-click btn-md" style="float:right" title="The research behind the effect of a gene variant is well-established.">
										Well-Established
										<i class="fa fa-info-circle fa-lg"></i>
									</button>
								</div>
							</div>

							<div id="categoriesQ2" class="cat_labels row" style="visibility:hidden; height:25%">
								<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants that may affect how one reacts to medications.">
		          						Drug Response
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants that are associated with the genitals and reproductive organs as well as gene variants that are associated with urinary system, which includes the kidneys. (Ex. Increased or decreased susceptibility to Kidney Disease or Endometriosis).">
		          						Genital & Urinary
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants that are associated with hearing and vision. (Ex. Increased or decreased susceptibility to Deafness or Age-related Macular Degeneration).">
		          						Hearing & Vision
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants that are associated with the heart and the circulatory system that are not specifically associated with the blood. (Ex. Increased or decreased susceptibility to heart defects or arrhythmia).">
		          						Heart & <br>Circulatory
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>
	         				</div>

	         				<div id="likely_tt" class="graph_labels row">
								<div class="col-sm-3">
									<button class="btn btn-click btn-md" style="float:right" title="The research behind the effect of a gene variant is not as well-established, and therefore the effect described is only likely linked to the gene variant.">
										Likely
										<i class="fa fa-info-circle fa-lg"></i>
									</button>
								</div>
							</div>

							<div id="categoriesQ3" class="cat_labels row" style="visibility:hidden; height:25% !important;">

								<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants that are associated with the immune system and autoimmune diseases. (Ex. Increased or decreased susceptibility to the flu or Celiac Sprue disease).">
		          						Immune System
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>

	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants that are associated with mental and behavioral disorders. (Ex. Increased or decreased susceptibility to depression or schizophrenia).">
	          							<div>
	          								Mental & Behavioral
	          								<i class="fa fa-info-circle fa-lg"></i>
	          							</div>
		         					</button>
		         				</div>

								<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants that are associated with the chemical transformations that happen throughout the body. (Ex. Increased or decreased susceptibility to Cushing’s Disease or high cholesterol).">
		          						Metabolism
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>

	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants associated with the teeth, gums, liver, and the rest of the digestive system. (Ex. Increased or decreased susceptibility to Crohn’s disease or gum disease).">
		          						Mouth, Liver <br>& Digestive
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
		         				</div>

	         				</div> <!-- end categoriesQ3 -->

	         				

							<div id="uncertain_tt" class="graph_labels row" style='height:10%'>
								<div class="col-sm-3">
									<button class="btn btn-click btn-md" style="float:right" title="The research behind the effect of a gene variant is uncertain, and therefore there is little evidence that links the effect to the gene variant.">
										Uncertain
										<i class="fa fa-info-circle fa-lg"></i>
									</button>
								</div>
							</div>

							<div id="categoriesQ4" class="cat_labels row" style="visibility:hidden; height:20%">
								<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants associated with the muscles, bones, and connective tissue. (Ex. Increased or decreased susceptibility to Arthritis or Muscular Dystrophy).">
		          						Muscular, Skeletal, & <br>Connective Tissue
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
	         					</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants associated with the brain and the spinal cord / nervous system. (Ex. Increased or decreased susceptibility to Seizures or Multiple Sclerosis).">
		          						Nervous System
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
	         					</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants associated with the skin. (Ex. Increased or decreased susceptibility to Eczema or Psoriasis).">
		          						Skin
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
	         					</div>
	         					<div class="col-sm-3">
									<button class="btn btn-click btn-md" title="Contains gene variants that are benign, do not fit into the other health categories, or that may have been missed when sorted into health categories.">
		          						Other
		          						<i class="fa fa-info-circle fa-lg"></i>
		         					</button>
	         					</div>
	         				</div>

							<div id="health_labels">

								<div class="row">

									<div class="col-sm-3">
									</div>
									
									<div id="low_tt">
										<div class="col-sm-3">
											<button class="btn btn-click btn-md" title="Genes in this category have a low heath effect.">
												Low
												<i class="fa fa-info-circle fa-lg"></i>
											</button>
										</div>
									</div>
									<div id="medium_tt">
										<div class="col-sm-3">
											<button class="btn btn-click btn-md" title="Genes in this category have a medium heath effect.">
												Medium
												<i class="fa fa-info-circle fa-lg"></i>
											</button>
										</div>
									</div>
									<div id="high_tt">
										<div class="col-sm-3">
											<button class="btn btn-click btn-md" title="Genes in this category have a high heath effect.">
												High 
												<i class="fa fa-info-circle fa-lg"></i>
											</button>
										</div>
									</div>

								</div> <!-- end heath labels row -->

								<br>

								<div id="health_axis_label" class="axes_label row">

									<div class="col-sm-6"></div>

									<button class="btn btn-click btn-md col-sm-3" title="Health Effect is based on three different variables. Severity, treatability and risk of the disease associated with the variant. The higher the health effect score, the more important it is to discuss with a medical professional.">
										HEALTH EFFECT
										<i class="fa fa-info-circle fa-lg"></i>
									</button>

								</div>

							</div>

						</div> <!-- .overview -->

		    		</div></div> <!--end col-sm-7 (overview section) -->
		    		
		    		<div class="col-sm-3" style="background-color:#f2f2f2; height:80%">
		    			<div style="background-color:#f2f2f2;">
			    			<h3>Variant Information</h3>
			    			<div id="var_info" style="font-size:16px"></div>
			    			<div id="second_info"></div>

							<br/>

							<button style="position:absolute;bottom:10px;right:10px" data-role="button" id="testButton" size="10px" style="visibility:hidden">SAVE</button>
							<button style="position:absolute;bottom:10px;left:10px" data-role="button" id="saveButton" size="10px" style="visibility:hidden">CLEAR</button>

						
			    	</div></div> <!--end col-sm-3 (variant info column) -->

			    </div> <!--end row-->

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

		

			<!-- ******************* NOTEBOOK CONTENT ********************* -->

			<!-- Tab 4 Content-->
			<div id="tab-content4" class="tab-content">

				<span style="float:left">Welcome, PGP user #huMTURK!<br><a href='login.php'>Not huMTURK? Click here.</a></span>

				<br><br>

				<!-- <input type="text" id="createPageTitle"></input>
				<button data-role="button" id="createPageButton" size="10px">CREATE</button>




				 -->

					
			</div> <!-- #tab-content4 -->

		</div> 

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
	    <script type="text/javascript" src="js/feb.js"></script>
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

	      	$('.btn-click').tooltip({trigger: "click", placement: "bottom"});

	      	//creates variant page when variant is saved
	      	var add = document.getElementById("testButton");
            add.onclick = function () {
            	var current_var = document.getElementById("var_info").innerHTML;
            	dbData = {variant: current_var};

			    $.ajax({
	              url: 'save.php', //link to php file
	              type: 'POST',
	              data: dbData, 
	              success: function (success) {
	                //alert(current_var);
	              }
	            });
            }

            //adds a new page when "create" button is pressed
            var createPage = document.getElementById("createPageButton");
            createPage.onclick = function () {
            	var title = document.getElementById("createPageTitle").value;
            	//currently saves as "variant", eventually change to own file
            	createData = {variant: title};

			    $.ajax({
	              url: 'save.php', //link to php file
	              type: 'POST',
	              data: createData, 
	              success: function (success) {
	                //alert(title);
	              }
	            });
            }


	        $('#rarity_penetrance a').click(function() {
	          var secview_type = $(this).attr('id');
	          $('#rarity_penetrance a').removeClass('active');
	          $(this).toggleClass('active');
	          custom_bubble_chart.toggle_view(secview_type);
	          return false;
	        });
	      });

	      var $template = $(".template");
	      var divHeader = document.getElementById('var_info').innerHTML;

			var hash = 2;
			$(".btn-add-panel").on("click", function () {
			    var $newPanel = $template.clone();
			    $newPanel.find(".collapse").removeClass("in");
			    $newPanel.find(".accordion-toggle").attr("href", "#" + (++hash))
			        .text(divHeader);
			    $newPanel.find(".panel-collapse").attr("id", hash);
			    $("#accordion").append($newPanel.fadeIn());
			});

			$(document).on('click', '.glyphicon-remove-circle', function () {
			    $(this).parents('.panel').get(0).remove();
			});

	    </script>

	</body>
</html>

