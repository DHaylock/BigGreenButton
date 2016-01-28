<?php

include('dbconnect.php');

if (ini_get('magic_quotes_gpc')) {
	foreach ($_GET as $k => $v) {
		$_GET[$k] = stripslashes($v);
	}
	foreach ($_POST as $k => $v) {
		$_POST[$k] = stripslashes($v);
	}
}
//
function sanitise_filename($filename) {
	return basename(preg_replace("/[^0-9a-z._-]/i", "", $filename));
}

if(isset($_POST['pledge']) && ($_POST['pledge'] == '1')) {
    require_once('secret.php');

    if (!isset($_POST['lat']) || !isset($_POST['lng'])) {
        echo "Error: lat and/or lng not specified";
        http_response_code(404);
        exit;
    }
    
    $lat = $_POST['lat'];
	$lng = $_POST['lng'];
	$pledgeid = $_POST['pledgeid'];
	$havegps = $_POST['havegps'];
	$passkey = $_POST['passkey'];
	$createdat = $_POST['created_at'];
    
	$pdostatement = "INSERT INTO `biggreenbuttonlocations` (`lat`,`lng`,`pledgeid`,`havegps`,`passkey`,`timestamp`) VALUES(:lat,:lng,:pledgeid,:havegps,:passkey,:timestamp)";
	$q = $DBH->prepare($pdostatement);	
	$q->execute(array(':lat' => $lat,':lng' => $lng,':pledgeid' => $pledgeid,':havegps' => $havegps,':passkey' => $passkey,':timestamp' => $createdat));

	// Error Handling
	if (!$q) {
		echo "Error: can't insert into database. ".$q->errorCode();
		exit;
	}
	else {
		echo "Success";
		exit;
	}
}
?>
