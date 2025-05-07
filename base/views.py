
from django import forms
from django.db.models import Q

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from . import models
from . import reports


class UserLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('apps')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('apps')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('apps')
        return super(RegisterPage, self).get(*args, **kwargs)


class Apps_list(LoginRequiredMixin, ListView):
    model = models.Apps
    context_object_name = 'apps'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apps'] = context['apps'].filter(user=self.request.user)
        context['count'] = context['apps'].count()

        search_input = self.request.GET.get('searchArea') or ''
        if search_input:
            context['apps'] = context['apps'].filter(
                student__name__startswith=search_input)

            context['search_input'] = search_input
        return context


class Apps_detail(LoginRequiredMixin, DetailView):
    model = models.Apps
    context_object_name = 'apps'


class Apps_create(LoginRequiredMixin, CreateView):
    model = models.Apps
    fields = ['student', 'company', 'position', 'appStatus']
    success_url = reverse_lazy('apps')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Apps_create, self).form_valid(form)


class Apps_create_filtered(LoginRequiredMixin, CreateView):
    model = models.Apps
    fields = ['student', 'appStatus']

    def dispatch(self, request, *args, **kwargs):
        position = models.Position.objects.get(pk=self.kwargs['position_id'])

        if not position.available:
            return redirect('company_positions')

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['position'] = self.kwargs["position_id"]
        initial['company'] = self.kwargs["company_id"]
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.position = models.Position.objects.get(
            pk=self.kwargs['position_id'])

        form.instance.company = models.Company.objects.get(
            pk=self.kwargs['company_id'])

        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['appStatus'].widget.attrs['class'] = 'form-select'
        return form

    def get_success_url(self):
        return reverse_lazy('company_positions', kwargs={'pk': self.kwargs['company_id']})


class Apps_update(LoginRequiredMixin, UpdateView):
    model = models.Apps
    fields = ['student', 'company', 'position', 'appStatus']
    success_url = reverse_lazy('apps')


class Apps_delete(LoginRequiredMixin, DeleteView):
    model = models.Apps
    context_object_name = 'app'
    success_url = reverse_lazy('apps')


class Positions_list(LoginRequiredMixin, ListView):
    model = models.Position
    context_object_name = 'positions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = context['positions'].filter(
            user=self.request.user)
        context['count'] = context['positions'].filter().count()

        search_input = self.request.GET.get('searchArea') or ''
        if search_input:
            context['positions'] = context['positions'].filter(
                company__companyName__startswith=search_input)

            context['search_input'] = search_input
        return context


class Position_detail(LoginRequiredMixin, DetailView):
    model = models.Position
    context_object_name = 'position'


class Position_create(LoginRequiredMixin, CreateView):
    model = models.Position
    fields = ['title', 'company', 'duration', 'location', 'paid', 'available']
    template_name = 'base/position_form.html'
    success_url = reverse_lazy("positions")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Position_create, self).form_valid(form)


class Position_create_filtered(LoginRequiredMixin, CreateView):
    model = models.Position
    fields = ['title', 'duration', 'location', 'paid']
    template_name = 'base/position_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['company'] = self.kwargs["company_id"]
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company = models.Company.objects.get(
            pk=self.kwargs['company_id']
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('company_positions', kwargs={'pk': self.kwargs['company_id']})


class Position_update(LoginRequiredMixin, UpdateView):
    model = models.Position
    fields = ['title', 'company', 'duration', 'location', 'paid']
    success_url = reverse_lazy('positions')


class Position_delete(LoginRequiredMixin, DeleteView):
    model = models.Position
    context_object_name = 'position'
    success_url = reverse_lazy('positions')


class Company_list(LoginRequiredMixin, ListView):
    model = models.Company
    context_object_name = 'companies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = context['companies'].filter(
            user=self.request.user)
        context['count'] = context['companies'].count()

        search_input = self.request.GET.get('searchArea') or ''
        if search_input:
            context['companies'] = context['companies'].filter(
                companyName__startswith=search_input)

            context['search_input'] = search_input
        return context


class Company_detail(LoginRequiredMixin, DetailView):
    model = models.Company
    context_object_name = 'companies'


class Company_create(LoginRequiredMixin, CreateView):
    model = models.Company
    fields = ['companyName', 'sector', 'industry']
    success_url = reverse_lazy('companies')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Company_create, self).form_valid(form)


class Company_update(LoginRequiredMixin, UpdateView):
    model = models.Company
    fields = ['companyName', 'sector', 'industry']
    success_url = reverse_lazy('companies')


class Company_delete(LoginRequiredMixin, DeleteView):
    model = models.Company
    template_name = "base\company_confirm_delete.html"
    context_object_name = 'companies'
    success_url = reverse_lazy('companies')

