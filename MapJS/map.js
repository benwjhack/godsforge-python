canvas = document.getElementById("mapCanvas");
cellDetailsContainer = document.getElementById("thingsInCell");
cellNameContainer = document.getElementById("cellName")
map = []

numHorizCells = 20
numVertCells = 20
cellWidth = canvas.width/numHorizCells;
cellHeight = canvas.height/numVertCells;

voidColour = "#000000";
creatureColour = "#FF0000";

function loadMap(stuff) {
	var newMap=[];	
	
	for (var i=-numHorizCells/2; i<numHorizCells/2; i++) {
		var row=[];
		for (var j=-numVertCells/2; j<numVertCells/2; j++) {
			var tmp = {
				x: i,
				y: j,
				void: true,
				landName: "Empty Void",
				colour: voidColour,
				fortifications: [],
				equipment: [],
				artifacts: [],
				paragons: [],
				creatures: [],
			} //base empty cell

			for (var k=0; k<stuff.length; k++) { //populate the cell
				if (stuff[k].x == i && stuff[k].y == j) {
					if (stuff[k].type=="land") {
						tmp.void = false;
						tmp.colour = stuff[k].colour;
						tmp.landName = stuff[k].name;
						tmp.land = stuff[k];
					}
					if (stuff[k].type=="fortification") {
						tmp.fortifications.push(stuff[k])
					}
					if (stuff[k].type=="equipment") {
						tmp.equipment.push(stuff[k])
					}
					if (stuff[k].type=="artifact") {
						tmp.artifacts.push(stuff[k])
					}
					if (stuff[k].type=="race" || stuff[k].type=="legend") {
						tmp.creatures.push(stuff[k])
					}
				}
			}

			row.push(tmp);
		}
		newMap.push(row);
	}
	
	map = newMap;
}

function drawMap() {
	var ctx=canvas.getContext("2d");
	
	for (var x=0; x<numHorizCells; x++) {
		for (var y=0; y<numVertCells; y++) {
			ctx.fillStyle = map[x][y].colour
			ctx.fillRect(x * cellWidth, y * cellWidth, cellWidth, cellHeight);

			if (map[x][y].creatures.length > 0) {
				ctx.beginPath();
				ctx.arc( (x+0.5) * cellWidth, (y+0.5) * cellWidth, cellWidth*0.2, 0, 2*Math.PI );

				ctx.fillStyle = creatureColour;
				ctx.strokeStyle = voidColour;
				ctx.stroke();
				ctx.fill();

				ctx.closePath()
			}
		}
	}
}

function listOfStuffIn(cell) {
	out = ""

	if (cell.creatures.length > 0) {
		out += "<li>Creatures<ul>"

		for (var i=0; i<cell.creatures.length; i++) {
			var c = cell.creatures[i];

			var keywords = "";
			if (c.keywords && c.keywords.length>0) {
				for (var j=0; j<c.keywords.length; j++) {
					if (j == 0) {keywords += " ("}
					if (j > 0) {keywords += ", "}
					keywords += c.keywords[j];
				}
			}
			if (keywords!="") {keywords += ")"}

			var traits = "";
			if (c.traits && c.traits.length>0) {
				for (var j=0; j<c.traits.length; j++) {
					if (j == 0) {traits += " ("}
					if (j > 0) {traits += ", "}
					traits += c.traits[j];
				}
			}
			if (traits!="") {traits += ")"}

			out += "<li>" + c.value + "DP " + c.type + keywords + traits + ": " + c.name + ". </li>"
		}

		out += "</ul></li>"
	}

	if (cell.fortifications.length > 0) {
		out += "<li>Fortifications<ul>"

		for (var i=0; i<cell.fortifications.length; i++) {
			var c = cell.fortifications[i];

			var keywords = "";
			if (c.keywords && c.keywords.length>0) {
				for (var j=0; j<c.keywords.length; j++) {
					if (j == 0) {keywords += " ("}
					if (j > 0) {keywords += ", "}
					keywords += c.keywords[j];
				}
			}
			if (keywords!="") {keywords += ")"}

			out += "<li>" + c.value + "DP " + c.type + keywords + ": " + c.name + ". </li>"
		}

		out += "</ul></li>"
	}

	if (cell.equipment.length > 0) {
		out += "<li>Equipment<ul>"

		for (var i=0; i<cell.equipment.length; i++) {
			var c = cell.equipment[i];

			var keywords = "";
			if (c.keywords && c.keywords.length>0) {
				for (var j=0; j<c.keywords.length; j++) {
					if (j == 0) {keywords += " ("}
					if (j > 0) {keywords += ", "}
					keywords += c.keywords[j];
				}
			}
			if (keywords!="") {keywords += ")"}

			out += "<li>" + c.value + "DP " + c.type + keywords + ": " + c.name + ". </li>"
		}

		out += "</ul></li>"
	}

	if (cell.artifacts.length > 0) {
		out += "<li>Artifacts<ul>"

		for (var i=0; i<cell.artifacts.length; i++) {
			var c = cell.artifacts[i];

			var keywords = "";
			if (c.keywords && c.keywords.length>0) {
				for (var j=0; j<c.keywords.length; j++) {
					if (j == 0) {keywords += " ("}
					if (j > 0) {keywords += ", "}
					keywords += c.keywords[j];
				}
			}
			if (keywords!="") {keywords += ")"}

			var shards;
			if (c.shards == 0) {shards = "no shard"}
			if (c.shards == 1) {shards = "shard"}
			if (c.shards > 1) {shards = c.shards + " shards"}

			out += "<li>" + c.value + "DP " + c.type + keywords + " (" + shards + ")" + ": " + c.name + ". </li>"
		}

		out += "</ul></li>"
	}

	return out;
}


loadMap([]);
drawMap();

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		loadMap(JSON.parse(this.responseText));
		drawMap();
	}
};
xhttp.open("GET", "stuff.json", true);
xhttp.send();





canvas.addEventListener("mousemove", function(e) {
	var mouseX = e.clientX - Math.floor(canvas.getBoundingClientRect().left);
	var mouseY = e.clientY - Math.floor(canvas.getBoundingClientRect().top);
	var hoverX = Math.floor(mouseX/cellWidth);
	var hoverY = Math.floor(mouseY/cellHeight);
	
	hoverCell = map[hoverX][hoverY];

	var nameUsed = hoverCell.landName;
	var extras = ""
	if (!hoverCell.void) {
		extras = " (" + hoverCell.land.value + "DP";
			if (hoverCell.land.keywords && hoverCell.land.keywords.length>0) {
				for (var j=0; j<hoverCell.land.keywords.length; j++) {
					extras += ", "
					extras += hoverCell.land.keywords[j];
				}
			}
		extras += ")"
	}

	cellNameContainer.innerHTML = nameUsed + extras;
	cellDetailsContainer.innerHTML = listOfStuffIn(hoverCell); //TODO: IMPROVE THIS
})

canvas.addEventListener("mouseleave", function(e) {
	cellNameContainer.innerHTML = "";
	cellDetailsContainer.innerHTML = "";
})


