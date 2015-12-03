<?php
    @$db = mysql_connect('localhost', 'dbname', 'dbpassword');
    if (!$db)
    {
        echo "Error: no database connection";
        exit;
    }
    if (!mysql_select_db('dbname'))
    {
        echo "Error: no database selected";
        exit;
    }
    ?>
