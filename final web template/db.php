<?PHP


//==========================================
//	ESCAPE DANGEROUS SQL CHARACTERS
//==========================================
function quote_smart($value, $handle) {

   if (get_magic_quotes_gpc()) {
       $value = stripslashes($value);
   }

   if (!is_numeric($value)) {
       $value = "'" . mysql_real_escape_string($value, $handle) . "'";
   }
   return $value;
}



   if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    $uname = $_POST['username'];
	$pword = $_POST['password'];
    $confirmpword = $_POST['confirm password'];
    $email = $_POST['email'];
    $tel = $_POST['phone number'];

    $sign_up_check = isset($uname) && isset($pword) && isset($confirmpword) && isset($email) && isset($tel) && (
    md5($pword) == md5($confirmpword));
    echo $sign_up_check;

	$uname          = htmlspecialchars($uname);
	$pword          = htmlspecialchars($pword);
    $confirmpword   = htmlspecialchars($confirmpword);
    $email          = htmlspecialchars($email);
    $tel            = htmlspecialchars($tel);

	//==========================================
	//	CONNECT TO THE LOCAL DATABASE
	//==========================================
	$user_name = "root";
	$pass_word = "";
	$database = "iotdevdb";
	$server = "127.0.0.1";

        $db_handle = mysql_connect($server, $user_name, $pass_word);
        $db_found = mysql_select_db($database, $db_handle);

//        print "DB Read Operation";
        if ($db_found) {
            echo "$uname:$pword:";
            $epw = md5($pword);

            $uname = quote_smart($uname, $db_handle);
            $pword = quote_smart($pword, $db_handle);

            echo ":$uname:$pword:";

            $SQL = "SELECT * FROM login WHERE (L1 = $uname AND L2 = '$epw')";
/            $SQL = "SELECT * FROM login WHERE L2 = '$epw'";
//            $SQL = "SELECT * FROM login WHERE L1 = $uname";
            echo "$SQL";


            if ($sign_up_check) {
               $SQL = "INSERT INTO login (L1, L2, email, phone_number) VALUES ($uname,$pword,$email,$tel)";
               $result = mysql_query($SQL);
               $num_rows = mysql_num_rows($result);
               echo "SIGNING UP";
            } else {
                $result = mysql_query($SQL);
                $num_rows = mysql_num_rows($result);
            }
    	    //====================================================
    	    //	CHECK TO SEE IF THE $result VARIABLE IS TRUE
    	    //====================================================
            echo "- $num_rows -";
		    if ($num_rows) {
	 	        session_start();
		        $_SESSION['login'] = "1";
		        header ("Location: page1.php");
            } else {
			    $errorMessage = "Error logging on";
		    }

	        mysql_close($db_handle);

        }
    }



?>
