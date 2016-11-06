console.log("Highlight Selected Block and Get Block Information");

if (typeof changeBorderForVipsSelection != 'function') {
	changeBorderForVipsSelection = function(){
		event.preventDefault();
		if (event.target.style.border == "") {
	    	event.target.style.border = "2px solid #FF0000";
	    	// Get coordinates of target event
	    	var UpLeft = [event.target.offsetLeft, event.target.offsetTop];
			var BotRight = [event.target.offsetLeft + event.target.offsetWidth, event.target.offsetTop + event.target.offsetHeight];
			console.log("UpperLeft Coordinates:" + UpLeft);
			console.log("BottomRight Coordinates:" + BotRight);
			// Get content of target event
			console.log("Element Content:" + event.target.innerHTML);


	    }
	    else {
	    	event.target.style.border = "";
	    }
	}
}


document.addEventListener("click", changeBorderForVipsSelection);
