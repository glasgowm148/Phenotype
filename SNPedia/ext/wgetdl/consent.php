<!DOCTYPE>
<html>
	<head>
		<title>GenomiX Consent Form</title>
				
		
		<link href="bootswatch.css" rel="stylesheet">
		<link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">
		<link href="vis_style.css" rel="stylesheet">
		<style>
			.portrait { margin-left:7px; }
		</style>
	</head>
	<body>
	
	<div class="navbar navbar-fixed-top navbar-inverse">
	<div class="navbar-inner">
		<div class="container">
			<span class="brand"><img src="assets/img/dna.png"> GenomiX Consent Form</span>
		</div>
	</div>
	</div>
	
	<div class="container" style="margin-top:100px">
		<center><h2>Welcome to GenomiX!</h2></center>
		<p>
			GenomiX is a novel tool for self-exploration of personal genomic data. 
			Using data from the Personal Genome Project (PGP), GenomiX creates a unique 
			and interactive gene variants report, which can be explored visually as an 
			overview graph (Figure 1) or by health category. 
			GenomiX report can be used together with a Chrome 
			extension (Figure 2) to collect and store information about your gene variant report.
		</p>
		<br>
		<center>
			<img src='img/overview.png' style=" width: 80%; border: 1px solid #ddd; border-radius: 4px; padding: 5px;">
			<p><b>Figure 1.</b> Overview graph view of example variant report.</p>
			<img src='img/curation_tool.png' style="width: 80%; border: 1px solid #ddd; border-radius: 4px; padding: 5px;">
			<p><b>Figure 2.</b> Curation tool and chrome extension.</p>
		</center>
		<br>
		If you'd like more information about the features of GenomiX before interacting with your own data, you can watch our tutorial
		videos for our <a href='https://www.youtube.com/watch?v=_DlU2h6ODLo' target='_blank'>visualization tool</a> or our <a href='https://www.youtube.com/watch?v=2RmTXyFvyvc' target='_blank'>curation tool and chrome extension</a>.
		<br>
		<br>
		To interact with your personal genomic information using GenomiX, please read and sign the consent form below.
		

		<br><br>
		<center><h2>Consent Form</h2></center>
		<p>Please consider this information carefully before deciding whether to participate in this research.</p>
		<p><b>Purpose of the research:</b> To understand how users of personal genomics engage with and learn from their own personal genomic information.</p>
		<p>To learn more about and contact our primary investigators, go to: <a href='http://cs.wellesley.edu/~hcilab/pghci_pgp'>http://cs.wellesley.edu/~hcilab/pghci_pgp</a></p>
		<p><b>Time required:</b> You are free to use the application as much or as little as you would like. A short questionnaire will be sent out to you periodically over the next couple of months about your experience using the application, each of which should take about 5 minutes to complete.</p>
		<p><b>What you will do in this study:</b> If you decide to participate, you will explore your personal genomics through GenomiX visualization and curation tool, at your own leisure, and respond to short, periodic questionnaires about your experiences with the tool over the next three months. We will collect information about your usage of the tool--including quantity and length of interactions, pages saved with the curation tool, and variants saved within the visualization--along with your huID. This data will saved on a secure server and will only be used in aggregate (added together with the data of other users) to identify trends in usage of this application.</p>
		<p><b>Benefits:</b> You will receive access to a new tool and contribute to a research project with the goal of creating interactive and highly usable tools for non-expert engagement with personal genomics.</p>
		<p><b>Compensation:</b> There is no monetary compensation for this study.</p>
		<p><b>Confidentiality:</b> Your responses to our questionnaires, huID, and information about how and when you use the tool will be recorded. This information will be kept strictly confidential on our secure server. When research results are reported, responses will be aggregated (added together) and described in summary.</p>
		<p><b>Participation and withdrawal:</b> Your participation is completely voluntary, and you may quit at any time without penalty. To quit the study, email <a href='mailto:wellesleyhcilab@gmail.com'>wellesleyhcilab@gmail.com</a> to let the researchers know you’d like to stop. None of your information will be used should you choose to quit and previously recorded information will be removed.</p>
		<p style="border-style: solid; padding: 5px"><b>To Contact the Researcher:</b> If you have any questions or concerns about the study, please email Orit Shaer, Associate Professor, Wellesley College at <a href='mailto:oshaer@wellesley.edu'>oshaer@wellesley.edu</a>. </p>
		<p>If you have questions about your rights in this research, concerns, suggestions, or complaints that are <b>not being addressed by the researcher</b>, or research-related harm:
			<br>Nancy L Marshall, Chair, Wellesley College IRB, Phone: (781)(2832551), 106 Central Street, Wellesley, Massachusetts 02481; email: nmarshall@wellesley.edu.</p>
		<br><p>I have read the description of the study and voluntarily consent to participate. I understand that I may discontinue participation in this study at any time without any penalty and that there are no risks associated with this study. I have been printed or saved a copy of this consent form.</p>
		<br>
		<p>Please sign below if you agree to the above statements:</p>
		<form action='consent_process.php' method='post'>
			Signature: <input type="text" name="sign" required><br>
  			Date: <input type="text" name="date" required><br>
  			Email: <input type="text" name="email" required><br>
  			<input type="submit" value="Consent"><br>
		</form>
	</div>
		
	</body>
</html>