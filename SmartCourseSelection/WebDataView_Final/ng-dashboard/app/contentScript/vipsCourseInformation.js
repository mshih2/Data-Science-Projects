console.log("Course Information");

// Read vips API and the globalBlocks
var vips = new VipsAPI();
globalBlocks = vips.getVisualBlockList();

var pattern1 = new RegExp("^\s*([A-Z]{2,7})\xa0*\s*([A-Z]*[0-9]+[A-Z]*)(.*)", "m");

// Only look for sub blocks
var pattern2 = new RegExp("^[0-9]*-[0-9]*-[0-9]*$", "m");

var numBlock = 0;

for (var i = 0; i < globalBlocks.length; i++) {

    if (pattern1.test(globalBlocks[i]['-att-textContent'])) {
        if (pattern2.test(globalBlocks[i]['-vips-id'])) {

            var myArray = pattern1.exec(globalBlocks[i]['-att-textContent']);
            numBlock++;

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


if (numBlock > 0) {
    console.log("Success, found %d blocks.", numBlock);
} else {
console.log("Fail, found 0 block.");
}

