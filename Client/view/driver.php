<?php

require_once("view/dashboard.php");
$dashboardHeader = new DashboardHeader();
$dashboardHeader->render();

$dashboardView = new DashboardView();

$section = new Section("Order List");

$dashboardView->addSection($section);

$dashboardView->render();