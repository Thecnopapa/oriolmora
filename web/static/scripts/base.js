


window.addEventListener('load', event => {
    init()
})


function init(){
    let horizontalScrollElements = [...document.getElementsByClassName("horizontal-scroll")];
    horizontalScrollElements.forEach(element => {
        verticalToHorizontal(element);
    })
    loadAllImages()
}


function verticalToHorizontal(element){
    if (window.innerHeight < element.innerWidth){
        element.addEventListener("wheel", e => {
                console.log("Wheel");
                if (Math.abs(e.deltaY) > 0 && e.deltaX === 0){
                    element.scrollLeft += e.deltaY*2;
                    console.log(e.deltaY, element.scrollLeft);
                }
            });
            element.addEventListener("scrollend", e => {
                console.log(document.elementFromPoint(document.body.offsetWidth / 2, document.body.offsetHeight / 2));

                document.elementFromPoint(document.body.offsetWidth / 2, document.body.offsetHeight / 2).scrollIntoView({block: "center", inline: "center"});
            })
            //element.addEventListener("touchend", e => {console.log("touchend");document.elementFromPoint(document.body.offsetWidth / 2, document.body.offsetHeight / 2).scrollIntoView({block: "center", inline: "center"});})
    }
}


function loadAllImages() {
    loadImages("fast");
    loadImages("normal");
    loadImages("slow");
}

async function loadImages(selection){
    let selectedImages = document.getElementsByClassName(selection+"-image");
    console.log(selection);
    console.log(selectedImages);
    let changedImages = 0;
    let changedVideos = 0;
    for (let i = 0; i < selectedImages.length; i++) {
	    try{
            const url = selectedImages[i].attributes.background.value;
            console.log(selectedImages[i].tagName);
            if (selectedImages[i].tagName === "IMG"){
                selectedImages[i].src = url;
            } else {
                selectedImages[i].style.backgroundImage = "url('" + url + "')";
            }
            imagesToPreload.push(url);
			changedImages++;

		    selectedImages[i].removeAttribute("background");
		    selectedImages.classList.remove(selection-"-image");
	    } catch(err){}
    }
    console.log(" * "+ selection +" images loaded (" + changedImages + ") videos: "+changedVideos);

}