# ----------------------------------------------------------------------------------------
#     CompanyApplications & CompanyPositions


class CompanyPosition_list(LoginRequiredMixin, ListView):
    model = models.Position
    template_name = "base/company_positions_filtered.html"
    context_object_name = "positions"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, available=True, company__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = models.Company.objects.get(pk=self.kwargs['pk'])
        return context


class CompanyApps_list(LoginRequiredMixin, ListView):
    model = models.Apps
    template_name = "base/company_apps_filtered.html"
    context_object_name = "apps"

    def get_queryset(self):
        queryset = self.model.objects.filter(
            user=self.request.user, company__id=self.kwargs['pk'])
        search_input = self.request.GET.get('searchArea') or ''
        if search_input:
            queryset = queryset.filter(student__name__startswith=search_input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = models.Company.objects.get(pk=self.kwargs['pk'])
        context['search_input'] = self.request.GET.get('searchArea') or ''
        return context


class Student_list(LoginRequiredMixin, ListView):
    model = models.Student
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Always define 'students' first
        students = self.model.objects.filter(user=self.request.user)

        # Get search input from query parameters
        search_input = self.request.GET.get('searchArea') or ''

        if search_input:
            if search_input.isdigit():
                # If search is numeric, filter by ID
                students = students.filter(id=int(search_input))
            else:
                # Otherwise, optionally search by name/surname
                students = students.filter(
                    Q(name__icontains=search_input) |
                    Q(surname__icontains=search_input)
                )
            context['search_input'] = search_input

        # Set the final filtered queryset
        context['students'] = students
        context['count'] = students.count()

        return context


class Student_detail(LoginRequiredMixin, DetailView):
    model = models.Student
    context_object_name = 'student'


class Student_create(LoginRequiredMixin, CreateView):
    model = models.Student
    fields = ['name', 'surname', "department", "major", "year"]
    success_url = reverse_lazy('students')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Student_create, self).form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['year'].widget = forms.DateInput(attrs={'type': 'date'})
        return form


class Student_update(LoginRequiredMixin, UpdateView):
    model = models.Student
    fields = ['name', 'surname', "department", "major", "year"]
    success_url = reverse_lazy('students')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['year'].widget = forms.DateInput(attrs={'type': 'date'})
        return form


class Student_delete(LoginRequiredMixin, DeleteView):
    model = models.Student
    context_object_name = 'student'
    success_url = reverse_lazy('students')


class Depart_list(LoginRequiredMixin, ListView):
    model = models.Depart
    context_object_name = 'departs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departs'] = context['departs'].filter(
            user=self.request.user)
        context['count'] = context['departs'].count()

        search_input = self.request.GET.get('searchArea') or ''
        if search_input:
            context['departs'] = context['departs'].filter(
                deptName__startswith=search_input)

            context['search_input'] = search_input
        return context


class Depart_detail(LoginRequiredMixin, DetailView):
    model = models.Depart
    context_object_name = 'depart'


class Depart_create(LoginRequiredMixin, CreateView):
    model = models.Depart
    fields = ['deptName']
    success_url = reverse_lazy('departs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Depart_create, self).form_valid(form)


class Depart_update(LoginRequiredMixin, UpdateView):
    model = models.Depart
    fields = ['deptName']
    success_url = reverse_lazy('departs')


class Depart_delete(LoginRequiredMixin, DeleteView):
    model = models.Depart
    context_object_name = 'depart'
    success_url = reverse_lazy('departs')

# ------------------------------------------------------------------------------
# reports view


class Reports(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        report_name = self.kwargs.get('report_name')
        if report_name == 'most_applied_positions':
            return ['base/apps_per_position.html']

        elif report_name == 'available_positions':
            return ['base/available_positions.html']

        elif report_name == 'apps_per_company':
            return ['base/apps_per_company.html']

        elif report_name == 'activity_of_student_per_month':
            return ['base/activity_of_student_per_month.html']

        elif report_name == 'acceptance_per_company':
            return ['base/acceptance_per_company.html']

        return ['base/reports.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_name = self.kwargs.get('report_name')

        report_map = {
            'most_applied_positions': reports.report_total_applications_per_position,
            'available_positions': reports.report_available_positions,
            'apps_per_company': reports.report_apps_per_company,
            'activity_of_student_per_month': reports.report_activity_of_student_per_month,
            'acceptance_per_company': reports.report_acceptance_per_company,
        }

        if report_name in report_map:
            context['report_data'] = report_map[report_name]()
            context['report_name'] = report_name.replace('_', ' ').title()
        else:
            context['error'] = 'No such report.'

        return context
