<?php

require_once("view/dashboard.php");
$dashboardHeader = new DashboardHeader();
$dashboardHeader->render();

$dashboardView = new DashboardView();

$section = new Section("Package List");

$dashboardView->addSection($section);

$dashboardView->render();