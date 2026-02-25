<?php

setcookie("uname", "", time() - 3600, "/");
setcookie("sessionID", "", time() - 3600, "/");

header("Location: /");
        exit();