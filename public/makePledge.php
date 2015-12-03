<?php
if (isset($_POST['submit'])) {

    $ids = mysql_real_escape_string($_POST['pledgeid']);
	$isAuthQuery = "SELECT `passkey`,`pledgeid`,`timestamp` FROM `biggreenbuttonlocations` WHERE `pledgeid` = '".$ids."';";
    $isAuth = mysql_query($isAuthQuery);

	if (!$isAuth) {
	    echo "Error: " .mysql_error();
	    exit;
  	}

    $key = mysql_result($isAuth, 0, 'passkey');

	if($_POST['securekey'] != $key) {
		echo "Incorrect Key";
		exit;
	}
    // echo mysql_real_escape_string($_POST['emailadd']);
    $emailAdd = mysql_real_escape_string($_POST['emailadd']);
    $pledge = mysql_real_escape_string($_POST['pledge']);
    $pledgeName = mysql_real_escape_string($_POST['pledgename']);
    $pledgeid = mysql_real_escape_string($_POST['pledgeid']);


	$query = "UPDATE `biggreenbuttonlocations` SET `email`= '".$emailAdd."' ,`pledge`= '".$pledge."' ,`pledgename`= '".$pledgeName."' ,`updated_at`= NOW() WHERE `pledgeid`= '".$pledgeid."'";
	$result = mysql_query($query);
	if (!$result) {
		echo "Error: couldn't execute query. ".mysql_error();
		exit;
	}
    header("location:pledgeSuccessful.php?pledge=".$pledge."&pledgeid=".$pledgeid);
}
?>
