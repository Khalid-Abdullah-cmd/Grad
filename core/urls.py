from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    IndexView, FacultyListView, ProgramListView, ProgramDetailView,
    logout_view,
    DashboardHome,
    DashboardUniversityList, DashboardUniversityCreate, DashboardUniversityUpdate, DashboardUniversityDelete,
    DashboardFacultySelectUniversity, DashboardFacultyList, DashboardFacultyCreate, DashboardFacultyUpdate, DashboardFacultyDelete,
    DashboardProgramSelectUniversity, DashboardProgramSelectFaculty, DashboardProgramList, DashboardProgramCreate, DashboardProgramUpdate, DashboardProgramDelete,
)
from . import views

app_name = 'core'

urlpatterns = [
    # — Public Site —
    path('', IndexView.as_view(), name='index'),
    path('universities/<int:uni_id>/faculties/', FacultyListView.as_view(), name='faculty_list_public'),
    path('universities/<int:uni_id>/faculties/<int:fac_id>/programs/', ProgramListView.as_view(), name='program_list_public'),
    path('universities/<int:uni_id>/faculties/<int:fac_id>/programs/<int:prog_id>/', ProgramDetailView.as_view(), name='program_detail_public'),
    
    # -- about --
    path('about/', views.about_page, name='about'),
    
    # -- contact --
    path('contact/', views.contact_page, name='contact'),

    # — Authentication —
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    # — Dashboard Home —
    path('dashboard/', DashboardHome.as_view(), name='dashboard_home'),

    # — Universities CRUD —
    path('dashboard/universities/', DashboardUniversityList.as_view(), name='dashboard_uni_list'),
    path('dashboard/universities/add/', DashboardUniversityCreate.as_view(), name='dashboard_uni_add'),
    path('dashboard/universities/<int:pk>/edit/', DashboardUniversityUpdate.as_view(), name='dashboard_uni_edit'),
    path('dashboard/universities/<int:pk>/delete/', DashboardUniversityDelete.as_view(), name='dashboard_uni_delete'),

    # — Faculties CRUD —
    path('dashboard/faculties/select-university/', DashboardFacultySelectUniversity.as_view(), name='dashboard_faculty_select_university'),
    path('dashboard/faculties/<int:uni_id>/', DashboardFacultyList.as_view(), name='dashboard_faculty_list'),
    path('dashboard/faculties/<int:uni_id>/add/', DashboardFacultyCreate.as_view(), name='dashboard_faculty_add'),
    path('dashboard/faculties/<int:pk>/edit/', DashboardFacultyUpdate.as_view(), name='dashboard_faculty_edit'),
    path('dashboard/faculties/<int:pk>/delete/', DashboardFacultyDelete.as_view(), name='dashboard_faculty_delete'),

    # — Programs CRUD —
    path('dashboard/programs/select-university/', DashboardProgramSelectUniversity.as_view(), name='dashboard_program_select_university'),
    path('dashboard/programs/select-faculty/<int:uni_id>/', DashboardProgramSelectFaculty.as_view(), name='dashboard_program_select_faculty'),
    path('dashboard/programs/<int:fac_id>/', DashboardProgramList.as_view(), name='dashboard_program_list'),
    path('dashboard/programs/<int:fac_id>/add/', DashboardProgramCreate.as_view(), name='dashboard_program_add'),
    path('dashboard/programs/<int:pk>/edit/', DashboardProgramUpdate.as_view(), name='dashboard_program_edit'),
    path('dashboard/programs/<int:pk>/delete/', DashboardProgramDelete.as_view(), name='dashboard_program_delete'),
]