<?php
include('dbconnect.php');
if (isset($_GET['get'])) {

	$query = "SELECT `pledgeid`,`lat`, `lng`, `timestamp`,
				IF(`id` is NULL,'broken',id) as id,
				IF(`pledge` IS NULL,'No Pledge has been Made Yet',pledge) as pledge,
				IF(`updated_at` IS NULL,'No Pledge has been Made Yet',updated_at) as updated_at,
				IF(`pledgename` IS NULL,'No Pledge has been Made Yet',pledgename) as pledgename
				FROM `biggreenbuttonlocations`
				ORDER BY 'timestamp' ASC";

	$get = $DBH->prepare($query);
	$get->execute();

	if (!$get) {
		echo "Error: couldn't execute query. ".$get->errorCode();
		exit;
	}

	if ($get->fetchColumn() == 0) {
		echo '[]';
		exit;
	}

	$rows = array();
	while ($row = $get->fetch(PDO::FETCH_ASSOC)) {
		$rows[] = $row;
	}

	echo json_encode($rows);
}
elseif (isset($_GET['newMarkers'])) {
	$latestId = $_GET['maxID'];
	$lastIDQuery = "SELECT id FROM `biggreenbuttonlocations` ORDER BY id DESC LIMIT 1";
	$isAuth = $DBH->prepare($lastIDQuery);
	$isAuth->execute();

	if (!$isAuth) {
	    echo "Error: ".$get->errorCode();
	    exit;
  	}

	if ($latestId == $isAuth->fetchAll(PDO::FETCH_COLUMN,0)) {
		echo "No new Markers";
		exit;
	}

	$query = "SELECT `pledgeid`,`lat`, `lng`, `timestamp`,
				IF(`id` is NULL,'broken',id) as id,
				IF(`pledge` IS NULL,'No Pledge has been Made Yet',pledge) as pledge,
				IF(`updated_at` IS NULL,'No Pledge has been Made Yet',updated_at) as updated_at,
				IF(`pledgename` IS NULL,'No Pledge has been Made Yet',pledgename) as pledgename
				FROM `biggreenbuttonlocations`
				WHERE `id` > '.$latestId.'
				ORDER BY 'timestamp' ASC";

	$get = $DBH->prepare($query);
	$get->execute();
	if (!$get) {
		echo "Error: couldn't execute query. ".$get->errorCode();
		exit;
	}
	if ($get->fetchColumn() == 0) {
		echo '[]';
		exit;
	}

	$rows = array();
	while ($row = $get->fetch(PDO::FETCH_ASSOC)) {
		$rows[] = $row;
	}
	echo json_encode($rows);
}
?>
