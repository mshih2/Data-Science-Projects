//Initialization
vips = new VipsAPI(); //our API
globalBlocks = vips.getVisualBlockList(); //the list that contains your data, each item is a data element

//Your algorithm to analyze the data is here
//The following code manually specifies the result as a list of IDs.
//http://infolab.stanford.edu/db_pages/members.html 
/*************************************************************/

console.log("Clustering");


function getColors(n){
    
    var colors = ['#db5f57', '#dbc257', '#91db57', '#57db80', '#57d3db', '#5770db', '#a157db', '#db57b2'];
    var colors_sel = [];

    for (var i = 0; i < n; i++) { 

        var num = Math.floor(Math.random() * 8); 
        while (colors_sel.indexOf( colors[num] ) != -1) { 
            var num = Math.floor(Math.random() * 8);
        }
        colors_sel.push(colors[num]);
    }

    return colors_sel
}

function inorder_traversal(node){
    if (node){

        //traverse the right subtree
        if (node.right !== null){
            inorder_traversal(node.right);
        }

        //call the process method on this node
        //process.call(this, node);
        if (node.hasOwnProperty('value')) {
            console.log(node.value);
        }

        //traverse the left subtree
        if (node.left !== null){
            inorder_traversal(node.left);
        }            
    }
}

// Euclidean distance 
function Euclidean(a, b) {
  var d = 0;
  for (var i = 0; i < a.length; i++) {
    d += Math.pow(a[i] - b[i], 2);
  }
  return Math.sqrt(d);
}

function removeBlank(List) {
    var newList = [];
    for (var i = 0; i < List.length; i++) {
        if (List[i] != "") {
            newList.push(List[i]);
        }
    }
    return newList;              
}

function getMinMaxOf2DIndex (arr, idx) {
    return {
        min: Math.min.apply(null, arr.map(function (e) { return e[idx]})),
        max: Math.max.apply(null, arr.map(function (e) { return e[idx]}))
    }
} 


//////////////////////////////////
////////////// Main //////////////
//////////////////////////////////

//// Ask user if we should use small block or large block
var smallBlock = confirm("Do you want to group the blocks base on the small block? If not, we will use large blocks, which may contain more than 1 small blocks."); 
if (smallBlock) {
    var pattern2 = new RegExp("^[0-9]*-[0-9]*-([0-9]*)$", "m");
} else {
    var pattern2 = new RegExp("^[0-9]*-([0-9]*)$", "m");
}


//// Ask user for number of clusters
var nCluster = prompt("Please enter the number of clusters: (2~8)");
if (!isNaN(nCluster)) {
    var nCluster = parseInt(nCluster, 10);
} else {
    alert('This is not a number.');
}
console.log('Choose '+nCluster+' clusters.');
if (nCluster < 2 || nCluster > 8) {
    alert('The number is not valid.');
} 

//// Get the list of colors to use
var colors = getColors(nCluster);


var pattern3 = new RegExp("[^A-Za-z0-9_]+", "m");
var pattern4 = new RegExp("([0-9]+)", "m");
//var pattern5 = new RegExp("([0-9]{1,3}).+([0-9]{1,3}).+([0-9]{1,3})", "m");

var data = [];
var vipsId = [];
var id = [];


//// Collect 
for (var i = 0; i < globalBlocks.length; i++) {

    if (pattern2.test(globalBlocks[i]['-vips-id'])) {

        // Features [subblock number, word count]
        var tuple = []; 

        if (smallBlock) {
            //// Subblock number
            var reMatchArray = pattern2.exec(globalBlocks[i]['-vips-id']);
            tuple.push(parseInt(reMatchArray[1], 10));

            //// Word count
            var rawList = globalBlocks[i]['-att-textContent'].split(pattern3);        
            List = removeBlank(rawList);
            tuple.push(List.length);

            //// -att-offsetLeft
            tuple.push(parseInt(globalBlocks[i]['-att-offsetLeft'], 10));

            //// -style-font-size
            var reMatchArray = pattern4.exec(globalBlocks[i]['-style-font-size']);
            tuple.push(parseInt(reMatchArray[1], 10));

            //// -style-height
            var reMatchArray = pattern4.exec(globalBlocks[i]['-style-height']);
            tuple.push(parseInt(reMatchArray[1], 10));

            //// -style-font-weight
            if (globalBlocks[i]['-style-font-weight'] == 'normal') {
                tuple.push(0);
            } else {
                tuple.push(1);
            }
        } else {
            //// Word count
            var rawList = globalBlocks[i]['-att-textContent'].split(pattern3);        
            List = removeBlank(rawList);
            tuple.push(List.length);

            //// -style-height
            var reMatchArray = pattern4.exec(globalBlocks[i]['-style-height']);
            tuple.push(parseInt(reMatchArray[1], 10));

            //// -att-childElementCount
            tuple.push(parseInt(globalBlocks[i]['-att-childElementCount'], 10));

        }

        ////// -style-color
        //var reMatchArray = pattern5.exec(globalBlocks[i]['-style-color']);
        //tuple.push(parseInt(reMatchArray[1], 10));
        //tuple.push(parseInt(reMatchArray[2], 10));
        //tuple.push(parseInt(reMatchArray[3], 10));


        data.push(tuple);
        vipsId.push(globalBlocks[i]['-vips-id']);
        id.push(i);
    }
}


//// Set id for tracking purposes
data.forEach(function(block, i) {
    block.vipsId = vipsId[i];
});
data.forEach(function(block, i) {
    block.id = id[i];
});

console.table(data);


//// Normalization
for (var i = 0; i < data[0].length; i++) {

    minMax = getMinMaxOf2DIndex(data, i); 
    range = minMax.max - minMax.min;

    if (range == 0) {
        for (var j = 0; j < data.length; j++) {
            data[j][i] = 0;
        }
    } else {
        for (var j = 0; j < data.length; j++) {
            data[j][i] = (data[j][i] - minMax.min) / range;
        }
    }
}

console.table(data);




//// Actual clustering
var clusters = clusterfck.kmeans(data, nCluster);
//var clusters = clusterfck.hcluster(data, "euclidean", "single");


//// hierarchical clustering
//var levels = Cluster({
//  input: data,
//  distance: Euclidean,
//  linkage: averageLink,
//  minClusters: 2, // only want two clusters 
//});
//var clusters = levels[levels.length - 1].clusters;
//console.log(levels);
//console.log(clusters);


//// Highlight and label the cluster number on each box
for (var i = 0; i < clusters.length; i++) {

    boxStyle = "2px solid " + colors[i];
    for (var j = 0; j < clusters[i].length; j++) {

        index = clusters[i][j].id; 

        var box = globalBlocks[index]['-att-box'];
        box.style.border = boxStyle;
        box.title = globalBlocks[i]['-vips-id'];
        box.addEventListener('click', function(e){
                e.preventDefault();
                this.style.border = "4px solid green";
        });
        box.cluster = i;

    }
    console.table(clusters[i]);
}

alert('Clustering finished. Please click on a block from your desired cluster. After you are done, click "Give Me Suggestions".');


