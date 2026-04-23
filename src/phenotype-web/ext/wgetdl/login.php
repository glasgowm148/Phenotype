<!DOCTYPE>
<html>
	<head>

		<title>Visualization: Login</title>

		<!--original css-->
		<link rel="stylesheet" href="css/feb.css">
		<!--font awesome css-->
		<link rel="stylesheet" href="css/font-awesome-4.4.0/css/font-awesome.min.css">
		<!--font-->
		<link href='http://fonts.googleapis.com/css?family=Raleway:500,700,400' rel='stylesheet' type='text/css'>

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

	    <form action="login_process.php" method="post" onsubmit="return clicked()" style="width:75%;padding-top:200px;padding-left:25%">
	    	<h3>Login: PGP User</h3>
	    	<br><b>BEFORE YOU LOG IN:</b> This tool was built to be used in a Chrome browser. If you are using a browser other than Google Chrome (e.g. Safari, Firefox, Internet Explorer), please
	    	 take a moment to <a href='https://www.google.com/chrome/browser/desktop/index.html'>download Google Chrome</a> and return to this webpage using the Chrome browser.
	    	<br>
	    	<br>After logging in, you will be brought to the 'Report' tab of GenomiX, which contains your interactive visualization. <b>Tutorial videos</b> and the <b>link to download the curation tool</b> are located in the 'Instructions' tab on the far right.
	    	<br>
	    	<br><b>If you experience techinical issues:<b> First, try refreshing your page. If this doesn't resolve the issue, please do not hesitate to email lwestend@wellesley.edu and our techinical support will respond as quickly as possible.
	    	<br>
	    	<br>To continue to the visualization and curation tool, please enter your huID: 
			<br><input type="text" name="huID" id="huID" style="height:20px" required>
			<br>
			<br><b>How to find huID: </b>Your huID is visible in the top right of your account when you’re logged in to my.pgp-hms.org.
			<br>
			<br>Entering your huID will allow us to generate an interactive visualization of your current genome data 
			<br>that you publicly share in your PGP profile. 
			<br>
			<br>
			<br><input type="text" name="login" id="login" style="display:none" value="pgp">
			<input class="btn btn-primary submit-study" type="submit" value="Continue"> 

			<br>
			<br>
			<!-- Not a PGP user? <a href='open_login.php'>Click Here</a> -->

			<script type="text/javascript">
    		function clicked() {
    			var path = "http://cs.wellesley.edu/~hcilab/pghci_pgp/data/csv_genome_reports/";
        		var huid = document.getElementById('huID');
        		var url = path.concat(huid.value,".csv");

        		var request;
					if(window.XMLHttpRequest) {
					    request = new XMLHttpRequest();
					} else {
					    request = new ActiveXObject("Microsoft.XMLHTTP");
					}
					request.open('GET', url, false);
					request.send();
					if (request.status === 404) {
					    alert("We cannot locate the genome report for the huID provided. Please verify that your huID input is correct (it's case-sensitive!). If you are confident your huID is correct and you are still receiving this message, please email lwestend@wellesley.edu.");
					    return false;
					} else {
						return true;
					}
	    		}
			</script>
	    </form>

	</body>
</html>

