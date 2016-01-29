<?php
include('dbconnect.php');
if (isset($_POST['submit'])) {


    $ids = $_POST['pledgeid'];
	$isAuthQuery = "SELECT `passkey`,`pledgeid`,`timestamp` FROM `biggreenbuttonlocations` WHERE `pledgeid` = '".$ids."';";
    $isAuth = $DBH->prepare($isAuthQuery);
    $isAuth->execute();

    if (!$isAuth) {
	    echo "Error: " .$isAuth->errorCode();
	    exit;
  	}
    $key = "";
    while ($row = $isAuth->fetch(PDO::FETCH_ASSOC)) {
           $key = $row['passkey'];
    }

	if($_POST['securekey'] != $key) {
		echo "Incorrect Key";
		exit;
	}

    $emailAdd = $_POST['emailadd'];
    $pledge = $_POST['pledge'];
    $pledgeName = $_POST['pledgename'];
    $pledgeid = $_POST['pledgeid'];

	$query = "UPDATE `biggreenbuttonlocations` SET `email`= '".$emailAdd."' ,`pledge`= '".$pledge."' ,`pledgename`= '".$pledgeName."' ,`updated_at`= NOW() WHERE `pledgeid`= '".$pledgeid."'";
    $update = $DBH->prepare($query);
    $update->execute();

	if (!$update) {
		echo "Error: couldn't execute query. ".$update->errorCode();
		exit;
	}
    header("location:pledgeSuccessful.php?pledge=".$pledge."&pledgeid=".$pledgeid);
}
?>
