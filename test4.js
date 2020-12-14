  var socket = io('http://127.0.0.1:5000/test1');
	const canvas = document.getElementById("canvasOutput");
	const context = canvas.getContext("2d")

    socket.on('connect', function(){
        console.log("Connected...!", socket.connected)
    });

    const video = document.querySelector("#videoElement");

    video.width = 500; 
    video.height = 375; ;

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function (err0r) {
            console.log(err0r)
            console.log("Something went wrong!");
        });
    }
	
    const FPS = 22;

   let timerId =  setInterval(() => {
		context.drawImage(video,0,0,canvas.width, canvas.height);
		data = canvas.toDataURL("image/png")
		socket.emit('image', data);
    }, 10000/FPS);
setTimeout(() => { clearInterval(timerId)}, 5000);


    socket.on('response_back', function(image){
        const image_id = document.getElementById('image');
        image_id.src = image;
    });