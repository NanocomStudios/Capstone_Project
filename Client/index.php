<?php

require_once("config.php");

if(!isset($_COOKIE["sessionID"]) || !isset($_COOKIE["uname"])){
    header("Location: /login.php");
    exit();
}else{
    $data = array('username' => $_COOKIE["uname"], 'sessionID' => $_COOKIE["sessionID"]);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://auth-service:8000/get_role");
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    $r = curl_exec($ch);

    if ($r === false) {
        // Handle error
        echo "Error: " . curl_error($ch);
        exit;
    }
    $response = json_decode($r);
    
    if($response->role == "none"){
        header("Location: /login.php");
        exit();
    }else{
        switch ($response->role) {
            case "client":
                require_once("view/client.php");
                break;

            case "driver":
                require_once("view/driver.php");
                break;

            case "warehouse":
                require_once("view/warehouse.php");
                break;
            
            default:
                header("Location: /login.php");
                exit();
                break;
        }
    }
}
