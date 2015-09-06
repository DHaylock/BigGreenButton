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

$secretUploadKey = "jkqcu309qivdkmv";

if(isset($_POST['pledge']) && ($_POST['pledge'] == '1')) {
	if(!isset($_POST['secret'])) {
		echo "No Secret Key Attached ... Stranger Danger";
		http_response_code(404);
		exit;
	}

	if($_POST['secret'] != $secretUploadKey){
		echo "Invalid Secret";
		http_response_code(404);
		exit;
	}

	if (!isset($_POST['lat']) || !isset($_POST['lng'])) {
		echo "Error: lat and/or lng not specified";
		http_response_code(404);
		exit;
	}


	$query = "INSERT INTO `locations` SET pledgeid='".mysql_real_escape_string($_POST['pledgeid'])."',lat='".mysql_real_escape_string($_POST['lat'])."',lng='".mysql_real_escape_string($_POST['lng'])."',passkey='".mysql_real_escape_string($_POST['passkey'])."'";
	$result = mysql_query($query);
	if (!$result) {
		echo "Error: couldn't execute query. ".mysql_error();
		exit;
	}
	echo "Sucess";
}
?>
