<!DOCTYPE HTML>
<html>
  <head>
    <title>Login</title>
    <script src="<?php echo ROOT ?>/view/js/login.js"></script>
    <link rel="stylesheet" type="text/css" href="<?php echo ROOT."/view/css/main.css"; ?>">
    <link rel="stylesheet" type="text/css" href="<?php echo ROOT."/view/css/form.css"; ?>">
    <link rel="stylesheet" type="text/css" href="<?php echo ROOT."/view/css/input.css"; ?>">

    <script src="<?php echo ROOT;?>/view/js/input.js"></script>
  </head>
  <body>
    <div class="container">
      <div class="formContainer">
        <div class="formBox">
            <h1><?php echo COMPANY_NAME;?></h1>
            <div>

              <div class="form-card">
                <div class="input-card">
                  <input type="email" class="input" placeholder=" " id="uname" tabindex="1">
                  <label class="input-label">User Name</label>
                  <div class="input-option input-option-email"></div>
                </div>
              </div>

              <div class="form-card">
                <div class="input-card">
                  <input type="password" class="input" placeholder=" " id="pass" tabindex="2">
                  <label class="input-label">Password</label>
                  <button class="input-option input-option-password" id="passwordVisibilityButton" onClick="changePasswordVisibility('pass','passwordVisibilityButton');"></button>
                </div>
              </div>
            </div>
            <div class="align-right m-b-1">
              <a href="?action=forgotPassword" class="link-small">Forgot Password</a>
            </div>
            
            <button onclick="checkLogin()" id="loginBtn" class="submitButton" tabindex="3">Login</button>
            
            <div class="align-left m-t-1 m-b-1 text-normal">
              Don't have an account?
              <a href="?action=register" class="link-normal underline m-l-0_5">Register</a>
            </div>

        </div>
      </div>  
    </div>
  </body>
</html>
<!-- >