<?php

require_once("dashboard.php");


$dashboardHeader = new DashboardHeader();
$dashboardHeader->render();

$dashboardView = new DashboardView();

echo '<script>let sections = ["orderedSection", "deliverySection"];</script>';
echo '<script>let user = "'.$_COOKIE['uname'].'";</script>';
echo '<script src="view/js/client.js"></script>';

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

$statCard = new StatsCard("", "onclick='showSection(\"deliverySection\")' style='cursor:pointer;'");
$statCard->addItem(new OtherObject('
    <div class="stat-icon" >
        <i class="fas fa-users"></i>
    </div>
    <div class="stat-content">
        <h3>Deliveries</h3>
        <div class="stat-number" id="deliveryCount">3</div>
    </div>'));
$section->addItem($statCard);

$dashboardView->addSection($section);


$section = new Section("Order List", "","style='display:none;' id='orderedSection'");
$subsection = new SubSection();

$subsection->addItem(new JSButton("New Order", "onclick='showPopup(\"newOrderSection\")'", "", "green", "createOrderButton"));
$section->addSubsection($subsection);

$table = new Table("orderTable");

$tr = new TableRow();
$tr->addCol(new TableCol("Order ID"));
$tr->addCol(new TableCol("Customer"));
$tr->addCol(new TableCol("Address"));
$tr->addCol(new TableCol("Status"));

$table->addRow($tr);

$section->addSubSection($table);
$dashboardView->addSection($section);


$section = new Section("Packed Order List", "","style='display:none;' id='deliverySection'");
$subsection = new SubSection();

$table = new Table("deliveryTable");

$tr = new TableRow();
$tr->addCol(new TableCol("Order ID"));
$tr->addCol(new TableCol("Address"));
$tr->addCol(new TableCol("Client"));
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

$dashboardView->addSection(new PopupOverlay());

$section = new Section("New Order", "popup-l", "style='display:none;' id='newOrderSection'");
$subsection = new SubSection();

$subsection->addItem(new InputText("Customer Name", "long", "customerNameInput"));
$subsection->addItem(new InputText("Delivery Address", "long", "deliveryAddressInput"));
$subsection->addItem(new JSButton("Submit Order", "onclick='submitOrder()'", "", "green", "submitOrderButton"));
$subsection->addItem(new JSButton("Cancel", "onclick='hidePopup(\"newOrderSection\")'", "", "red", "cancelOrderButton"));
$section->addSubSection($subsection);
$dashboardView->addSection($section);

$dashboardView->render();