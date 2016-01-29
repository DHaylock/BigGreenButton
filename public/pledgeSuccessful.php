<!DOCTYPE html>
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="./js/bootstrap/js/bootstrap.js"></script>
    <script src="./js/progressbar.js"></script>
    <link rel="stylesheet" type="text/css" href="./js/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="stylesheet.css">

    <script type="text/javascript">

        <?php
            $pledge = explode("=",parse_url($_SERVER['REQUEST_URI'], PHP_URL_QUERY));
            $pledgeData = urldecode($pledge[1]);
            $pledgeId = urldecode($pledge[2]);
        ?>

        function timer(callback, delay) {
            var id, started, remaining = delay, running

            this.start = function() {
                running = true
                started = new Date()
                id = setTimeout(callback, remaining)
            }

            this.pause = function() {
                running = false
                clearTimeout(id)
                remaining -= new Date() - started
            }

            this.getTimeLeft = function() {
                if (running) {
                    this.pause()
                    this.start()
                }
                return remaining/1000
            }

            this.getStateRunning = function() {
                return running
            }

            this.start()
        }
        var a = new timer(function() {
            window.location.href= 'http://button.do15.co.uk/index.php?pledgeid='+<?php echo json_encode($pledgeId); ?>;
        }, 5000);

        setInterval(function() {
            if (a.getTimeLeft() < 1) {
                document.getElementById('messages').innerHTML = "Hold on!";
            }
            else if (a.getTimeLeft() < 2 && a.getTimeLeft() > 1) {
                document.getElementById('messages').innerHTML = "Updating Map!";
            }
            else if (a.getTimeLeft() < 3 && a.getTimeLeft() > 2) {
                document.getElementById('messages').innerHTML = "Generating New Marker!";
            }
        },500);

    </script>
</head>
<body>
<div align='center'>
    <h2>Congratulations</h2>
    <h4>You have just pledged</h4>
    <br/>
    <h4><?php echo $pledgeData;?></h4>
    <div style="width:400px; height:400px;" id="progress"></div>
    <h4 id="messages">Updating ...</h4>

    <script>
    var startColor = '#A1D490';
    var endColor = '#12B300';
        var circle = new ProgressBar.Circle('#progress', {
            color: startColor,
            strokeWidth: 5,
            trailWidth: 1,
            duration: 5000,
            easing:'easeInOut',
            text: {
                value: '0%'
            },
            step: function(state,circle) {
                circle.setText((circle.value() * 100).toFixed(0)+'%');
                circle.path.setAttribute('stroke', state.color);
            }
        });

        circle.animate(1, {
            from: {color: startColor},
            to: {color: endColor}
        })
    </script>
    <!---<img style="width:200px; height:200px;"alt="Brand" src="./assets/logo.jpg">--->
</div>
</html>
