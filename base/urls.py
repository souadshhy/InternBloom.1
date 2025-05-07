from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [



    path('login', views.UserLogin.as_view(), name='login'),

    path('logout', LogoutView.as_view(next_page='login'), name='logout'),

    path('register/', views.RegisterPage.as_view(), name='register'),

    path('apps_list', views.Apps_list.as_view(),
         name='apps'),

    path('apps_list/apps_detail/<int:pk>/', views.Apps_detail.as_view(),
         name='app_detail'),

    path('apps_list/apps_create',
         views.Apps_create.as_view(), name='app_create'),

    # Note!!!
    path('apps_list/apps_create/<int:position_id>/<int:company_id>/',
         views.Apps_create_filtered.as_view(), name='app_create_filtered'),



    path('apps_list/apps_update/<int:pk>/', views.Apps_update.as_view(),
         name='app_update'),

    path('apps_list/app_delete/<int:pk>',
         views.Apps_delete.as_view(), name='app_delete'),

    path('positions_list', views.Positions_list.as_view(),
         name='positions'),

    path('positions_list/position_detail/<int:pk>/', views.Position_detail.as_view(),
         name='position_detail'),

    path('companies_list/position_create/',
         views.Position_create.as_view(), name='position_create'),

    path('companies_list/position_create/<int:company_id>/',
         views.Position_create_filtered.as_view(), name='position_create_filterd'),


    path('positions_list/position_update/<int:pk>/', views.Position_update.as_view(),
         name='position_update'),

    path('positions_list/position_delete/<int:pk>',
         views.Position_delete.as_view(), name='position_delete'),

    path('companies_list', views.Company_list.as_view(),
         name='companies'),

    path('companies_list/company_detail/<int:pk>/', views.Company_detail.as_view(),
         name='company_detail'),

    path('companies_list/company_create/',
         views.Company_create.as_view(), name='company_create'),

    path('companies_list/company_update/<int:pk>/', views.Company_update.as_view(),
         name='company_update'),

    path('companies_list/company_delete/<int:pk>/',
         views.Company_delete.as_view(), name='company_delete'),



    #     CompanyApplications & CompanyPositions

    path('companies_list/<int:pk>/positions',
         views.CompanyPosition_list.as_view(), name='company_positions'),

    path('companies_list/<int:pk>/apps',
         views.CompanyApps_list.as_view(), name='company_apps'),




    path('students_list', views.Student_list.as_view(),
         name='students'),

    path('students_list/student_detail/<int:pk>/',
         views.Student_detail.as_view(), name='student_detail'),

    path('students_list/student_create/', views.Student_create.as_view(),
         name='student_create'),

    path('students_list/student_update/<int:pk>/', views.Student_update.as_view(),
         name='student_update'),

    path('students_list/student_delete/<int:pk>/', views.Student_delete.as_view(),
         name='student_delete'),


    path('departs_list', views.Depart_list.as_view(),
         name='departs'),

    path('departs_list/depart_detail/<int:pk>/',
         views.Depart_detail.as_view(), name='depart_detail'),

    path('departs_list/depart_create/', views.Depart_create.as_view(),
         name='depart_create'),

    path('departs_list/depart_update/<int:pk>/',
         views.Depart_update.as_view(), name='depart_update'),

    path('departs_list/depart_delete/<int:pk>/',
         views.Depart_delete.as_view(), name='depart_delete'),

    # ---------------------------------------------
    # reports path

    path("reports/<str:report_name>/", views.Reports.as_view(), name="reports"),
]
