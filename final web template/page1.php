<?PHP
session_start();
if (!(isset($_SESSION['login']) && $_SESSION['login'] != '')) {
        header ("Location: login3.php");
}
?>

	<html>
	<head>
	<title>IOT Device Management Interface</title>
    <?php  include  'head.php';
      head();
    ?>
	</head>
	<body>
        <div class="container">
            <div class="container">
	            <h1>User Logged in</h1>

                <?PHP   print ("<p>Add your device management code here</p>");
                print ("<p>I recommend a combination of PHP and python scripts</p>");?>
                 <a href="page2.php" class="btn btn-primary">Log out</a>
            </div>
        </div>




	</body>
	</html>
