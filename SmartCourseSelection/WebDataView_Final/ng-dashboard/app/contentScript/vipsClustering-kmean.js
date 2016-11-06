//Initialization
vips = new VipsAPI(); //our API
globalBlocks = vips.getVisualBlockList(); //the list that contains your data, each item is a data element

//Your algorithm to analyze the data is here
//The following code manually specifies the result as a list of IDs.
//http://infolab.stanford.edu/db_pages/members.html 
/*************************************************************/

console.log("/////Clustering, Code Start/////");
 
textlengthmin=15
colors = ["red", "blue", "green","yellow"]
clustpar=6 //expected number of course in one cluster

/// Functions ///
// Matrix
Array.matrix = function(numrows, numcols, initial) {
    var arr = [];
    for (var i = 0; i < numrows; ++i) {
        var columns = [];
        for (var j = 0; j < numcols; ++j) {
            columns[j] = initial;
        }
        arr[i] = columns;
    }
    return arr;
}

// Sort
function SortedIndex(test) {
var len = test.length;
var indices = new Array(len);
for (var i = 0; i < len; ++i) indices[i] = i;
indices.sort(function (a, b) { return test[a] > test[b] ? -1 : test[a] < test[b] ? 1 : 0; });
return indices
}

// cosine similarity
function vecDotProduct(vecA, vecB) {
	var product = 0;
	for (var i = 0; i < vecA.length; i++) {
		product += vecA[i] * vecB[i];
	}
	return product;
}

function vecMagnitude(vec) {
	var sum = 0;
	for (var i = 0; i < vec.length; i++) {
		sum += vec[i] * vec[i];
	}
	return Math.sqrt(sum);
}

function cosineSimilarity(vecA, vecB) {
	return vecDotProduct(vecA, vecB) / (vecMagnitude(vecA) * vecMagnitude(vecB)+0.000001);
}

// summation
function sumArray(array) {
	  for (
	    var
	      index = 0,              // The iterator
	      length = array.length,  // Cache the array length
	      sum = 0;                // The total amount
	      index < length;         // The "for"-loop condition
	      sum += array[index++]   // Add number on each iteration
	  );
	  return sum;
	}


//// Collect Word Elements 

// clean too frequent words//
var ignore = ['class','schedule','undergraduate','graduate','course','registration','concurrent','prerequisite','and','credit','hours','credits','hour','instructor','school','course','for','of','or','the','to','a','of','for','as','i','with','it','is','on','that','this','at','can','in','be','has','if'];
var textList = "";

// create word list
numBlock=0
for (var i = 0; i < globalBlocks.length; i++) { 
	textList += globalBlocks[i]['-att-textContent']
	numBlock++;
}
cleanlist=textList.toLowerCase().replace(/[\.]*[\,]*[\;]*[\&]*/g, '').replace( /\n/g, " " ).split(/[\s,:;]/);

var wordlist=[]
var wordcounts=[]

for (word in cleanlist) {
	if (wordlist.indexOf(cleanlist[word])==-1 && cleanlist[word]!='' && ignore.indexOf(cleanlist[word])==-1)
		wordlist.push(cleanlist[word]);	
}
wordlist.sort()

// word count for each text
wordcount= Array.matrix(numBlock,wordlist.length,0)
totalcount=[]

for (var i = 0; i < globalBlocks.length; i++) {
	myArray= globalBlocks[i]['-att-textContent'].toLowerCase().replace(/[\.]*[\,]*[\;]*[\&]*/g, '').replace( /\n/g, " " ).split(/[\s,:;]/)
	for (j in myArray){
		wordcount[i][wordlist.indexOf(myArray[j])]+=1
	}
	totalcount[i]=sumArray(wordcount[i])
}

// get the NN number of texts with most number of words

NN=Math.floor((numBlock/clustpar))

maxblocks=SortedIndex(totalcount).slice(0,NN)

simdata=Array.matrix(numBlock,NN,0)

var id = []

var vipsId = [];

for (var i = 0; i < numBlock; i++) {
	for (var j = 0; j< NN; j++) {
		if (totalcount[i]>=textlengthmin){
		simdata[i][j]=cosineSimilarity(wordcount[i], wordcount[maxblocks[j]])}
		else {simdata[i][j]=0}
	}
	vipsId.push(globalBlocks[i]['-vips-id']);
	id.push(i);
}

// set for tracking
simdata.forEach(function(block, i) {
    block.vipsId = vipsId[i];
});
simdata.forEach(function(block, i) {
    block.id = id[i];
});

var clusters = clusterfck.kmeans(simdata, Math.floor((numBlock/clustpar)));
//var clusters = clusterfck.kmeans(simdata, 5);
console.log(Math.floor((numBlock/clustpar)))
//var clusters = clusterfck.kmeans(simdata, 3);


for (var i = 0; i < clusters.length; i++) {

//    boxStyle = "2px solid " + colors[i];
	if (clusters[i]) {
    for (var j = 0; j < clusters[i].length; j++) {

        index = clusters[i][j].id; 

        var box = globalBlocks[index]['-att-box'];
//        box.style.border = boxStyle;
        box.title = globalBlocks[i]['-vips-id'];
        box.addEventListener('click', function(e){
                e.preventDefault();
                this.style.border = "4px solid green";
        });
        box.cluster = i;

    }
    }
}

console.log("Success")

alert('KMean Clustering finished. Please click on a block from your desired cluster. After you are done, click "Give Me Suggestions".');
        
 






