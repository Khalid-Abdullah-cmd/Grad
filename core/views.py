from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .models import University, Faculty, Program, Job
from .forms import JobFormSet

# --- Superuser Mixin ---

class SuperuserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# --- Public Views ---

class IndexView(ListView):
    model = University
    template_name = 'core/index.html'
    context_object_name = 'unis'

class FacultyListView(TemplateView):
    template_name = 'core/faculty_list_public.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        uni = get_object_or_404(University, pk=kwargs['uni_id'])
        ctx.update({
            'university': uni,
            'facs': uni.faculties.all(),
        })
        return ctx
    
    

# -- login --



class ProgramListView(TemplateView):
    template_name = 'core/program_list_public.html'

    def get_context_data(self, **kwargs):
        uni = get_object_or_404(University, pk=kwargs['uni_id'])
        fac = get_object_or_404(Faculty, pk=kwargs['fac_id'], university=uni)
        return {
            'university': uni,
            'faculty': fac,
            'progs': fac.programs.all(),
        }

class ProgramDetailView(TemplateView):
    template_name = 'core/program_detail_public.html'

    def get_context_data(self, **kwargs):
        uni = get_object_or_404(University, pk=kwargs['uni_id'])
        fac = get_object_or_404(Faculty, pk=kwargs['fac_id'], university=uni)
        prog = get_object_or_404(Program, pk=kwargs['prog_id'], faculty=fac)
        return {
            'university': uni,
            'faculty': fac,
            'program': prog,
            'jobs': prog.jobs.all(),
        }

def logout_view(request):
    logout(request)
    return redirect('core:index')

# --- Dashboard Home ---

class DashboardHome(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'core/dashboard_home.html'

# --- Dashboard: Universities CRUD ---

class DashboardUniversityList(LoginRequiredMixin, SuperuserRequiredMixin, View):
    def get(self, request):
        universities = University.objects.all()
        return render(request, 'core/uni_CRUD.html', {'universities': universities})

class DashboardUniversityCreate(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = University
    fields = ['name']
    template_name = 'core/uni_form.html'
    success_url = reverse_lazy('core:dashboard_uni_list')

class DashboardUniversityUpdate(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = University
    fields = ['name']
    template_name = 'core/uni_form.html'
    success_url = reverse_lazy('core:dashboard_uni_list')

class DashboardUniversityDelete(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = University
    template_name = 'core/uni_confirm_delete.html'
    success_url = reverse_lazy('core:dashboard_uni_list')

# --- Dashboard: Faculties CRUD ---

class DashboardFacultySelectUniversity(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'core/faculty_select_university.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['universities'] = University.objects.all()
        return context

class DashboardFacultyList(LoginRequiredMixin, SuperuserRequiredMixin, View):
    def get(self, request, uni_id):
        university = get_object_or_404(University, pk=uni_id)
        faculties = university.faculties.all()
        return render(request, 'core/faculty_CRUD.html', {
            'university': university,
            'faculties': faculties,
        })
class DashboardFacultyCreate(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Faculty
    fields = ['name']  # Only include 'name', exclude 'university'
    template_name = 'core/faculty_form.html'

    def form_valid(self, form):
        uni_id = self.kwargs.get('uni_id')  # Get university ID from URL
        if uni_id:
            form.instance.university = get_object_or_404(University, pk=uni_id)  # Set university
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:dashboard_faculty_list', kwargs={'uni_id': self.object.university.id})

class DashboardFacultyUpdate(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Faculty
    fields = ['name']  # Only include 'name', exclude 'university'
    template_name = 'core/faculty_form.html'

    def get_success_url(self):
        return reverse('core:dashboard_faculty_list', kwargs={'uni_id': self.object.university.id})


class DashboardFacultyDelete(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Faculty
    template_name = 'core/faculty_confirm_delete.html'

    def get_success_url(self):
        return reverse('core:dashboard_faculty_list', kwargs={'uni_id': self.object.university.id})

# --- Dashboard: Programs CRUD ---


class DashboardProgramSelectUniversity(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'core/program_select_university.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['universities'] = University.objects.all()
        return context

class DashboardProgramSelectFaculty(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'core/program_select_faculty.html'

    def get_context_data(self, **kwargs):
        university = get_object_or_404(University, pk=kwargs['uni_id'])
        return {
            'university': university,
            'faculties': university.faculties.all(),
        }

class DashboardProgramList(LoginRequiredMixin, SuperuserRequiredMixin, View):
    def get(self, request, fac_id):
        faculty = get_object_or_404(Faculty, pk=fac_id)
        programs = faculty.programs.all()
        return render(request, 'core/program_CRUD.html', {
            'faculty': faculty,
            'programs': programs,
        })
class DashboardProgramCreate(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Program
    fields = ['name', 'content', 'description', 'link']  # Exclude 'faculty'
    template_name = 'core/program_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(self.request.POST, instance=self.object)
        else:
            context['job_formset'] = JobFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        fac_id = self.kwargs.get('fac_id')
        if fac_id:
            form.instance.faculty = get_object_or_404(Faculty, pk=fac_id)
        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('core:dashboard_program_list', kwargs={'fac_id': self.object.faculty.id})


class DashboardProgramUpdate(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Program
    fields = ['name', 'content', 'description', 'link']  # Exclude 'faculty'
    template_name = 'core/program_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(self.request.POST, instance=self.object)
        else:
            context['job_formset'] = JobFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('core:dashboard_program_list', kwargs={'fac_id': self.object.faculty.id})


class DashboardProgramDelete(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Program
    template_name = 'core/program_confirm_delete.html'

    def get_success_url(self):
        return reverse('core:dashboard_program_list', kwargs={'fac_id': self.object.faculty.id})
    
    
    
# about page

def about_page(request):
    unis = University.objects.all()
    return render(request, 'core/about.html', {
        'unis': unis,
    })

def contact_page(request):
    unis = University.objects.all()
    return render(request, 'core/contact.html', {
        'unis': unis,
    })