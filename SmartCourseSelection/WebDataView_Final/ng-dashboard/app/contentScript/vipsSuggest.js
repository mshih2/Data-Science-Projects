//Initialization
vips = new VipsAPI(); //our API
globalBlocks = vips.getVisualBlockList(); //the list that contains your data, each item is a data element

//Your algorithm to analyze the data is here
//The following code manually specifies the result as a list of IDs.
//http://infolab.stanford.edu/db_pages/members.html 
/*************************************************************/


for (var i = 0; i < globalBlocks.length; i++) {

    var box = globalBlocks[i]['-att-box'];
    if (box.style.border == "4px solid green") {
        var cluster = box.cluster;
        console.log(i, box.cluster);
    }
}

if (typeof cluster == 'undefined') {
    alert("Selected box is not recognized by VIPS.");
}


var numBlock = 0;

for (var i = 0; i < globalBlocks.length; i++) {

    var box = globalBlocks[i]['-att-box'];
    if (box.hasOwnProperty('cluster') && box.cluster == cluster) {
            
            numBlock++;

            // get box object and highlight
            var box = globalBlocks[i]['-att-box'];
            box.style.border = "2px solid red";
            box.addEventListener('click', function(e){
                    e.preventDefault();
                    this.style.border = "";
            });

            //// test
            //console.log(i, myArray[1], myArray[2], myArray[3]);
            //console.log(i, globalBlocks[i]['-vips-id']);
    } else {
        box.style.border = "";
    }
}

// For testing
if (numBlock > 0) {
    console.log("Success, found %d blocks.", numBlock);
} else {
console.log("Fail, found 0 block.");
}


//// Download data
//var confirmed = confirm("We think the highlighted blocks are interesting data in this page. Do you want to save it?"); 
//if (confirmed){
//    var strout = textList
//    filename = 'vips_' + window.location.host + '.txt';
//    var blob = new Blob([strout], {type: "text/plain;charset=utf-8"});
//    saveAs(blob, filename);
//}

alert('All of the "red blocks" are in the same cluster as your selection. If you think any "red blocks" is wrong, simply click it again to remove it. After you are done, please click "Export Text Data" to save the result.');

