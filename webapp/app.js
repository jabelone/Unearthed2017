var __json = "data/live.json";
var app = require('http').createServer(function(req, res) {

fs.readFile(req.url.substring(1),
	function (err, data) {
		if (err) {
			console.error(req.url);
			res.writeHead(500);
  			return res.end('Error loading index.html');
		}
		res.writeHead(200);
		res.end(data);
	});
});

var io = require("socket.io")(app);
var fs = require("fs");


app.listen(8000);


io.on('connection', function(s) {

	fs.readFile(__json,'utf8', function(e,d) {
		s.emit('jsonDoc', d);
	});

	fs.watch(__json, {'persistant': true} ,function() {
		fs.readFile(__json,'utf8', function(e,d) {
			s.emit('jsonDoc', d);
		});
	})
})
