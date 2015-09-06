<?php
    $secret = "sd2ela5234kn7312din";


    if (isset($_POST['submit'])){

        if (!isset($_POST['secretkey']) || $_POST['secretkey'] != $secret) {
        	echo "The Secret Key Is Incorrect";
        	exit;
        }
        $projectorstatus = "";

        echo "<br>";
        if (!isset($_POST['locationid']) || $_POST['locationid'] == 0) {
            echo "This form has no Location ID";
            echo "<br />";
            exit;
        }

        if (!isset($_POST['activations']) || $_POST['activations'] == 0) {
            echo "No People Field";
            echo "<br>";
            exit;
        }

        if (!isset($_POST['projectorstatus']) || $_POST['projectorstatus'] == 0) {
            echo " No Projector Status ";
            $projectorstatus = "Missing";
        }
        else {
            $projectorstatus = $_POST['projectorstatus'];
        }

        // $elements = array("LocationID: ".$_POST['locationid'],"Activations: ".$_POST['activations'],"Projector Status: ".$_POST['locationid']);
        echo "LocationID: ".$_POST['locationid'];
        // echo "<br>";
        echo " Activations: ".$_POST['activations'];
        // echo "<br>";
        echo " Projector Status: ".$_POST['locationid'];
        // print_r($elements);
    }
?>
