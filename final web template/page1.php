<?php
    session_start();
    if (!(isset($_SESSION['login']) && $_SESSION['login'] != '')) {
        header ("Location: login.php");
    }
?>
<html>
    <head>
	    <title>IOT Device Management Interface</title>
        <?php  include  'head.php'; ?>
	</head>
	<body>
        <div class="container-fluid">
            <div class="col-lg-12 col-md-12 col-sm-12">
	            <h1>User Logged in</h1>
                 <a href="page2.php" class="btn btn-primary">Log out</a>
            </div>
        </div>




	</body>
</html>
