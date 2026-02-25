function switchRole(roleId){
    document.cookie = "role="+roleId+"; path=/";
    location.reload();
}

function loadDashboard(){
    window.location.href=ROOT + '/dashboard/';
}

function showSection(sectionId){
    if(!sections.includes(sectionId)){
        showSection(sections[0]);
        return;
    }

    sections.forEach(sec => {
        if(sec === sectionId){
            document.getElementById(sec).style.display = 'block';
        } else {
            document.getElementById(sec).style.display = 'none';
        }
    });
    document.cookie = "selectedSection="+sectionId+"; path=/";
}

window.onload = function(){

    if(this.document.cookie.indexOf('selectedSection') == -1){
        showSection(sections[0]);
    } else {
        let name = 'selectedSection=';
        let decodedCookie = decodeURIComponent(this.document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                let sectionId = c.substring(name.length, c.length);
                showSection(sectionId);
            }else{
                showSection(sections[0]);
            }
        }
    }
}