<?php

abstract class Input{
    protected $label;
    protected $id;
    protected $size;
    protected $options;

    public function __construct($label, $size = "", $id = "", $options=""){
        $this->label = $label;
        $this->id = $id;
        if($size != ""){
            $this->size = "-".$size;
        }else{
            $this->size = "";
        }
        $this->options = $options;
    }

    abstract public function render();
}

class InputText extends Input{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="text" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
            </div>';
    }
}

class InputPassword extends Input{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="password" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
                <button class="input-option input-option-password" id="'.$this->id.'VisibilityButton" onClick="changePasswordVisibility(\''.$this->id.'\',\''.$this->id.'VisibilityButton\');"></button>
            </div>';
    }
}

class InputEmail extends Input{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="email" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
                <div class="input-option input-option-email"></div>
            </div>';
    }
}

class InputTel extends Input{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="tel" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
                <div class="input-option input-option-tel"></div>
            </div>';
    }
}

class InputNumber extends Input{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="number" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
                <div class="input-option input-option-number"></div>
            </div>';
    }
}

class InputDate extends Input{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="date" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
            </div>';
    }
}

class InputTime extends Input{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="time" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
            </div>';
    }
}

class InputSearch extends Input{
    private $searchDropDown;

    public function __construct($label, $size = "", $id = "", $options="", $searchDropDown = null){
        $this->label = $label;
        $this->id = $id;
        if($size != ""){
            $this->size = "-".$size;
        }else{
            $this->size = "";
        }
        $this->options = $options;
        $this->searchDropDown = $searchDropDown;
    }
    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="search" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
                <div class="input-option input-option-search"></div>';

                if($this->searchDropDown != null){
                    $this->searchDropDown->render();
                }

            echo '</div>';
    }
}

class InputUrl extends Input{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="url" class="input" placeholder=" " id="'.$this->id.'" '.$this->options.'>
                <label class="input-label">'.$this->label.'</label>
                <div class="input-option input-option-url"></div>
            </div>';
    }
}

class InputCheckBox extends Input{

    public function render(){
        echo '<div class="input-card settings-card checkbox-card'.$this->size.'">
                <label class="checkbox-label">'.$this->label.'</label>
                <div class="switch-box">
                    <div class="switch">
                        <input type="checkbox" class="" id="'.$this->id.'" '.$this->options.'>
                        <span class="slider round"  onclick="toggleCheckBox(\''.$this->id.'\');"></span>
                    </div>
                </div>
            </div>';
    }
}

class InputSelect extends Input{

    private $optionList = [];

    public function addOption($option){
        $this->optionList[] = $option;
    }

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <select id="'.$this->id.'" class="input" '.$this->options.'>';

        foreach($this->optionList as $option){
            $option->render();
        }

        echo '</select>
            </div>';
    }
}

class InputOption{
    private $label;
    private $value;
    private $option;

    public function __construct($label, $value, $option=""){
        $this->label = $label;
        $this->value = $value;
        $this->option = $option;
    }

    public function render(){
        echo '<option '.$this->option.' value="'.$this->value.'">'.$this->label.'</option>';
    }
}

abstract class Button{
    protected $label;
    protected $type;
    protected $id;
    protected $size;

    protected $option;

    public function __construct($label, $option ="", $size = "", $type = "", $id = ""){
        $this->label = $label;
        $this->option = $option;
        $this->type = $type;
        $this->id = $id;
        if($size != ""){
            $this->size = "-".$size;
        }else{
            $this->size = "";
        }

        if($type != ""){
            $this->type = $type."-button";
        }else{
            $this->type = "";
        }
    }

    abstract public function render();

}

class LinkButton extends Button{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <a href="'.$this->option.'"><button class="input-button '.$this->type.'" id="'.$this->id.'">'.$this->label.'</button></a>
            </div>';
    }
}

class JSButton extends Button{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <button class="input-button '.$this->type.'" id="'.$this->id.'" '.$this->option.'>'.$this->label.'</button></a>
            </div>';
    }
}

class UploadButton extends Button{

    public function render(){
        echo '<div class="input-card settings-card'.$this->size.'">
                <input type="file" class="input-button '.$this->type.'" id="'.$this->id.'" '.$this->option.'>
            </div>';
    }
}

