from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('sp/<int:pk>/', views.sp_view, name="sp"),
    path('fp/<int:pk>/', views.fp_view, name="fp"),
    path('pie_chart/', views.pie_chart, name="chart"),
    # path('merge/<int:pk>/', views.merge_view, name="merge"),
    # path('pagetest/<int:pk>/', views.test_view, name="PageTest"),

    # REQUEST-SERVER
    path('request-server/', views.RequestServerView.as_view(), name="RequestServerList"),
    path('request-server/new/', views.request_server_new, name="RequestServerNew"),
    path('request-server/<int:pk>/approve/', views.request_server_approve, name="RequestServerApprove"),
    path('request-server/<int:pk>/send/', views.request_server_send, name="RequestServerSend"),
    path('request-server/<int:pk>/receive/', views.request_server_receive_document, name="RequestServerReceive"),
    path('request-server/approved/', views.request_server_approved, name="RequestServerApprovedList"),
    path('request-server/<int:pk>/set-pc', views.request_server_set_pc, name="RequestServerSetPc"),

    # ANTIVIRUS
    path('antivirus/', views.AntiVirusView.as_view(), name="AntiVirusList"),
    path('antivirus/new/', views.anti_virus_new, name="AntiVirusNew"),
    path('antivirus/<int:pk>/delete/', views.anti_virus_delete, name="AntiVirusDelete"),
    path('antivirus/<int:pk>/edit/', views.anti_virus_delete, name="AntiVirusEdit"),
    path('antivirus/requested/', views.AntiVirusView.as_view(), name="AntiVirusRequestedList"),

    # CUSTOMER
    path('customer/', views.CustomerListView.as_view(), name="CustomerList"),
    path('customer/new/', views.customer_new, name="CustomerNew"),
    path('customer/<int:pk>/edit/', views.customer_edit, name="CustomerEdit"),
    path('customer/<int:pk>/delete/', views.customer_delete, name="CustomerDelete"),

    # PRINCIPAL
    path('principal/', views.PrincipalListView.as_view(), name="PrincipalList"),
    path('principal/new/', views.principal_new, name="PrincipalNew"),
    path('principal/<int:pk>/edit/', views.principal_edit, name="PrincipalEdit"),
    path('principal/<int:pk>/delete/', views.principal_delete, name="PrincipalDelete"),

    # DISTRIBUTOR
    path('distributor/', views.DistributorListView.as_view(), name="DistributorList"),
    path('distributor/new/', views.distributor_new, name="DistributorNew"),
    path('distributor/<int:pk>/edit/', views.distributor_edit, name="DistributorEdit"),
    path('distributor/<int:pk>/delete/', views.distributor_delete, name="DistributorDelete"),

    # PC
    path('pc/', views.PcView.as_view(), name="PcList"),
    path('pc/<str:pk>/edit/', views.pc_edit, name="PcEdit"),
    path('pc/new/', views.pc_new, name="PcNew"),
    path('pc/<str:pk>/delete/', views.pc_delete, name="PcDelete"),

    # SSD
    path('ssd/', views.SsdView.as_view(), name="SsdList"),
    path('ssd/<str:pk>/edit/', views.ssd_edit, name="SsdEdit"),
    path('ssd/new/', views.ssd_new, name="SsdNew"),
    path('ssd/<str:pk>/delete/', views.ssd_delete, name="SsdDelete"),

    # HDD
    path('hdd/', views.HddView.as_view(), name="HddList"),
    path('hdd/<str:pk>/edit/', views.hdd_edit, name="HddEdit"),
    path('hdd/new/', views.hdd_new, name="HddNew"),
    path('hdd/<str:pk>/delete/', views.hdd_delete, name="HddDelete"),

    # PSU
    path('psu/', views.PsuView.as_view(), name="PsuList"),
    path('psu/<str:pk>/edit/', views.psu_edit, name="PsuEdit"),
    path('psu/new/', views.psu_new, name="PsuNew"),
    path('psu/<str:pk>/delete/', views.psu_delete, name="PsuDelete"),

    # RAM
    path('ram/', views.RamView.as_view(), name="RamList"),
    path('ram/<str:pk>/edit/', views.ram_edit, name="RamEdit"),
    path('ram/new/', views.ram_new, name="RamNew"),
    path('ram/<str:pk>/delete/', views.ram_delete, name="RamDelete"),
]
