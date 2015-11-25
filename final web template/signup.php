<?php require 'db.php'?>
<html>
<head>
<title>RPiSecCam - Signup</title>
    <?php include 'head.php'?>
</head>
<body>
    <?php echo $uname; echo $pword; ?>
    <div class="container-fluid text-center">
        <h1>Raspberry Security</h1>
        <h2>Andy Lincoln</h2>
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">Sign Up</h3>
            </div>
            <div class="panel-body">
                <form class="form-vertical" name ="form1" method ="POST" action="signup.php">
                    <div class="form-group">
                        <input type="text"  class="form-control" name="username"  value="" maxlength="20" placeholder="username">
                        <input type="email" class="form-control" name="email"  value="" maxlength="40" placeholder="email">
                        <input type="password" class="form-control" name="password"  value="" maxlength="16" placeholder="password">
                        <input type="password" class="form-control" name="confirm password" value="" maxlength="16" placeholder="confirm password">
                        <input type="tel" class="form-control" name="phone number" value="" maxlength="12" placeholder="+18005554455"/>
                        <input class="btn btn-primary" type="Submit" name = "Submit1"  value = "Login"/>
                    </div>
                </form>
            </div>
        <?PHP print $errorMessage;?>
    </div>

</body>
</html>
