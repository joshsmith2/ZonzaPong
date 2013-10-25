$(function () {
    var canvasInput = $('#webcam .inputCanvas');
    var videoInput = $('#webcam .inputVideo')[0];
    var output = $('#webcam .outputCanvas')[0].getContext('2d');
    var h_width = canvasInput.width() / 2;
    var h_height = canvasInput.height() / 2;

    var htracker = new headtrackr.Tracker();
    htracker.init(videoInput, canvasInput[0]);
    htracker.start();

    function trackFace(event) {
        var x = -((event.x - h_width) / h_width); // x == -0.1 -> 1.0

        // Draw webcam image
        output.drawImage(videoInput, 0, 0, h_width*2, h_height*2);

        // once we have stable tracking, draw rectangle
        output.save();
        // Draw small rect on the middle of the face
        output.translate(event.x, event.y);
        output.rotate(event.angle - Math.PI/2);
        output.strokeStyle	= '#00CC00';
        output.strokeRect(-Math.floor(10/2), -Math.floor(10/2), 10, 10);

        output.restore();

        window.face = x;
    }

    $(document).bind('facetrackingEvent', function(e) {
        trackFace(e.originalEvent)
    });

    $('#webcam .sens').bind('change', function (e) {
        window.sensitivity = 1.5 + $(this).val()/10*6;
    }).trigger('change');
});
