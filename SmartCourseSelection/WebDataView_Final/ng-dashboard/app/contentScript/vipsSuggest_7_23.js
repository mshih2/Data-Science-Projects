//Initialization
vips = new VipsAPI(); //our API
globalBlocks = vips.getVisualBlockList(); //the list that contains your data, each item is a data element

//Your algorithm to analyze the data is here
//The following code manually specifies the result as a list of IDs.
//http://infolab.stanford.edu/db_pages/members.html 
/*************************************************************/

var pattern1 = new RegExp("^\s*([A-Z]{2,7})\xa0*\s*([A-Z]*[0-9]+[A-Z]*)(.*)", "m");

// Only look for sub blocks
var pattern2 = new RegExp("^[0-9]*-[0-9]*-[0-9]*$", "m");

var numBlock = 0;

// String variable to store the output
var textList = "";

for (var i = 0; i < globalBlocks.length; i++) {

    if (pattern1.test(globalBlocks[i]['-att-textContent'])) {
        if (pattern2.test(globalBlocks[i]['-vips-id'])) {

            var myArray = pattern1.exec(globalBlocks[i]['-att-textContent']);
            numBlock++;

            //textList += myArray[1] + "," + myArray[2] + "," + myArray[3] + "\n";
            textList += globalBlocks[i]['-att-textContent'] + "\n";

            // get box object and highlight
            var box = globalBlocks[i]['-att-box'];
            box.style.border = "2px solid #FF0000";
            box.title = globalBlocks[i]['-vips-id'];
            box.addEventListener('click', function(e){
                    e.preventDefault();
                    this.style.border = "4px solid blue";
            });

            //// test
            //console.log(i, myArray[1], myArray[2], myArray[3]);
            //console.log(i, globalBlocks[i]['-vips-id']);
        }
    }

}

// For testing
if (numBlock > 0) {
    console.log("Success, found %d blocks.", numBlock);
} else {
console.log("Fail, found 0 block.");
}


// Download data
var confirmed = confirm("We think the highlighted blocks are interesting data in this page. Do you want to save it?"); 
if (confirmed){
    var strout = textList
    filename = 'vips_' + window.location.host + '.txt';
    var blob = new Blob([strout], {type: "text/plain;charset=utf-8"});
    saveAs(blob, filename);
}


