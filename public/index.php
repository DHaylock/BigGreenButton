<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta charset="utf-8">
    <title>Big Green Button</title>
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="./js/bootstrap/js/bootstrap.js"></script>
    <link rel="stylesheet" type="text/css" href="./js/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="stylesheet.css">
    <script src="OpenLayers.js"></script>
    <link rel="stylesheet" href="js/leaflet/leaflet.css" />
    <script src="js/leaflet/leaflet.js"></script>
    <script type="text/javascript" src="http://maplib.khtml.org/khtml.maplib/khtml_all.js"> </script>
    <script src="http://maximeh.github.io/leaflet.bouncemarker/bouncemarker.js"></script>
    <link rel="stylesheet" href="./js/Leaflet.markercluster/dist/MarkerCluster.css" />
	<link rel="stylesheet" href="./js/Leaflet.markercluster/dist/MarkerCluster.Default.css" />
	<script src="./js/Leaflet.markercluster/dist/leaflet.markercluster-src.js"></script>
    <script src="main.js"></script>
    <script type="text/javascript">
        <?php $id = json_encode($_GET['pledgeid']);?>
        var id = <?php echo $id;?>;
        if(id != null){
            setTimeout(function() { findPledgeReturn(id); },2000);
        }
    </script>
</head>
<body>
    <div style="">
    	<div class="row">
    		<div style="margin-bottom:0px;" class="navbar navbar-inverse navbar-static-top" role="navigation">
		    	<div class="col-sm-12">
                    <a style="margin-left:5px;" class="navbar-brand" data-toggle="modal" data-target=".bs-example-modal-lg" class="navbar-brand">
                        <span data-toggle="modal" data-target=".bs-example-modal-lg">Big Green Button</span>
                    </a>
                    <div class="navbar-form">
                        <div class="col-sm-6 input-group">
                            <input id="get" type="text" class="form-control">
                            <div class="input-group-btn">
                                <button type="button" onclick="findPledge()" class="btn btn-success"
                                tabindex="-1">
                                    <span class="glyphicon glyphicon-search"></span>
                                </button>
                                <button id="edit" type="button" style="visibility:hidden; opacity:0;" class="btn btn-primary" data-toggle="modal" data-target="#myModal" tabindex="-1">Edit Pledge</button>
                            </div>
                        </div>
                    </div>
                </div>
	        </div>
        </div>
    </div>
    <div id="pledgemap"></div>
    <nav id="alertBar" style="opacity:0; margin-bottom:0px" class="navbar navbar-fixed-bottom navbar-inverse" role="navigation">
        <div class="container-fluid">
            <div class="col-lg-4">
                <div class="navbar-header">
                    <h5 class="navbar-brand">A New Pledge Has Just Been Made</h5>
                </div>
            </div>
        </div>
    </nav>
    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" id="pledgeLabel"></h4>
                </div>
                <div class="modal-body">
                    <form role="form" action="makePledge.php" method="post" class="form-horizontal">
                        <div class="form-group">
                            <label class="col-sm-2 control-label" for="name">Name:</label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" id="name" name="pledgename">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-sm-2 control-label" for="pass">Password:</label>
                            <div class="col-sm-8">
                                <input type="password" class="form-control" id="pass" name="securekey">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-sm-2 control-label" for="email">Email:</label>
                            <div class="col-sm-8">
                                <input type="email" class="form-control" id="email" name="emailadd">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-sm-2 control-label" for="pledge">Pledge:</label>
                            <div class="col-sm-8">
                                <textarea class="form-control" id="pledge" name="pledge" rows="3"></textarea>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <input id="pledgeid" type="hidden" name="pledgeid" value="">
                            <input type="submit" name="submit" class="btn btn-primary btn-lg">
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    </div>
    </div>
    </div>
    <div class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Infomation</h3>
                </div>
                <div class="modal-body">
                    <p>This Contains data about the scheme/the button.</p>
                    <p>Built by
                        <strong>David Haylock</strong> and
                        <strong>Chloe Mennick</strong>
                    </p>
                    <div align='center'>
                        <img alt="Brand" src="./assets/logo.jpg">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
