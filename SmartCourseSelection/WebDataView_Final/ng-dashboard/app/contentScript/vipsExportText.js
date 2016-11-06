//Initialization
vips = new VipsAPI(); //our API
globalBlocks = vips.getVisualBlockList(); //the list that contains your data, each item is a data element

//Your algorithm to analyze the data is here
//The following code manually specifies the result as a list of IDs.
//http://infolab.stanford.edu/db_pages/members.html 
/*************************************************************/


// String variable to store the output
var textList = "";

for (var i = 0; i < globalBlocks.length; i++) {

    var box = globalBlocks[i]['-att-box'];
    if (box.style.border == "2px solid red") {
        textList += globalBlocks[i]['-att-textContent'] + "\n";
    }
}


// Download data
//var confirmed = confirm("We think the highlighted blocks are interesting data in this page. Do you want to save it?"); 
//if (confirmed){
var strout = textList
var filename = prompt("Please enter the output filename.");
filename = filename + '.txt';
var blob = new Blob([strout], {type: "text/plain;charset=utf-8"});
saveAs(blob, filename);
//}


