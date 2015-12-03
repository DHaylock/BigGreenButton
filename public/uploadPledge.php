<?php
include('dbconnect.php');
if(isset($_POST['pledge']) && ($_POST['pledge'] == '1')) {
    if(!isset($_POST['secretkey'])) {
        echo "No Secret Key Attached ...";
        http_response_code(404);
        exit;
    }

    include('secret.php');

    if (!isset($_POST['lat']) || !isset($_POST['lng'])) {
        echo "Error: lat and/or lng not specified";
        http_response_code(404);
        exit;
    }

    $query = "INSERT INTO `biggreenbuttonlocations` SET pledgeid='".mysql_real_escape_string($_POST['pledgeid'])."',movegps='".mysql_real_escape_string($_POST['havegps'])."',lat='".mysql_real_escape_string($_POST['lat'])."',lng='".mysql_real_escape_string($_POST['lng'])."',passkey='".mysql_real_escape_string($_POST['passkey'])."' , timestamp='".mysql_real_escape_string($_POST['created_at'])."'";
    $result = mysql_query($query);
    if (!$result) {
        echo "Error: couldn't execute query. ".mysql_error();
        exit;
    }
    echo "Success";
}
?>
