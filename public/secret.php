<?php
    $secret = "";
    if (!isset($_POST['secretkey']) || $_POST['secretkey'] != $secret) {
        header('HTTP/1.0 403 Forbidden');
        exit;
    }
    ?>
