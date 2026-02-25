<?php

require_once("dashboard.php");
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


$section = new Section("Order List");

$dashboardView->addSection($section);

$dashboardView->render();