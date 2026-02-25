function changePasswordVisibility(passwordBoxID, passwordVisibilityIconID){
    let passwordBox = document.getElementById(passwordBoxID);
    if(passwordBox.type == "password"){
        passwordBox.type = "text";
        document.getElementById(passwordVisibilityIconID).style.backgroundImage = "url(" + ROOT + "/view/html/css/icons/eye-open.svg)";
    }else{
        passwordBox.type = "password";
        document.getElementById(passwordVisibilityIconID).style.backgroundImage = "url(" + ROOT + "/view/html/css/icons/eye-close.svg)";
    }
}

function toggleCheckBox(checkboxID){
    let checkbox =  document.getElementById(checkboxID);
    checkbox.checked = !checkbox.checked;
}
