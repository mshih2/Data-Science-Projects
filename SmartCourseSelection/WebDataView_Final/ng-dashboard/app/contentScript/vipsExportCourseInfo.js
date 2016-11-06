console.log("VIPS Start Downloading Course Information...");
var vips = new VipsAPI();
globalBlocks = vips.getVisualBlockList();
// You can see the tutorial about TreeModel here:
// http://jnuno.com/tree-model-js/
root = vips.getVisualBlockTree();
alert("We are loading the course information on this page...Please click on any COURSE TITLE!");

// The output of course titles
for (var i = 0; i < globalBlocks.length; i++) {
	var box = globalBlocks[i]['-att-box'];
	box.title = globalBlocks[i]['-vips-id'];

	// Define current node
	var cur = root.first(function (node) {
	    return node.model.data['-vips-id'] === globalBlocks[i]['-vips-id'];
	});


	// Define sibling node
	var siblings = root.all(function (node) {
	    // Sibling attributes, which include coordinate, style, font
		comp_att = ['-att-offsetLeft', '-style-font-family', '-style-font-size','-style-height','-style-font-weight', '-style-color'];
		var isSibling = true;
		for (var i = 0; i < comp_att.length; i++){
			if (node.model.data[comp_att[i]] != cur.model.data[comp_att[i]] || node.children.length != 0) {
				isSibling = false;
			}
		}
		if (isSibling) {
			return node;
		}
	});

	box.siblings = siblings;
	box.addEventListener('click', function(e){
		// Initialize lists to store course names and course descriptions
		var courseNamesId = [];	// list of vips_id of course title dom
		var courseNames = [];	// list of course title
		var courseDescId = [];	// list of vips_id of course
		var courseDesc = [];	// list of course description
		var courseInfoId = [];	// list of course info vips id
		var courseInfo = [];	// list of course title and course description

		e.preventDefault();
		var ss = this.siblings;
		console.log("You have just clicked on a block with vips-id " + this.title);
		//console.log("Here is the list of its siblings in the visual block tree:")
		for (var k = 0; k < ss.length; k++) {
			// find the vips id of course information
			var selectId = ss[k].model.data['-vips-id'];
			var infoId = '';
			// This case is when the title and content blocks are parallel
			if (selectId.match(/-/g).length == 1) {
				var sib = ss[k].model.data;
				courseNamesId.push(sib['-vips-id']);
				courseNames.push(sib['-att-innerText']);
				var desId = sib['-vips-id'].split('-');
				var newdesId = desId[0] + '-' + String(Number(desId[1]) + 1);
				for (var i = 0; i<globalBlocks.length; i++){
					if (globalBlocks[i]['-vips-id'] == newdesId) {
						var description = globalBlocks[i]['-att-innerText'];
						courseDesc.push(description);
					}
				}
			}
			// This case is when title block is in the content block
			else {
				infoId = selectId.slice(0,-2);
				courseNamesId.push(ss[k].model.data['-vips-id']);
				courseNames.push(ss[k].model.data['-att-innerText']);
			}
			// append the vips id of course
			courseInfoId.push(infoId);
		}
		this.style.border = "4px solid red";
		// write the course names as csv
		if (ss.length) {
			for (var i = 0; i<globalBlocks.length; i++){
				for (var j = 0; j<courseInfoId.length; j++){
					if (globalBlocks[i]['-vips-id'] == courseInfoId[j]){
						var info = globalBlocks[i]['-att-innerText'];
						courseInfo.push(info);
					}
				}
			}

			for (var i = 0; i<courseInfo.length; i++) {
				var splitInfo = courseInfo[i].split('\n');
				splitInfo.shift();
				var description = splitInfo.join(' ');
				courseDesc.push(description);
			}

			// Write the output list as tuples of coursenames and course //description
			var op = [];
			for(var i = 0; i<courseNames.length; i++){
				var courseTuple = [courseNames[i], courseDesc[i]];
				op.push(courseTuple);
			}

			// Write the output to txt file
			var filename = prompt("Please enter the output filename.");
			if (filename) {
				filename = filename + '.txt';
				var csvContent = "";
				op.forEach(function(infoArray, index){
   					dataString = infoArray.join(",");
   					csvContent += index < op.length ? dataString+ "\n" : dataString;
				});
				var blob = new Blob([csvContent], {type: "text/plain;charset = utf-8"});
				saveAs(blob, filename);
			}
		}
	});
}