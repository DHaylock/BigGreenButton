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

if (isset($_GET['get'])) {

	$query = "SELECT `pledgeid`,`lat`, `lng`, `timestamp`,
				IF(`id` is NULL,'broken',id) as id,
				IF(`pledge` IS NULL,'No Pledge has been Made Yet',pledge) as pledge,
				IF(`updated_at` IS NULL,'No Pledge has been Made Yet',updated_at) as updated_at,
				IF(`pledgename` IS NULL,'No Pledge has been Made Yet',pledgename) as pledgename
				FROM `locations`
				ORDER BY 'timestamp' ASC";

	$result = mysql_query($query);
	if (!$result) {
		echo "Error: couldn't execute query. ".mysql_error();
		exit;
	}
	if (mysql_num_rows($result) == 0) {
		echo "[]";
		exit;
	}
	$rows = array();
	while ($row = mysql_fetch_assoc($result)) {
		$rows[] = $row;
	}
	echo json_encode($rows);
}
elseif (isset($_GET['newMarkers'])) {


	$latestId = $_GET['maxID'];
	$lastIDQuery = "SELECT id FROM locations ORDER BY id DESC LIMIT 1";
	$isAuth = mysql_query($lastIDQuery);
	if (!$isAuth) {
	    echo "Error: ".mysql_error();
	    exit;
  	}

	if ($latestId == mysql_result($isAuth, 0))
	{
		echo "No new Markers";
		exit;
	}
	// echo "New Markers";
	// if (mysql_result($isAuth, 0)) <= $latestId) {
	// 	exit;
	// }

	// echo $stuff;

	$query = "SELECT `pledgeid`,`lat`, `lng`, `timestamp`,
				IF(`id` is NULL,'broken',id) as id,
				IF(`pledge` IS NULL,'No Pledge has been Made Yet',pledge) as pledge,
				IF(`updated_at` IS NULL,'No Pledge has been Made Yet',updated_at) as updated_at,
				IF(`pledgename` IS NULL,'No Pledge has been Made Yet',pledgename) as pledgename
				FROM `locations`
				WHERE `id` > '.$latestId.'
				ORDER BY 'timestamp' ASC";

	$result = mysql_query($query);
	if (!$result) {
	echo "Error: couldn't execute query. ".mysql_error();
		exit;
	}
	if (mysql_num_rows($result) == 0) {
		echo "[]";
		exit;
	}
	$rows = array();
	while ($row = mysql_fetch_assoc($result)) {
		$rows[] = $row;
	}
	echo json_encode($rows);
}

?>
