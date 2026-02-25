<?php

class NavLink{
    public $href;
    public $text;
    public $cssClass;

    function __construct($hrf, $txt, $cls=""){
        $this->href = $hrf;
        $this->text = $txt;
        $this->cssClass = $cls;
    }

    public function render(){
        echo '<a href="'.$this->href.'" class="nav-item '.$this->cssClass.'">'.$this->text.'</a>';
    }

}

class NavButton{
    private $label;
    private $option;
    private $cssClass;
    private $id;

    function __construct($label, $option="", $cssClass="", $id=""){
        $this->label = $label;
        $this->option = $option;
        $this->cssClass = $cssClass;
        $this->id = $id;
    }

    public function render(){
        echo '<a '.$this->option.' class="nav-item '.$this->cssClass.'" id="'.$this->id.'">'.$this->label.'</a>';
    }

}

class NavBarView{
    private $navLinks = [];

    public function addItem($navLink){
        $this->navLinks[] = $navLink;
    }

    public function render(){
        global $deviceType;
        echo '<link rel="stylesheet" type="text/css" href=" '.ROOT.'/view/css/navbar.css">';
        
        echo '<div class="header">
            <a href="'.ROOT.'/" style="text-decoration: none;color:white;"><h1>'.COMPANY_NAME.'</h1></a>
            <nav class="nav">';
                foreach ($this->navLinks as $navLink) {
                    $navLink->render();
                }
            echo '</nav>
            </div>';
    }
}




        