<!DOCTYPE>
<html>
	<head>

		<title>GenomiX: Login</title>

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
	            <span class="brand"><img src="assets/img/dna.png"> Genomix: Genome Curation Tool</span>
	          </div>
	        </div>
	      </div>
	    </header>

	    <form action="login_process.php" method="post" onsubmit="return clicked()" style="width:75%;padding-top:200px;padding-left:25%">
	    	<h3>Login: Non-PGP User</h3>
	    	<br>To continue to the curation tool, please enter your open human ID: 
			<br><input type="text" name="huID" id="huID" style="height:20px" required>
			<br>
			<br>
			<br><input type="text" name="login" id="login" style="display:none" value="open">
			<input class="btn btn-primary submit-study" type="submit" value="Continue"> 

			<br>
			<br>
			Are you a PGP user? <a href='login.php'>Click Here</a>

	    </form>

	</body>
</html>

