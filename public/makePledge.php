<?php

@$db = mysql_connect('localhost', 'root', 'root');
if (!$db) {
	echo "Error: no database connection";
	exit;
}
if (!mysql_select_db('BristolBigGreenButton')) {
	echo "Error: no database selected";
	exit;
}

if (isset($_POST['submit'])) {

	$isAuthQuery = "SELECT `passkey`,`pledgeid`,`timestamp` FROM `locations` WHERE `pledgeid`=|;
	$isAuth = mysql_query($isAuthQuery);

	if (!$isAuth) {
	    echo "Error: ".mysql_error();
	    exit;
  	}

	if($_POST['securekey'] != mysql_result($isAuth, 0)) {
		echo "Incorrect Key";
		exit;
	}

	$query = "UPDATE `locations` SET `pledge`='".mysql_real_escape_string($_POST['pledge'])."',`pledgename`='".mysql_real_escape_string($_POST['pledgename'])."',`updated_at`=NOW() WHERE `pledgeid`='".mysql_real_escape_string($_POST['pledgeid'])."'";

	$result = mysql_query($query);
	if (!$result) {
		echo "Error: couldn't execute query. ".mysql_error();
		exit;
	}

	// if (isset(mysql_real_escape_string($_POST['emailaddress'])) && !empty(mysql_real_escape_string($_POST['emailaddress']))) {
	// 	$to      = mysql_real_escape_string($_POST['emailaddress']);
	// 	$subject = 'Your Pledge';
	// 	$message = 'You have pledged to '.mysql_real_escape_string($_POST['pledge']);
	// 	mail($to, $subject, $message);
	// }
}
?>
