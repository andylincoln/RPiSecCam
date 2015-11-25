<?php require 'db.php'?>
<html>
<head>
<title>Basic Login Script</title>
    <?php include 'head.php'?>
</head>
<body>
    <?php echo $uname; echo $pword; ?>
    <div class="container-fluid text-center">
        <h1>Raspberry Security</h1>
        <h2>Andy Lincoln</h2>
        <a href="signup.php">Sign Up</a>
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">Log in</h3>
            </div>
            <div class="panel-body">
                <div class="form-group">
                    <form class="form" name ="form1" method ="POST" action="login.php">
                        <input class="form-control" type='text' name ='username'  value="<?PHP print $uname;?>" maxlength="20" placeholder="username">
                        <input class="form-control" type='password' name ='password'  value="<?PHP print $pword;?>" maxlength="16" placeholder="password">
                        <input class="btn btn-primary" type="Submit" name="Submit1"  value="Login"/>
                    </form>
                </div>
            </div>
        <?PHP print $errorMessage;?>
    </div>

</body>
</html>
