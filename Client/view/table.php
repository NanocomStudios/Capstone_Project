<?php

class Table{
    private $rows = [];
    private $headRows = [];
    private $id;
    private $options;

    function __construct($id = "", $options=""){
        $this->id = $id;
        $this->options = $options;
    }

    public function addRow($row){
        $this->rows[] = $row;
    }

    public function addHeadRow($row){
    $this->headRows[] = $row;
    }

    public function render(){
        echo '<div class="table-container">
                <table class="data-table" ';

        if($this->id != ""){
            echo 'id="'.$this->id.'"';
        }

        echo ' '.$this->options.'>
            <thead>';

        foreach($this->headRows as $row){
            $row->render();
        }

        echo '</thead>
            <tbody>';

        foreach($this->rows as $row){
            $row->render();
        }

        echo '</tbody>
            </table>
            </div>';

    }
}

class TableRow{
    private $cols = [];
    private $id;
    private $options;

    public function __construct($id="", $options=""){
        $this->id = $id;
        $this->options = $options;
    }

    public function addCol($col){
        $this->cols[] = $col;
    }

    public function render(){
        echo '<tr';

        if($this->id != ""){
            echo ' id="'.$this->id.'"';
        }

        echo ' '.$this->options.'>';

        foreach($this->cols as $col){
            $col->render();
        }

        echo '</tr>';
    }
}

class TableCol{
    protected $data;
    protected $id;
    protected $options;

    public function __construct($data, $id="", $options=""){
        $this->data = $data;
        $this->id = $id;
        $this->options = $options;
    }

    public function render(){
        echo '<td';

        if($this->id != ""){
            echo ' id="'.$this->id.'"';
        }

        echo ' '.$this->options.'>'.$this->data.'</td>';
    }
}

class TableHead extends TableCol{
 
    public function render(){
        echo '<th';

        if($this->id != ""){
            echo ' id="'.$this->id.'"';
        }

        echo ' '.$this->options.'>'.$this->data.'</th>';
    }
}