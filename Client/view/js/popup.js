function hidePopup(id){
    document.getElementById("popupOverlay").style.display = "none";
    document.getElementById(id).style.display = "none";
    document.body.style.overflow = "auto";
}

function showPopup(id){
    document.getElementById("popupOverlay").style.display = "flex";
    document.getElementById(id).style.display = "flex";
    document.body.style.overflow = "hidden";
}