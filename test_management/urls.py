from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', views.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:project_pk>/testsuites/create/', views.testsuite_create, name='testsuite_create'),
    path('testsuites/<int:pk>/', views.testsuite_detail, name='testsuite_detail'),
    path('testsuites/<int:pk>/update/', views.testsuite_update, name='testsuite_update'),
    path('testsuites/<int:pk>/delete/', views.testsuite_delete, name='testsuite_delete'),
    path('testsuites/<int:testsuite_pk>/testcases/create/', views.testcase_create, name='testcase_create'),
    path('testsuites/<int:testsuite_pk>/testcases/export/', views.testcase_export, name='testcase_export'),
    path('testsuites/<int:testsuite_pk>/testcases/import/', views.testcase_import, name='testcase_import'),
    path('testcases/<int:pk>/', views.testcase_detail, name='testcase_detail'),
    path('testcases/<int:pk>/update/', views.testcase_update, name='testcase_update'),
    path('testcases/<int:pk>/delete/', views.testcase_delete, name='testcase_delete'),
    path('testcases/<int:pk>/duplicate/', views.testcase_duplicate, name='testcase_duplicate'),
    path('testcases/<int:pk>/history/', views.testcase_history, name='testcase_history'),
    path('testcase-attachments/<int:pk>/delete/', views.testcase_attachment_delete, name='testcase_attachment_delete'),
    # テストプラン関連
    path('projects/<int:project_pk>/testplans/create/', views.testplan_create, name='testplan_create'),
    path('testplans/<int:pk>/', views.testplan_detail, name='testplan_detail'),
    path('testplans/<int:pk>/update/', views.testplan_update, name='testplan_update'),
    path('testplans/<int:pk>/delete/', views.testplan_delete, name='testplan_delete'),
    # テスト実行関連
    path('testplans/<int:testplan_pk>/testruns/create/', views.testrun_create, name='testrun_create'),
    path('testruns/<int:pk>/', views.testrun_detail, name='testrun_detail'),
    path('testruns/<int:pk>/update/', views.testrun_update, name='testrun_update'),
    path('testruns/<int:pk>/delete/', views.testrun_delete, name='testrun_delete'),
    path('testruns/<int:testrun_pk>/testcases/<int:testcase_pk>/results/create/', 
         views.testresult_create, name='testresult_create'),
    # 不具合関連
    path('testresults/<int:testresult_pk>/bugs/create/', views.bug_create, name='bug_create'),
    path('projects/<int:project_pk>/bugs/', views.project_bugs, name='project_bugs'),
    path('bugs/<int:pk>/', views.bug_detail, name='bug_detail'),
    path('bugs/<int:pk>/update/', views.bug_update, name='bug_update'),
    path('bugs/<int:pk>/delete/', views.bug_delete, name='bug_delete'),
] 