         // Connect to PeerJS, have server assign an ID instead of providing one
         // Showing off some of the configs available with PeerJS :).
        var peer = new Peer({
            // Set API key for cloud server (you don't need this if you're running your
            // own.
            key: 'lwjd5qra8257b9',
            // Set highest debug level (log everything!).
            debug: 3,
            // Set a logging function:
            logFunction: function() {
                var copy = Array.prototype.slice.call(arguments).join(' ');
                $('.log').append(copy + '<br>');
            },
            // Use a TURN server for more network support
            config: {
                'iceServers': [{
                    url: 'stun:stun.l.google.com:19302'
                }]
            } /* Sample servers, please use appropriate ones */
        });
        var connectedPeers = {};
         // Show this peer's ID.
        peer.on('open', function(id) {
            $('#pid').text(id);
        });
         // Await connections from others
        peer.on('connection', connect);
         // Handle a connection object.

        function connect(c) {
            // Handle a chat connection.
            if (c.label === 'chat') {
                var chatbox = $('<div></div>').addClass('connection').addClass('active').attr('id', c.peer);
                var header = $('<h1></h1>').html('Chat with <strong>' + c.peer + '</strong>');
                var messages = $('<div><em>Peer connected.</em></div>').addClass('messages');
                chatbox.append(header);
                chatbox.append(messages);
                // Select connection handler.
                chatbox.on('click', function() {
                    if ($(this).attr('class').indexOf('active') === -1) {
                        $(this).addClass('active');
                    } else {
                        $(this).removeClass('active');
                    }
                });
                $('.filler').hide();
                $('#connections').append(chatbox);
                c.on('data', function(data) {
                    messages.append('<div><span class="peer">' + c.peer + '</span>: ' + data +
                        '</div>');
                });
                c.on('close', function() {
                    alert(c.peer + ' has left the chat.');
                    chatbox.remove();
                    if ($('.connection').length === 0) {
                        $('.filler').show();
                    }
                    delete connectedPeers[c.peer];
                });
            } else if (c.label === 'file') {
                c.on('data', function(data) {
                    // If we're getting a file, create a URL for it.
                    if (data.constructor === ArrayBuffer) {
                        var dataView = new Uint8Array(data);
                        var dataBlob = new Blob([dataView]);
                        var url = window.URL.createObjectURL(dataBlob);
                        $('#' + c.peer).find('.messages').append('<div><span class="file">' +
                            c.peer + ' has sent you a <a target="_blank" href="' + url + '">file</a>.</span></div>');
                    }
                });
            }
        }
