<?php

class StatsCardSection{
    private $items = [];
    private $id;
    private $options;
    public function __construct($id="", $options=""){
        $this->id = $id;
        $this->options = $options;
    }

    public function addItem($item){
        $this->items[] = $item;
    }

    public function render(){
        echo '<div class="stats-grid" '.$this->options.'>';
        foreach ($this->items as $item){
            $item->render();
        }
        echo '</div>';
    }
}

class StatsCard{
    private $items = [];
    private $id;
    private $options;
    public function __construct($id="", $options=""){
        $this->id = $id;
        $this->options = $options;
    }

    public function addItem($item){
        $this->items[] = $item;
    }

    public function render(){
        echo '<div class="stat-card" '.$this->options.'>';
        foreach ($this->items as $item){
            $item->render();
        }
        echo '</div>';
    }
}

class ItemGrid{
    private $itemList = [];
    private $options;
    public function __construct($options = ''){
        $this->options = $options;
    }

    public function addItem($item){
        $this->itemList[] = $item;
    }

    public function render(){
        echo '<div class="item-grid" '.$this->options.'>';

        foreach($this->itemList as $item){
            $item->render();
        }

        echo '</div>';
    }
}

class ItemCard extends ItemGrid{
    private $itemList = [];
    private $options;
    public function __construct($options = ''){
        $this->options = $options;
    }

    public function addItem($item){
        $this->itemList[] = $item;
    }

    public function render(){
        echo '<div class="item-card" '.$this->options.'>';

        foreach($this->itemList as $item){
            $item->render();
        }

        echo '</div>';
    }
}

class ItemContent{
    private $itemList = [];
    private $options;
    public function __construct($options = ''){
        $this->options = $options;
    }

    public function addItem($item){
        $this->itemList[] = $item;
    }

    public function render(){
        echo '<div class="item-content" '.$this->options.'>';

        foreach($this->itemList as $item){
            $item->render();
        }

        echo '</div>';
    }
}