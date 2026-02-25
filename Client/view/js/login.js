async function checkLogin() {
    const username = document.getElementById('uname').value;
    const password = document.getElementById('pass').value;

    const inputData = {
        username: username,
        password: password
    };

    try{
        const response = await fetch('http://localhost:8006/login', {
            method: "POST",
            body: JSON.stringify(inputData),
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        });
        const data = await response.json();
        if(data.response == "success"){
            document.cookie = "sessionID=" + data.sessionID;
            document.cookie = "uname=" + username;
            window.location.href = "/";
        }else{
            alert("Incorrect username or password. Please try again.");
            console.log("Login failed:", data);
        }
    }catch(error){
        console.error("Error:", error);
    }

}