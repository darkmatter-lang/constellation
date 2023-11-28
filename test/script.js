
const State = {
	DISCONNECTED: 0,
	CONNECTING: 1,
	CONNECTED: 2,
}

const Element = {
	CANVAS: "canvas"
}

document.addEventListener("DOMContentLoaded", function() {
	const canvas = document.getElementById(Element.CANVAS);
	redrawCanvas(canvas);

	var ws = null;
	var state = State.DISCONNECTED;
	
	function log(msg, sender="console") {
		var date = new Date();
		var unixTime = date.getTime() / 1000;
		var datestamp = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
		var hours = (date.getHours() <= 9) ? "0" + date.getHours() : date.getHours();
		var minutes = (date.getMinutes() <= 9) ? "0" + date.getMinutes() : date.getMinutes();
		var seconds = (date.getSeconds() <= 9) ? "0" + date.getSeconds() : date.getSeconds();
		var timestamp = `${hours}:${minutes}:${seconds}`;
	
		$("#log").append(`
			<div class="log-entry">
				<span class="log-entry-timestamp">
					<time datetime="${datestamp} ${timestamp}" data-unixtime="${unixTime}" title="${datestamp} ${timestamp}">${timestamp}</time>
				</span>
				<span class="log-entry-sender log-entry-sender-${sender.toLowerCase()}">[${sender}]</span>
				<span class="log-entry-message">${msg}</span>
			</div>
		`);
	
		console.log(`[${sender}]`, msg);
	}





	// Event functions

	function onOpen(evt) {
		state = State.CONNECTED;
		log(`Successfully connected.`, "WebSocket");
		$("#connect").removeClass("is-warning");
		$("#connect").addClass("is-danger");
		$("#connect").attr("value", "Disconnect");
		$("#connect").prop("disabled", false);
	}

	function onClose(evt) {
		const code = evt.code;
		const reason = evt.reason;
		const wasClean = evt.wasClean;
		log(`Connection closed: ${code} ${reason}`, "WebSocket");
		disconnect();
	}

	function onError(evt) {
		log(`Error: ${evt.toString()}`, "WebSocket", true);
		console.error(evt);
	}

	function onMessage(evt) {
		const msg = evt.data;
	}







	// Client functions

	function connect(wsUrl) {
		log(`Connecting to ${wsUrl} ...`);
		$("#host").prop("disabled", true);
		$("#connect").prop("disabled", true);
		$("#connect").removeClass("is-success");
		$("#connect").addClass("is-warning");
		$("#connect").attr("value", "Connecting");

		ws = new WebSocket(wsUrl, []);

		ws.onopen = onOpen;
		ws.onerror = onError;
		ws.onmessage = onMessage;
		ws.onclose = onClose;
	}

	function disconnect() {
		state = State.DISCONNECTED;
		log(`Disconnected`);
		$("#connect").removeClass("is-danger");
		$("#connect").removeClass("is-warning");
		$("#connect").addClass("is-success");
		$("#connect").attr("value", "Connect");
		$("#connect").prop("disabled", false);
		$("#host").prop("disabled", false);
	}









	// Canvas functions

	function redrawCanvas() {
		var canvas = document.getElementById(Element.CANVAS);
		//var ctx = canvas.getContext("2d");
		//ctx.imageSmoothingEnabled = false;

		// Make it visually fill the positioned parent
		canvas.style.width = '100%';
		canvas.style.height = '100%';

		// ...then set the internal size to match
		canvas.width  = canvas.offsetWidth;
		canvas.height = canvas.offsetHeight;

		// read current image data?
		// write image data?
	}

	function clearCanvas() {
		var canvas = document.getElementById(Element.CANVAS);
		var ctx = canvas.getContext("2d");
		ctx.clearRect(0, 0, canvas.width, canvas.height);
	}

	function randomCanvas(bw) {
		var canvas = document.getElementById(Element.CANVAS);
		var ctx = canvas.getContext("2d");
		var id = ctx.getImageData(0, 0, canvas.width, canvas.height);
		var pixels = id.data;
		
		for (var w = 0; w < canvas.width; w++) {
			for (var h = 0; h < canvas.height; h++) {
				var x = w;
				var y = h;
				var r = Math.floor(Math.random() * 256);
				var g = Math.floor(Math.random() * 256);
				var b = Math.floor(Math.random() * 256);
				var off = (y * id.width + x) * 4;
	
				if (bw) {
					g = r;
					b = r;
				}
	
				pixels[off] = r;
				pixels[off + 1] = g;
				pixels[off + 2] = b;
				pixels[off + 3] = 255;
			}
		}

		ctx.putImageData(id, 0, 0);
	}










	// Console Buttons

	$("#clear-console").click(() => {
		$("#log").html("");
	});

	$("#print-active-stars").click(() => {
		
	});

	// Canvas Buttons

	$("#clear-canvas").click(() => {
		log("Cleared canvas");
		clearCanvas();
	});

	$("#fill-canvas-rgb").click(() => {
		log("Filled canvas with random RGB pixels");
		randomCanvas(false);
	});

	$("#fill-canvas-bw").click(() => {
		log("Filled canvas with random monochrome pixels");
		randomCanvas(true);
	});

	$("#redraw-canvas").click(() => {
		redrawCanvas();
	});














	$("#connect").click(() => {

		if (state == State.DISCONNECTED) {
			connect($("#host").val());
		} else {
			ws.close();
		}
		
		state = State.CONNECTING;
	});




});
