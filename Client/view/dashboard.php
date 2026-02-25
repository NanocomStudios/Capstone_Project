<?php
require_once("navbar.php");
require_once("input.php");
require_once("table.php");
require_once("cardGrid.php");
class DashboardHeader{
    public function render(){
        global $deviceType;

        echo '<html>
                <head>    
                    <link rel="stylesheet" type="text/css" href="'.ROOT.'/view/css/main.css">
                    <link rel="stylesheet" type="text/css" href="'.ROOT.'/view/css/input.css">
                    <link rel="stylesheet" type="text/css" href="'.ROOT.'/view/css/settings.css">
                    <link rel="stylesheet" type="text/css" href="'.ROOT.'/view/css/styles.css">

                    <script src="'.ROOT.'/view/js/input.js"></script>
                    <script src="'.ROOT.'/view/js/dashboard.js"></script>
                    <script src="'.ROOT.'/view/js/popup.js"></script>
                </head>
                <body>';

        $nav = new NavBarView();

        // $user = new UserModel();
        // $users = new Users();
        
        // if ($user->isLoggedIn() > 0){
        //     $dropdown = new DropDownView($user->getFirstName($_COOKIE['user']),'drp1', 'nav-item');
    
        //     if($user->isLoggedIn() == ACC_CUSTOMER){
        //         $dropdown->addItem(new DropDownButton('Dashboard', 'onClick="loadDashboard();"'));
        //     }

        //     $roleList = $users->getUserRoleArray($user->getRole());
    
        //     foreach($roleList as $key => $role){
        //         foreach($role as $key => $val){
        //             $dropdown->addItem(new DropDownButton($val, 'onClick="switchRole(\''.$key.'\');"', $key));
        //         }
        //     }
    
        //     $dropdown->addItem(new DropDownLink('?action=logout', 'Logout'));
    
        //     $nav->addItem($dropdown);
        // }else{
        //     $nav->addItem(new NavLink('?action=login', 'Login'));
        //     $nav->addItem(new NavLink('?action=register', 'Register', 'active'));
        // }
        $nav->addItem(new NavLink('/logout.php', 'Logout', 'active'));
        $nav->render();
    }

    
}

class DashboardView {
    private $sections = [];

    public function addSection($section){
        $this->sections[] = $section;
    }

    public function render(){
        
        echo '<div class="body-content">
                <div class="main-content">';

        foreach ($this->sections as $section) {
            $section->render();
        }

        echo '</div>
            </div>';
    }
}



class Section{
    private $subSections = [];
    private $heading;
    private $options;
    private $class;

    private $heading_id;
    private $heading_options;

    public function addSubSection($subSection){
        $this->subSections[] = $subSection;
    }

    function __construct($heading = "", $class = "" ,$options = ""){
        if($heading != ""){
            $this->heading = $heading;
        }
        $this->options = $options;
        $this->class = $class;
    }

    function setHeading($heading="", $id="",  $options=""){
        $this->heading = $heading;
        $this->heading_id = $id;
        $this->heading_options = $options;

    }

    public function render(){

        echo '<div class="section '.$this->class.'" '.$this->options.'>
                <div class="settings-section">';
        
        if(isset($this->heading)){
            echo '<div class="section-header"><h2 id="'.$this->heading_id.'" '.$this->heading_options.'>'.$this->heading.'</h2></div>';
        }
        
        foreach ($this->subSections as $subSection) {
            $subSection->render();
        }

        echo '  </div>
            </div>';
    }
}

class SubSection{
    private $itemList = [];

    private $options;
    public function __construct($options=""){
        $this->options = $options;
    }

    public function addItem($item){
        $this->itemList[] = $item;
    }

    public function render(){
        echo '<div class="settings-subsection" '.$this->options.'>';

        foreach ($this->itemList as $item) {
            $item->render();
        }

        echo '</div>';
    }
}

class OtherObject{
    private $code;

    public function __construct($code){
        $this->code = $code;
    }

    public function render(){
        echo $this->code;
    }
}

class PopupOverlay{
    public function render(){
        echo '<link rel="stylesheet" type="text/css" href="'.ROOT.'/view/css/popup.css">';
        echo '<script src="'.ROOT.'/view/js/popup.js"></script>';
        echo '<div class="popup-overlay" id="popupOverlay"></div>';
    }
}


class CalendarView{

    private $id;
    private $weekCount;
    private $selectedDay;
    private $selectedMonth;
    private $selectedYear;

    public function __construct($id, $selectedDay, $selectedMonth, $selectedYear,  $weekCount = 4, $action=""){
        $this->id = $id;
        $this->selectedDay = $selectedDay;
        $this->selectedMonth = $selectedMonth;
        $this->selectedYear = $selectedYear;
        $this->weekCount = $weekCount;
        $this->action = $action;
    }
    public function render(){
        echo "<link rel=\"stylesheet\" type=\"text/css\" href='".ROOT."/view/css/calendar.css'>";
        echo "<script src='".ROOT."/view/js/calendar.js'></script>";

        echo "<div class='calendar-container'>

                <table class='calendar' id='".$this->id."'>
                    <thead>
                        <tr>
                            <th>Sun</th>
                            <th>Mon</th>
                            <th>Tue</th>
                            <th>Wed</th>
                            <th>Thu</th>
                            <th>Fri</th>
                            <th>Sat</th>
                        </tr>
                    </thead>
                    <tbody id='".$this->id."-body'>
                    </tbody>
                </table>
            </div>";

        echo "<script>
                loadCalendar('".$this->id."', ".$this->weekCount.", ".($this->selectedDay - 1).", ".($this->selectedMonth - 1).", ".$this->selectedYear.", '".$this->action."');
              </script>";
    }
}
