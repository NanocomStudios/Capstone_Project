<?php

require_once("dashboard.php");
require_once("input.php");
require_once("table.php");
require_once("cardGrid.php");

$dashboardHeader = new DashboardHeader();
$dashboardHeader->render();

$dashboardView = new DashboardView();

echo '<script>let sections = ["orderedSection", "packedSection", "shippedSection"];</script>';
echo '<script>let user = "'.$_COOKIE['uname'].'";</script>';

$section = new StatsCardSection();
$statCard = new StatsCard("", "onclick='showSection(\"orderedSection\")' style='cursor:pointer;'");
$statCard->addItem(new OtherObject('
    <div class="stat-icon">
        <i class="fas fa-users"></i>
    </div>
    <div class="stat-content">
        <h3>Ordered</h3>
        <div class="stat-number" id="orderedCount">2</div>
    </div>'));
$section->addItem($statCard);

$statCard = new StatsCard("", "onclick='showSection(\"packedSection\")' style='cursor:pointer;'");
$statCard->addItem(new OtherObject('
    <div class="stat-icon" >
        <i class="fas fa-users"></i>
    </div>
    <div class="stat-content">
        <h3>Packed</h3>
        <div class="stat-number" id="packedCount">3</div>
    </div>'));
$section->addItem($statCard);

$statCard = new StatsCard("", "onclick='showSection(\"shippedSection\")' style='cursor:pointer;'");
$statCard->addItem(new OtherObject('
    <div class="stat-icon" >
        <i class="fas fa-users"></i>
    </div>
    <div class="stat-content">
        <h3>Shipped</h3>
        <div class="stat-number" id="shippedCount">4</div>
    </div>'));
$section->addItem($statCard);

$dashboardView->addSection($section);


$section = new Section("Order List", "","style='display:none;' id='orderedSection'");
$subsection = new SubSection();

$subsection->addItem(new JSButton("New Order", "onclick='createOrder()'", "", "green", "createOrderButton"));
$section->addSubsection($subsection);

$table = new Table("orders", "id='ordersTable'");

$tr = new TableRow();
$tr->addCol(new TableCol("Order ID"));
$tr->addCol(new TableCol("Address"));
$tr->addCol(new TableCol("Status"));

$table->addRow($tr);

$section->addSubSection($table);
$dashboardView->addSection($section);


$section = new Section("Packed Order List", "","style='display:none;' id='packedSection'");
$subsection = new SubSection();

$table = new Table("orders", "id='ordersTable'");

$tr = new TableRow();
$tr->addCol(new TableCol("Order ID"));
$tr->addCol(new TableCol("Address"));
$tr->addCol(new TableCol("Status"));

$table->addRow($tr);

$section->addSubSection($table);
$dashboardView->addSection($section);


$section = new Section("Shipped Order List", "", "style='display:none;' id='shippedSection'");
$subsection = new SubSection();

$table = new Table("orders", "id='ordersTable'");

$tr = new TableRow();
$tr->addCol(new TableCol("Order ID"));
$tr->addCol(new TableCol("Address"));
$tr->addCol(new TableCol("Status"));

$table->addRow($tr);

$section->addSubSection($table);
$dashboardView->addSection($section);


$dashboardView->render();