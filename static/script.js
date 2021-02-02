function popupMenu(){
    let elems = document.getElementsByClassName("popup__content");
    var popupDiv = document.getElementById("popup");
    document.documentElement.style.overflowY = "hidden"; 
    for(let i = 0; i<elems.length;i++){
        elems[i].style.display = "block";
        elems[i].style.position = "absolute";
        elems[i].style.top =  (screen.height - popupDiv.clientHeight)/2 - 50 + "px";
        elems[i].style.left = (screen.width - popupDiv.clientWidth)/2 - 5 + "px";
        elems[i].style.margin = "0 auto";
    }

    turnOnDiv();
    turnOnClose();
}

function turnOnDiv(){
    let div = document.getElementById("opaque__layer");
    var opacity_value = 0.00;
    var id = setInterval(frame, 10);
    function frame(){
        if(opacity_value >= 0.95){
            clearInterval(id);
        }
        else{
            opacity_value += 0.1;
            div.style.opacity = opacity_value;
        }
    }
}

function turnOffDiv(){
    let div = document.getElementById("opaque__layer");
    var opacity_value = 0.95;
    var id = setInterval(frame, 10);
    function frame(){
        if(opacity_value <= 0){
            clearInterval(id);
        }
        else{
            opacity_value -= 0.1;
            div.style.opacity = opacity_value;
        }
    }
}

function turnOnClose(){
    var close = document.getElementById("close__button");
    close.style.display = "block";
    close.style.position = "absolute";
    close.style.marginLeft = "0%";
    close.style.top = "4%";
}

function turnOffClose(){
    var close = document.getElementById("close__button");
    close.style.display = "none";
}

function closePopupMenu(){
    let elems = document.getElementsByClassName("popup__content");
    document.documentElement.style.overflowY = "scroll"; 
    for(let i = 0; i<elems.length;i++){
        elems[i].style.display = "none";
        elems[i].style.overflow = "hidden";
    }
    turnOffDiv();
    turnOffClose();
}
