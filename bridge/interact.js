var BUFFER = ""
const reader = new FileReader()
reader.addEventListener('loadend', (e) => {
	const text = e.srcElement.result;
	BUFFER += text + "\n"
});


SECRET = "super!!secure--"

sock = new WebSocket("ws://noot.lol:5051", [])
sock.onmessage = function (event) {
	reader.readAsText(event.data);
}


String.prototype.replaceAll = function(search, replacement) {
	var target = this;
	return target.split(search).join(replacement);
};

var send = function(code, subcode, params){
	nparam = []
	for(var param of params){
		nparam.push(param.toString().replaceAll(":", "\c").replaceAll(";", "\s").replaceAll("\n", "\e"))
	}
	var toSend = SECRET + code + ":" + subcode + ":" + nparam.join(";")
	console.log("sending: " + toSend)
	sock.send(toSend)
}

var receive = function(){
	var temp = BUFFER.split("\n")
	var value = temp.shift()
	BUFFER = temp.join("\n")
	value = value.split(":")
	code = parseInt(value[0])
	subcode = parseInt(value[1])
	nparam = []
	for(var param of value[2].split(";")){
		nparam.push(param.replaceAll("\c", ":").replaceAll(";", "\s").replaceAll("\e", "\n"))
	}
	return {"code": code, "subcode": subcode, param: nparam}
}
