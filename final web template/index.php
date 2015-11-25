<html>
    <head>
    <title>Web Server Template Application</title>
        <?php include 'head.php' ?>
    </head>
<body>

<?php

echo "Start of page to validate";

session_start();

if (!(isset($_SESSION['login']) && $_SESSION['login'] != '')) {
        header ("Location: login.php");
}

echo "back to validated window";
?>

    <div class="container-fluid">
        <h1>RPiSecCam by Andy Lincoln</h1>
    </div>

</body>
</html>
