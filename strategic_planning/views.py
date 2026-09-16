from datetime import date, datetime 
from django.db.models import Q, Sum, QuerySet 
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import (
    MainActivity, Report, StrategicTheme, StrategicObjective, Designation, KPI,
    Activity, User, Role
)
from .forms import ( ActivityForm, KPIForm, LoginForm, MainActivityForm, StrategicObjectiveForm, StrategicThemeForm, ReportForm, UserForm, RoleForm, DesignationForm, )
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from collections import defaultdict

from django.http import FileResponse
# Create your views here.

class RoleAndDesignationRequiredMixin(LoginRequiredMixin):
    required_role = None  # Set the required role in the view
    required_designation = None  # Set the required designation in the view

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated (handled by LoginRequiredMixin)
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Check for the required role
        if self.required_role and (not request.user.role or request.user.role.name != self.required_role):
            raise PermissionDenied("You do not have the required role to access this page.")

        # Check for the required designation
        if self.required_designation and (
            not request.user.designation or request.user.designation.name != self.required_designation
        ):
            raise PermissionDenied("You do not have the required designation to access this page.")

        return super().dispatch(request, *args, **kwargs)

from django.db.models import Case, When, Value, IntegerField, F, Sum, Count

class HomeView(RoleAndDesignationRequiredMixin, TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        # Fetch logged-in user and designation
        user = self.request.user
        role = user.role.name
        designations = user.designation.all()
        
        if designations.exists():
            if role == "Elder":
                current_designation = user.designation.all()
            else:
                current_designation = user.designation.first()
        else:
            current_designation = None
        
        # Initialize context
        context = super().get_context_data(**kwargs)

        # Get today's date, current year, and quarter
        today = date.today()
        current_year = today.year
        current_quarter = (today.month - 1) // 3 + 1

        # Fetch activities for the current designation
        if role == "Admin":
            activities = Activity.objects.all()
        elif isinstance(current_designation, QuerySet):
            activities = Activity.objects.filter(designation__in=current_designation.values_list('id', flat=True))
        else:
            activities = Activity.objects.filter(designation=current_designation)
        # Calculate total planned budget and number of activities
        planned_budget_quarter = activities.filter(
            start_date__year=current_year,
            start_date__quarter=current_quarter
        ).aggregate(total=Sum('estimated_amount'))['total'] or 0

        planned_budget_year = activities.filter(
            start_date__year=current_year
        ).aggregate(total=Sum('estimated_amount'))['total'] or 0

        num_activities_quarter = activities.filter(
            start_date__year=current_year,
            start_date__quarter=current_quarter
        ).count()
        num_activities_budget = activities.count()

        # Fetch reported activities and actual spent for the current designation
        if role == "Admin":
            reports = Report.objects.all()
        elif isinstance(current_designation, QuerySet):
            reports = Report.objects.filter(designation__in=current_designation.values_list('id', flat=True))
        else:    
            reports = Report.objects.filter(designation=current_designation)

        reported_activities_quarter = reports.filter(
            report_date__year=current_year,
            report_date__quarter=current_quarter
        )
        completed_activities_quarter =reported_activities_quarter.filter(
            goal_score = 'green'
        ).count()
        failed_activities_quarter =reported_activities_quarter.filter(
            goal_score = 'red'
        ).count()
        reports_quarter_percentage = int(((completed_activities_quarter) / (num_activities_quarter)) * 100 ) if num_activities_quarter > 0 else 0
        failed_quarter_percentage =int((failed_activities_quarter / num_activities_quarter) * 100 ) if num_activities_quarter > 0 else 0
        actual_spent_quarter = reported_activities_quarter.aggregate(
            total=Sum('actual_spent')
        )['total'] or 0

        actual_spent_year = reports.filter(
            report_date__year=current_year
        ).aggregate(total=Sum('actual_spent'))['total'] or 0

        # Activities with their scores for the current quarter (convert goal_score to numeric)
        activities_with_scores = reported_activities_quarter.annotate(
            numeric_goal_score=Case(
                When(goal_score='green', then=Value(100)),
                When(goal_score='orange', then=Value(75)),
                When(goal_score='yellow', then=Value(25)),
                When(goal_score='red', then=Value(0)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).values(
            activity_name=F('activity__name'),
            numeric_score=F('numeric_goal_score'),  # Avoid conflict by renaming
            report_on=F('report_date')
        )

        # Calculate average goal score for the current quarter
        average_goal_score = reported_activities_quarter.annotate(
            numeric_goal_score=Case(
                When(goal_score='green', then=Value(100)),
                When(goal_score='orange', then=Value(75)),
                When(goal_score='yellow', then=Value(25)),
                When(goal_score='red', then=Value(0)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).aggregate(average=Sum('numeric_goal_score'))['average'] or 0

        # Fetch all strategic themes
        strategic_themes = StrategicTheme.objects.all()

        # Prepare progress data for each theme
        themes_progress = []
        total_created_activities = 0
        total_reported_activities = 0
        
        for theme in strategic_themes:
            # Total activities for the theme
            created_activities = activities.filter(
                kpi__strategic_objective__strategic_theme=theme,
                start_date__year=current_year
            ).count()

            # Reported activities for the theme
            reported_activities = reports.filter(
                activity__kpi__strategic_objective__strategic_theme=theme,
                report_date__year=current_year
            ).count()
            # Progress percentage
            progress = (reported_activities / created_activities * 100) if created_activities > 0 else 0

            # Add to totals
            total_created_activities += created_activities
            total_reported_activities += reported_activities

            # Append to themes progress list
            themes_progress.append({
                'theme': theme.theme_name,
                'created_activities': created_activities,
                'reported_activities': reported_activities,
                'progress': round(progress, 2),
            })

        # Overall progress percentage
        overall_progress = (total_reported_activities / total_created_activities * 100) if total_created_activities > 0 else 0
        
        # Fetch activities for the current quarter with status 0
        if role == "Admin":
            sub_activities = Activity.objects.filter(
                start_date__year=current_year,
                start_date__quarter=current_quarter,
                status=0
            ).order_by('start_date')[:5]
        elif role == "Elder":
            sub_activities = Activity.objects.filter(
                start_date__year=current_year,
                start_date__quarter=current_quarter,
                status=0
            ).order_by('start_date')[:5]
        else:
            sub_activities = Activity.objects.filter(
                designation=current_designation,
                start_date__year=current_year,
                start_date__quarter=current_quarter,
                status=0
            ).order_by('start_date')[:5]
             
        # Count activities by goal_score
        goal_score_counts = reported_activities_quarter.values('goal_score').annotate(count=Count('goal_score'))
        goal_score_data = {item['goal_score']: item['count'] for item in goal_score_counts}

        # Ensure all statuses are represented in the data
        chart_data = {
            'green': goal_score_data.get('green', 0),
            'orange': goal_score_data.get('orange', 0),
            'yellow': goal_score_data.get('yellow', 0),
            'red': goal_score_data.get('red', 0),
        }
        print(chart_data)
        # Populate context
        context.update({
            'username': user.first_name,
            'themes_progress': themes_progress,
            'overall_progress': round(overall_progress, 2),
            'total_created_activities': total_created_activities,
            'total_reported_activities': total_reported_activities,
            'planned_budget_quarter': planned_budget_quarter,
            'planned_budget_year': planned_budget_year,
            'num_activities_budget': num_activities_budget,
            'num_activities_quarter': num_activities_quarter,
            'reported_activities_count': reported_activities_quarter.count(),
            'actual_spent_quarter': actual_spent_quarter,
            'actual_spent_year': actual_spent_year,
            'activities_with_scores': list(activities_with_scores),
            'average_goal_score': round(average_goal_score, 2),
            'sub_activities' : sub_activities,
            'completed_activities_quarter' : completed_activities_quarter,
            'failed_activities_quarter' : failed_activities_quarter,
            'failed_quarter_percentage' : failed_quarter_percentage,
            'reports_quarter_percentage' : reports_quarter_percentage, 
            'chart_data': chart_data,
        })

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

class StrategicThemeListView(RoleAndDesignationRequiredMixin, ListView):
    model = StrategicTheme
    template_name = 'strategic_themes.html'
    context_object_name = 'strategic_themes'

class StrategicThemeCreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = StrategicTheme
    form_class = StrategicThemeForm
    template_name = 'forms.html'
    success_url = reverse_lazy('strategic_themes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'strategic_theme_create'  # Set this for conditional rendering
        return context
    
class StrategicThemeDetailView(DetailView):
    model = StrategicTheme
    template_name = 'strategic_theme_detail.html'
    context_object_name = 'strategic_theme'

class StrategicThemeUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = StrategicTheme
    form_class = StrategicThemeForm
    template_name = 'forms.html'  # Your form template
    success_url = reverse_lazy('strategic_themes')  # Redirect after saving

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'strategic_theme_update'
        return context
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user
        return super().form_valid(form)

class StrategicThemeDeleteView(RoleAndDesignationRequiredMixin, DeleteView):
    model = StrategicTheme
    template_name = 'strategic_theme_confirm_delete.html'
    success_url = reverse_lazy('strategic_theme_list')

#strategic objectives views 
class StrategicObjectiveListView(RoleAndDesignationRequiredMixin, ListView):
    model = StrategicObjective
    
    required_role = 'Admin'
    template_name = 'strategic_objectives.html'
    context_object_name = 'strategic_objectives'


class StrategicObjectiveDetailView(DetailView):
    model = StrategicObjective
    template_name = 'strategic_objective_detail.html'
    context_object_name = 'strategic_objective'


class StrategicObjectiveCreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = StrategicObjective
    required_role = 'Admin'
    form_class = StrategicObjectiveForm
    template_name = 'forms.html'
    success_url = reverse_lazy('strategic_objectives')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'strategic_objective_create'  # Set this for conditional rendering
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user
        return super().form_valid(form)

class StrategicObjectiveUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = StrategicObjective
    form_class = StrategicObjectiveForm
    template_name = 'forms.html'
    success_url = reverse_lazy('strategic_objectives')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'strategic_objective_update'  # Set this for conditional rendering
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user  
        return super().form_valid(form)

class StrategicObjectiveDeleteView(DeleteView):
    model = StrategicObjective
    template_name = 'strategic_objective_confirm_delete.html'
    success_url = reverse_lazy('strategic_objective_list')


class DesignationDeleteView(DeleteView):
    model = Designation
    template_name = 'designation_confirm_delete.html'
    success_url = reverse_lazy('designation_list')

#KPI Views
class KPIListView(RoleAndDesignationRequiredMixin, ListView):
    model = KPI
    template_name = 'kpi_list.html'
    context_object_name = 'kpis'


class KPIDetailView(DetailView):
    model = KPI
    template_name = 'kpi_detail.html'
    context_object_name = 'kpi'

class KPICreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = KPI
    form_class = KPIForm
    template_name = 'forms.html'
    success_url = reverse_lazy('kpi_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'kpi_create'  # Set this for conditional rendering
        return context
    
    def form_valid(self, form):
        # Handle multiple KPIs
        kpi_names = self.request.POST.getlist('kpi_name')
        strategic_objective = form.cleaned_data['strategic_objective']
        for kpi_name in kpi_names:
            if kpi_name.strip():  # Ensure the KPI name is not empty
                KPI.objects.create(
                    name=kpi_name,
                    strategic_objective=strategic_objective,
                    created_by=self.request.user
                )
        return redirect(self.success_url)

class KPIUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = KPI
    form_class = KPIForm
    template_name = 'forms.html'
    success_url = reverse_lazy('kpi_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'kpi_update'  # Set this for conditional rendering
        return context

class KPIDeleteView(DeleteView):
    model = KPI
    template_name = 'kpi_confirm_delete.html'
    success_url = reverse_lazy('kpi_list')


    
# Activity Views
class ActivityListView(RoleAndDesignationRequiredMixin, ListView):
    model = Activity
    template_name = 'activities.html'
    context_object_name = 'activities'


class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity_detail.html'
    context_object_name = 'activity'


class ActivityCreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'forms.html'
    success_url = reverse_lazy('activity_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'activity_create'  # Set this for conditional rendering
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user
        return super().form_valid(form)
    

class ActivityUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'forms.html'
    success_url = reverse_lazy('activity_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'activity_update'  # Set this for conditional rendering
        return context
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user
        return super().form_valid(form)
    

class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activity_confirm_delete.html'
    success_url = reverse_lazy('activity_list')


    
class DesignationListView(RoleAndDesignationRequiredMixin, ListView):
    model = Designation
    template_name = 'designations.html'
    context_object_name = 'designations'


class DesignationDetailView(DetailView):
    model = Designation
    template_name = 'designation_detail.html'
    context_object_name = 'designation'


class DesignationCreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = Designation
    form_class = DesignationForm
    template_name = 'forms.html'
    success_url = reverse_lazy('designation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'designation_create'  # Set this for conditional rendering
        return context


class DesignationUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = Designation
    form_class = DesignationForm
    template_name = 'forms.html'
    success_url = reverse_lazy('designation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'designation_update'  # Set this for conditional rendering
        return context


class ReportDetailView(DetailView):
    model = Report
    template_name = 'report_detail.html'
    context_object_name = 'report'



class ReportUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'forms.html'
    success_url = reverse_lazy('report_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'report_update'  # Set this for conditional rendering
        return context

class RoleListView(RoleAndDesignationRequiredMixin, ListView):
    model = Role
    template_name = 'roles.html'
    context_object_name = 'roles'


class RoleDetailView(DetailView):
    model = Role
    template_name = 'role_detail.html'
    context_object_name = 'role'


class RoleCreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = Role
    required_role = "Admin"
    form_class = RoleForm
    template_name = 'forms.html'
    success_url = reverse_lazy('role_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'role_create'  # Set this for conditional rendering
        return context

class RoleUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'forms.html'
    success_url = reverse_lazy('role_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'role_update'  # Set this for conditional rendering
        return context

class UserListView(RoleAndDesignationRequiredMixin, ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'  # Pass the users to the template
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(role__name__icontains=query) |
                Q(designation__name__icontains=query)
            ).distinct()
        return queryset

class UserCreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'forms.html'
    success_url = reverse_lazy('user_list')  # Redirect to the user list after creation
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'user_create'  # Set this for conditional rendering
        return context
    
    def form_valid(self, form):
        """
        Hash the password before saving the user.
        """
        user = form.save(commit=False)
        if user.password:  # Hash password before saving
            user.set_password(form.cleaned_data['password'])
        user.save()
        form.save_m2m() 
        return super().form_valid(form)

class UserUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'forms.html'
    success_url = reverse_lazy('user_list')  # Redirect to the user list after update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'user_update'  # Set this for conditional rendering
        return context
    
    def form_valid(self, form):
        """
        Hash the password before saving the user.
        """
        user = form.save(commit=False)
        if user.password:  # Hash password before saving
            user.set_password(form.cleaned_data['password'])
        user.save()
        form.save_m2m()  # Save Many-to-Many relationships
        return super().form_valid(form)

class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data["username"]  # This now represents email
            password = form.cleaned_data["password"]
            print(f"Trying to authenticate user with email: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Authentication successful!")
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Please enter correct email and password.")
        return render(request, self.template_name, {"form": form})

def permission_denied(request, exception=None):
    return render(request, "403.html", status=403)

def dashboard(request):
    roles = request.user.groups.values_list('name', flat=True) if request.user.groups.exists() else []
    context = {
        'roles': roles
    }
    return render(request, 'home.html', context)


# Planning Module

class StrategicThemePlanningListView(RoleAndDesignationRequiredMixin, ListView):
    model = StrategicTheme
    template_name = 'general/base.html'  # Replace with your template name
    context_object_name = 'themes'

    def get_queryset(self):
        # Fetch all strategic themes
        return StrategicTheme.objects.all()


class StrategicObjectivePlanningListView(RoleAndDesignationRequiredMixin, ListView):
    model = StrategicObjective
    template_name = 'planning.html'  
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = self.kwargs.get('theme_id')
        # Retrieve the StrategicTheme object based on the theme_id
        theme = get_object_or_404(StrategicTheme, id=theme_id) 
        context['theme'] = theme
        context['strategic_objectives'] = self.get_queryset() 
        context['page_name'] = 'objective_planning_list'  
        return context
    
    def get_queryset(self):
        user_designation = self.request.user.designation.first()
        theme_id = self.kwargs.get('theme_id')
        queryset = StrategicObjective.objects.filter(
        strategic_theme__id=theme_id,
        designation=user_designation
        )

        return queryset
    
class KPIPlanningListView(RoleAndDesignationRequiredMixin, ListView):
    model = KPI
    template_name = 'planning.html'  # Replace with your template name
    context_object_name = 'kpis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        strategic_objective_id = self.kwargs.get('strategic_objective_id')

        # Retrieve the strategic objective
        objective = get_object_or_404(StrategicObjective, id=strategic_objective_id)
        context['objective'] = objective
        context['page_name'] = 'kpi_planning_list'
        return context

    def get_queryset(self):
        objective_id = self.kwargs.get('strategic_objective_id')
        queryset = KPI.objects.filter(strategic_objective_id=objective_id)
        return queryset


def main_activity_create(request, kpi_id):
    kpi = get_object_or_404(KPI, id=kpi_id)
    form = MainActivityForm()  # Your form logic here

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/kpi_content.html', {'form': form, 'kpi': kpi})

    return render(request, 'full_template.html', {'form': form, 'kpi': kpi})

class MainActivityCreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = MainActivity
    form_class = MainActivityForm
    template_name = 'planning.html'
    success_url = reverse_lazy('activities')  # Replace with your success URL
    
    def form_valid(self, form):
        """
        Set the KPI field to the KPI object based on kpi_id before saving.
        """
        kpi_id = self.kwargs.get('kpi_id')
        form.instance.kpi = get_object_or_404(KPI, id=kpi_id)
        form.instance.created_by = self.request.user  # Optionally set the creator
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kpi_id = self.kwargs.get('kpi_id')
        name = get_object_or_404(KPI, id=kpi_id)
        context['kpi'] = name
        context['page_name'] = 'main_activity_create'  # Set this for conditional rendering
        return context
    
    def get_success_url(self):
        # Redirect to SubActivityCreate view after submitting
        main_activity_id = self.object.id
        kpi_id = self.kwargs.get('kpi_id')
        if self.object and main_activity_id:
            return reverse_lazy('sub_activity_create', kwargs={
                'kpi_id': kpi_id,
                'main_activity_id': main_activity_id
            })
        else:
            return reverse_lazy('sub_activity_create_without_main', kwargs={
                'kpi_id': kpi_id
        })
    
class MainActivityUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = MainActivity
    form_class = MainActivityForm
    template_name = 'planning.html'
    success_url = reverse_lazy('activities')  # Replace with your success URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'main_activity_update'  # Set this for conditional rendering
        return context
class ActivityPlanningUpdateView(RoleAndDesignationRequiredMixin, UpdateView):
    model = MainActivity
    form_class = MainActivityForm
    template_name = 'planning.html'
    success_url = reverse_lazy('activities')  # Replace with your success URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'sub_activity_update'  # Set this for conditional rendering
        return context
    
class ActivityPlanningCreateView(RoleAndDesignationRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'planning.html'
    success_url = reverse_lazy('sub_activity_create')  # Replace with your success URL
    
    def form_valid(self, form):
        """
        Set the KPI field to the KPI object based on kpi_id before saving.
        """
        kpi_id = self.kwargs.get('kpi_id')
        main_activity_id = self.kwargs.get('main_activity_id')
        form.instance.kpi = get_object_or_404(KPI, id=kpi_id)
        form.instance.designation = self.request.user.designation.first()
        if main_activity_id:
            form.instance.main_activity = get_object_or_404(MainActivity, id=main_activity_id)
        
        form.instance.created_by = self.request.user  # Optionally set the creator
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kpi_id = self.kwargs.get('kpi_id')
        
        name = get_object_or_404(KPI, id=kpi_id)
        context['kpi'] = name
        context['page_name'] = 'sub_activity_create'  # Set this for conditional rendering
        return context
    def get_success_url(self):
        # Redirect to SubActivityList view after submitting        
        main_activity_id = self.kwargs.get('main_activity_id')
        kpi_id = self.kwargs.get('kpi_id')
        if self.object and main_activity_id:
            return reverse_lazy('sub_activity_create', kwargs={
                'kpi_id': kpi_id,
                'main_activity_id': main_activity_id
            })
        else:
            return reverse_lazy('sub_activity_create_without_main', kwargs={
                'kpi_id': kpi_id
        })
            
class MyActivitiesListView(RoleAndDesignationRequiredMixin, ListView):
    model = Activity
    template_name = 'my-activities.html'
    context_object_name = 'activities'
    paginate_by = 10  # Optional: Add pagination if needed
    
    def get_queryset(self):
        user = self.request.user
        """
        Customize the queryset to order and filter activities as needed.
        """
        queryset = super().get_queryset().filter(designation=user.designation.first()).select_related('main_activity', 'designation', 'kpi').order_by('name')
        
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        quarter = self.request.GET.get('quarter')
        
        if not year:  # Ensure year is mandatory
            return queryset
        
        queryset = queryset.filter(start_date__year=year)

        # Filter by month (if provided)
        if month:
            queryset = queryset.filter(start_date__month=month)
            
        if quarter:
            start_month, end_month = self.get_quarter_months(int(quarter))
            queryset = queryset.filter(start_date__month__gte=start_month, start_date__month__lte=end_month)                
        return queryset 
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
        Pass filter data back to the template for display.
        """
        months = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        current_year = datetime.now().year
        context['years'] = range(current_year, current_year - 5, -1)
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['months'] = months
        return context
    
    @staticmethod
    def get_quarter_months(quarter):
        """
        Returns the start and end months of the quarter.
        """
        quarters = {
            1: (1, 3),   # Q1: January to March
            2: (4, 6),   # Q2: April to June
            3: (7, 9),   # Q3: July to September
            4: (10, 12), # Q4: October to December
        }
        return quarters.get(quarter, (1, 3))
    
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports.html'
    success_url = reverse_lazy('report_list')  # Replace with your actual report list URL name

    def form_valid(self, form):
        # Automatically set the user and designation from the logged-in user
        form.instance.user = self.request.user
        form.instance.designation = self.request.user.designation  # Assuming `designation` is a field in the User model
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kpi_id = self.kwargs.get('kpi_id')
        
        
        context['page_name'] = 'main_activity_create'  # Set this for conditional rendering
        return context
    
class ReportListView(TemplateView):
    template_name = 'reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get activities and reports
        activities = Activity.objects.filter(
            designation=self.request.user.designation.first(),
            status=1
        )
        reports = Report.objects.filter(designation=self.request.user.designation.first())

        # Apply filters to activities
        activities = apply_filters(activities, self.request)
        # Create a mapping of activity IDs to their reports
        reports_by_activity = {report.activity_id: report for report in reports}

        # Pass activities, reports, and the form to the context
        context['activities'] = activities
        context['reports_by_activity'] = reports_by_activity  # Pre-filtered reports by activity ID
        context['form'] = ReportForm()
        return context
    
class ScoreCardListView(TemplateView):
    template_name = 'score-cards.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get activities and reports
        activities = Activity.objects.filter(
            designation=self.request.user.designation.first(),
            status=0
            )
        reports = Report.objects.filter(
            designation=self.request.user.designation.first()
            )
        # Apply filters to activities
        activities = apply_filters(activities, self.request)
        # Create a mapping of activity IDs to their reports
        reports_by_activity = {report.activity_id: report for report in reports}
        
        months = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        
        # Pass activities, reports, and the form to the context
        context['activities'] = activities
        context['reports_by_activity'] = reports_by_activity  # Pre-filtered reports by activity ID
        context['form'] = ReportForm()
        current_year = datetime.now().year
        context['years'] = range(current_year, current_year - 5, -1)
        context['months'] = months
        
        return context

    
class ActivityReportView(TemplateView):
    template_name = 'reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activity.objects.filter(
            designation=self.request.user.designation.first(),
            status=1
            )  # Fetch all activities
        context['reports'] = Report.objects.filter(
            activity__status=1,
            designation=self.request.user.designation.first()
            )
        context['form'] = ReportForm()
        return context

class SubmitReportView(View):
    def post(self, request, activity_id):
        # Fetch the activity object
        activity = get_object_or_404(Activity, id=activity_id)

        # Get or create the report object for the user and activity
        report, created = Report.objects.get_or_create(
            user=request.user,
            activity=activity,
            defaults={'designation': request.user.designation.first()}
        )

        if activity.status == 1:
            messages.error(request, "This report has already been submitted.")
            return redirect('report_list')  

        # Bind the form to the POST data
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.instance.designation = self.request.user.designation.first()
            form.save()
            activity.status = 1
            activity.save()

            messages.success(request, "Report submitted successfully.")
        else:
            messages.error(request, "There was an error submitting the report.")

        # Redirect back to the report list page
        return redirect('report_list') 


# delete me ??????
class FullReportView(TemplateView):
    template_name = "reports_templates/full-reports.html"  # The HTML template for the table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the logged-in user 
        user = self.request.user
        quarter = ''
        current_month = datetime.now().month

        # Determine the quarter based on the current month
        if 1 <= current_month <= 3:
            quarter = "First"
        elif 4 <= current_month <= 6:
            quarter = "Second"
        elif 7 <= current_month <= 9:
            quarter = "Third"
        elif 10 <= current_month <= 12:
            quarter = "Fourth"
            
        context["request"] = self.request.user.designation.first().name
        context["user"] = self.request.user
        context["quarter"] = quarter
        # Fetch all themes
        themes = StrategicTheme.objects.all()

        # Create structured data for the table
        data = []
        for theme in themes:
            objectives = theme.objectives.all()
            department_name = objective.designation.name 
            for objective in objectives:
                kpis = objective.kpis.all()
                for kpi in kpis:
                    main_activities = kpi.main_activities.all()
                    for main_activity in main_activities:
                        activities = main_activity.activities.all()
                        for activity in activities:
                            # Fetch the report if available
                            report = activity.reports.filter(user=user).first()

                            data.append({
                                "theme": theme.theme_name,
                                "objective": objective.objective_name,
                                "department" : department_name,
                                "kpi": kpi.name,
                                "main_activity": main_activity.name,
                                "activity": activity.name,
                                "start_date": activity.start_date,
                                "end_date": activity.end_date,
                                "status": report.goal_score if report else "No Report",
                                "q1": "",  # Leave empty for now
                                "report_details": report.report_details if report else "No details",
                            })

        context["data"] = data
        return context
    
class GenerateReportView(TemplateView):
    template_name = 'reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'generate_department_report'
        
        # Provide a list of years (e.g., last 10 years)
        current_year = datetime.now().year
        context['years'] = range(current_year, current_year - 5, -1)
    
        return context
class GeneratePlanningReportView(TemplateView):
    template_name = 'my-activities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'generate_activities_report'
        
        # Provide a list of years (e.g., last 10 years)
        current_year = datetime.now().year
        context['years'] = range(current_year, current_year - 5, -1)
    
        return context
    
class GenerateChurchReportsView(TemplateView):
    template_name = 'admin-full-reports.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide a list of years (e.g., last 10 years)
        current_year = datetime.now().year
        context['years'] = range(current_year, current_year - 5, -1)
        
        return context
class GenerateChurchPlansView(TemplateView):
    template_name = 'admin-church-plan.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide a list of years (e.g., last 10 years)
        current_year = datetime.now().year
        context['years'] = range(current_year, current_year - 5, -1)
        return context

class DepartmentalReportView(TemplateView):
    template_name = "reports_templates/departmental-reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        quarter = self.request.GET.get("report_period", "")
        year = self.request.GET.get("year", "")
        department = user.designation.first().name
        # Determine date range for the selected quarter
        start_date, end_date = self.get_date_range(year, quarter)

        themes = StrategicTheme.objects.all()
        data = []
        for theme in themes:
            objectives = theme.objectives.filter(designation__users=user)
            for objective in objectives:
                kpis = objective.kpis.all()
                for kpi in kpis:
                    main_activities = kpi.main_activities.all()
                    for main_activity in main_activities:
                        activities = main_activity.activities.all()
                        for activity in activities:
                            # Fetch the report within the selected period
                            report = activity.reports.filter(
                                 report_date__range=(start_date, end_date)
                            ).first()

                            # Only append data if a report exists
                            if report:
                                data.append({
                                    "theme": theme.theme_name,
                                    "objective": objective.objective_name,
                                    "kpi": kpi.name,
                                    "main_activity": main_activity.name,
                                    "activity": activity.name,
                                    "start_date": activity.start_date,
                                    "end_date": activity.end_date,
                                    "budget": activity.estimated_amount,
                                    "status": report.goal_score,
                                    "report_details": report.report_details,
                                })
        context["department"] = department
        context["quarter"] = quarter
        context["year"] = year
        context["data"] = data
        return context

    def get_date_range(self, year, quarter):
        """Returns the start and end dates for the given year and quarter."""
        if not year.isdigit():
            year = datetime.now().year  # Default to current year
        year = int(year)

        if quarter == "First Quarter":
            return f"{year}-01-01", f"{year}-03-31"
        elif quarter == "Second Quarter":
            return f"{year}-04-01", f"{year}-06-30"
        elif quarter == "Third Quarter":
            return f"{year}-07-01", f"{year}-09-30"
        elif quarter == "Fourth Quarter":
            return f"{year}-10-01", f"{year}-12-31"
        elif quarter == "Full Year":
            return f"{year}-01-01", f"{year}-12-31"
        else:
            return f"{year}-01-01", f"{year}-12-31"  # Default to full year
        
class DepartmentPlanView(TemplateView):
    template_name = "reports_templates/departmental-plans.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        quarter = self.request.GET.get("report_period", "")
        year = self.request.GET.get("year", "")
        department = user.designation.first().name
        # Determine date range for the selected quarter
        start_date, end_date = self.get_date_range(year, quarter)

        themes = StrategicTheme.objects.all()
        data = []
        for theme in themes:
            objectives = theme.objectives.filter(designation__users=user)
            for objective in objectives:
                kpis = objective.kpis.all()
                for kpi in kpis:
                    main_activities = kpi.main_activities.all()
                    for main_activity in main_activities:
                        activities = main_activity.activities.filter(
                            designation=user.designation.first(),
                            start_date__gte=start_date,
                            start_date__lte=end_date
                        )
                            
                        for activity in activities:

                            if activities:
                                data.append({
                                    "theme": theme.theme_name,
                                    "objective": objective.objective_name,
                                    "kpi": kpi.name,
                                    "main_activity": main_activity.name,
                                    "activity": activity.name,
                                    "start_date": activity.start_date,
                                    "end_date": activity.end_date,
                                    "budget": activity.estimated_amount,
                                    "details": activity.description,
                                })
                                
        context["department"] = department
        context["quarter"] = quarter
        context["year"] = year
        context["data"] = data
        return context

    def get_date_range(self, year, quarter):
        """Returns the start and end dates for the given year and quarter."""
        if not year.isdigit():
            year = datetime.now().year  # Default to current year
        year = int(year)

        if quarter == "First Quarter":
            return f"{year}-01-01", f"{year}-03-31"
        elif quarter == "Second Quarter":
            return f"{year}-04-01", f"{year}-06-30"
        elif quarter == "Third Quarter":
            return f"{year}-07-01", f"{year}-09-30"
        elif quarter == "Fourth Quarter":
            return f"{year}-10-01", f"{year}-12-31"
        elif quarter == "Full Year":
            return f"{year}-01-01", f"{year}-12-31"
        else:
            return f"{year}-01-01", f"{year}-12-31"  # Default to full year
        
class AdminDepartmentalReportView(TemplateView):
    template_name = "reports_templates/admin-department-report.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        quarter = self.request.GET.get("report_period", "")
        year = self.request.GET.get("year", "")
        designation_id = self.request.GET.get("designation_id", "")
        designation_name = self.request.GET.get("designation_name", "")
        print(designation_id)
        # Determine date range for the selected quarter
        start_date, end_date = self.get_date_range(year, quarter)
        themes = StrategicTheme.objects.all()
        data = []
        for theme in themes:
            objectives = theme.objectives.filter(
                Q(designation__id=designation_id) if designation_id else Q()
            )
            for objective in objectives:
                kpis = objective.kpis.all()
                for kpi in kpis:
                    main_activities = kpi.main_activities.all()
                    for main_activity in main_activities:
                        activities = main_activity.activities.filter(
                            designation=designation_id,
                        )
                        for activity in activities:
                            # Fetch the report within the selected period
                            report = activity.reports.filter(
                                 report_date__range=(start_date, end_date)
                            ).first()

                            # Only append data if a report exists
                            if report:
                                data.append({
                                    "theme": theme.theme_name,
                                    "objective": objective.objective_name,
                                    "kpi": kpi.name,
                                    "main_activity": main_activity.name,
                                    "activity": activity.name,
                                    "start_date": activity.start_date,
                                    "end_date": activity.end_date,
                                    "budget": activity.estimated_amount,
                                    "status": report.goal_score,
                                    "report_details": report.report_details,
                                })
        context["department"] = designation_name                    
        context["quarter"] = quarter
        context["year"] = year
        context["data"] = data
        return context
    
    def get_date_range(self, year, quarter):
        """Returns the start and end dates for the given year and quarter."""
        if not year.isdigit():
            year = datetime.now().year  # Default to current year
        year = int(year)

        if quarter == "First Quarter":
            return f"{year}-01-01", f"{year}-03-31"
        elif quarter == "Second Quarter":
            return f"{year}-04-01", f"{year}-06-30"
        elif quarter == "Third Quarter":
            return f"{year}-07-01", f"{year}-09-30"
        elif quarter == "Fourth Quarter":
            return f"{year}-10-01", f"{year}-12-31"
        elif quarter == "Full Year":
            return f"{year}-01-01", f"{year}-12-31"
        else:
            return f"{year}-01-01", f"{year}-12-31"  # Default to full year
        
class AdminDepartmentalPlanView(TemplateView):
    template_name = "reports_templates/admin-department-plan.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        quarter = self.request.GET.get("report_period", "")
        year = self.request.GET.get("year", "")
        designation_id = self.request.GET.get("designation_id", "")
        designation_name = self.request.GET.get("designation_name", "")
        context["name"] = designation_name                       
        
        print(f"Designation ID: {designation_id}, Designation Name: {designation_name}")

        # Determine date range for the selected quarter
        start_date, end_date = self.get_date_range(year, quarter)
        themes = StrategicTheme.objects.all()
        data = []
        for theme in themes:
            objectives = theme.objectives.filter(
                Q(designation__id=designation_id) if designation_id else Q()
            )
            for objective in objectives:
                kpis = objective.kpis.all()
                for kpi in kpis:
                    main_activities = kpi.main_activities.all()
                    for main_activity in main_activities:                     
                        activities = main_activity.activities.filter(
                            designation=designation_id,
                            start_date__gte=start_date,
                            start_date__lte=end_date
                        )
                            
                        for activity in activities:
                            
                            if activities:
                                data.append({
                                    "theme": theme.theme_name,
                                    "objective": objective.objective_name,
                                    "kpi": kpi.name,
                                    "main_activity": main_activity.name,
                                    "activity": activity.name,
                                    "date": activity.start_date,
                                    "budget": activity.estimated_amount,
                                    "details": activity.description,
                                })
                                
        context["quarter"] = quarter
        context["year"] = year
        context["data"] = data
        return context

    def get_date_range(self, year, quarter):
        """Returns the start and end dates for the given year and quarter."""
        if not year.isdigit():
            year = datetime.now().year  # Default to current year
        year = int(year)

        if quarter == "First Quarter":
            return f"{year}-01-01", f"{year}-03-31"
        elif quarter == "Second Quarter":
            return f"{year}-04-01", f"{year}-06-30"
        elif quarter == "Third Quarter":
            return f"{year}-07-01", f"{year}-09-30"
        elif quarter == "Fourth Quarter":
            return f"{year}-10-01", f"{year}-12-31"
        elif quarter == "Full Year":
            return f"{year}-01-01", f"{year}-12-31"
        else:
            return f"{year}-01-01", f"{year}-12-31"  # Default to full year
        
class AdminChurchReportView(TemplateView):
    template_name = "reports_templates/admin-church-report.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        quarter = self.request.GET.get("report_period", "")
        year = self.request.GET.get("year", "")

        # Determine date range for the selected quarter
        start_date, end_date = self.get_date_range(year, quarter)
        themes = StrategicTheme.objects.all()
        data = []
        for theme in themes:
            objectives = theme.objectives.all()
            for objective in objectives:
               
            
                kpis = objective.kpis.all()
                for kpi in kpis:
                    main_activities = kpi.main_activities.all()
                    for main_activity in main_activities:
                        activities = main_activity.activities.all()
                        for activity in activities:
                             # Access the designation directly since it's a ForeignKey
                            department_name = activity.designation.name if activity.designation else "No Department"
                            
                            report = activity.reports.filter(
                                 report_date__range=(start_date, end_date)
                            ).first()

                            # Only append data if a report exists
                            if report:
                                data.append({
                                    "theme": theme.theme_name,
                                    "objective": objective.objective_name,
                                    "department": department_name,
                                    "kpi": kpi.name,
                                    "main_activity": main_activity.name,
                                    "activity": activity.name,
                                    "status": report.goal_score,
                                    "start_date": activity.start_date,
                                    "end_date": activity.end_date,
                                    "budget": report.actual_spent,
                                    "report_details": report.report_details,
                                })
                                                    
        context["quarter"] = quarter
        context["year"] = year
        context["data"] = data
        return context

    def get_date_range(self, year, quarter):
        """Returns the start and end dates for the given year and quarter."""
        if not year.isdigit():
            year = datetime.now().year  # Default to current year
        year = int(year)

        if quarter == "First Quarter":
            return f"{year}-01-01", f"{year}-03-31"
        elif quarter == "Second Quarter":
            return f"{year}-04-01", f"{year}-06-30"
        elif quarter == "Third Quarter":
            return f"{year}-07-01", f"{year}-09-30"
        elif quarter == "Fourth Quarter":
            return f"{year}-10-01", f"{year}-12-31"
        elif quarter == "Full Year":
            return f"{year}-01-01", f"{year}-12-31"
        else:
            return f"{year}-01-01", f"{year}-12-31"  # Default to full year
        
class AdminChurchPlanView(TemplateView):
    template_name = "reports_templates/admin-church-plan.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        quarter = self.request.GET.get("report_period", "")
        year = self.request.GET.get("year", "")

        # Determine date range for the selected quarter
        start_date, end_date = self.get_date_range(year, quarter)
        themes = StrategicTheme.objects.all()
        data = []
        for theme in themes:
            objectives = theme.objectives.all()
            for objective in objectives:
                kpis = objective.kpis.all()
                for kpi in kpis:
                    main_activities = kpi.main_activities.all()
                    for main_activity in main_activities:
                        activities = main_activity.activities.filter(
                            start_date__gte=start_date,
                            start_date__lte=end_date
                        )
                            
                        for activity in activities:
                            department_name = activity.designation.name if activity.designation else "None"
                            if activities:
                                data.append({
                                    "theme": theme.theme_name,
                                    "objective": objective.objective_name,
                                    "department": department_name,
                                    "kpi": kpi.name,
                                    "main_activity": main_activity.name,
                                    "activity": activity.name,
                                    "start_date": activity.start_date,
                                    "end_date": activity.end_date,
                                    "budget": activity.estimated_amount,
                                    "details": activity.description,
                                })             
        context["quarter"] = quarter
        context["year"] = year
        context["data"] = data
        return context

    def get_date_range(self, year, quarter):
        """Returns the start and end dates for the given year and quarter."""
        if not year.isdigit():
            year = datetime.now().year  # Default to current year
        year = int(year)

        if quarter == "First Quarter":
            return f"{year}-01-01", f"{year}-03-31"
        elif quarter == "Second Quarter":
            return f"{year}-04-01", f"{year}-06-30"
        elif quarter == "Third Quarter":
            return f"{year}-07-01", f"{year}-09-30"
        elif quarter == "Fourth Quarter":
            return f"{year}-10-01", f"{year}-12-31"
        elif quarter == "Full Year":
            return f"{year}-01-01", f"{year}-12-31"
        else:
            return f"{year}-01-01", f"{year}-12-31"  # Default to full year

# class DepartmentalReportView(TemplateView):
#     template_name = "reports_templates/departmental-reports.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         # Get year and quarter from GET parameters
#         year = self.request.GET.get('year')
#         report_period = self.request.GET.get('report_period')

#         # Determine the start and end months of the selected quarter
#         quarters = {
#             "First Quarter": (1, 3),
#             "Second Quarter": (4, 6),
#             "Third Quarter": (7, 9),
#             "Fourth Quarter": (10, 12),
#             "Full Year": (1, 12)
#         }
#         start_month, end_month = quarters.get(report_period, (1, 12))

#         # Calculate the start and end dates for the selected period
#         if year:
#             start_date = datetime(int(year), start_month, 1)
#             end_date = datetime(int(year), end_month, 1).replace(day=31)  # Safely use last day
#         else:
#             # Default to the current quarter if no year/period is selected
#             year = datetime.now().year
#             current_month = datetime.now().month
#             start_month, end_month = quarters.get(report_period, (1, 12))
#             start_date = datetime(year, start_month, 1)
#             end_date = datetime(year, end_month, 31)

#         # Filter logic
#         user = self.request.user
#         themes = StrategicTheme.objects.all()

#         # Create structured data for the table
#         data = []
#         for theme in themes:
#             objectives = theme.objectives.filter(designation__users=user)
#             for objective in objectives:
#                 kpis = objective.kpis.all()
#                 for kpi in kpis:
#                     main_activities = kpi.main_activities.all()
#                     for main_activity in main_activities:
#                         activities = main_activity.activities.all()
#                         for activity in activities:
#                             # Fetch the report if available and filter by date
#                             report = activity.reports.filter(
#                                 user=user,
#                                 report_date__gte=start_date,
#                                 report_date__lte=end_date
#                             ).first()

#                             data.append({
#                                 "theme": theme.theme_name,
#                                 "objective": objective.objective_name,
#                                 "kpi": kpi.name,
#                                 "main_activity": main_activity.name,
#                                 "activity": activity.name,
#                                 "status": report.goal_score if report else "red",
#                                 "q1": "",  # Leave empty for now
#                                 "report_details": report.report_details if report else "No details",
#                             })

#         context["data"] = data
#         context["year"] = year
#         context["report_period"] = report_period
#         context["quarter"] = report_period.split()[0] if report_period else "Full Year"
#         return context

    
# class DepartmentalReportView(TemplateView):
#     template_name = "reports_templates/departmental-reports.html"  # The HTML template for the table

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Get the logged-in user 
#         user = self.request.user
#         quarter=''
#         current_month = datetime.now().month

#         # Determine the quarter based on the current month
#         if 1 <= current_month <= 3:
#             quarter = "First"
#         elif 4 <= current_month <= 6:
#             quarter = "Second"
#         elif 7 <= current_month <= 9:
#             quarter = "Third"
#         elif 10 <= current_month <= 12:
#             quarter = "Fourth"
            
#         context["request"] = self.request.user.designation.name
#         context["user"] = self.request.user
#         context["quarter"] = quarter
#         # Fetch all themes
#         themes = StrategicTheme.objects.all()

#         # Create structured data for the table
#         data = []
#         for theme in themes:
#             objectives = theme.objectives.filter(designation__users=user)
#             for objective in objectives:
#                 kpis = objective.kpis.all()
#                 for kpi in kpis:
#                     main_activities = kpi.main_activities.all()
#                     for main_activity in main_activities:
#                         activities = main_activity.activities.all()
#                         for activity in activities:
#                             # Fetch the report if available
#                             report = activity.reports.filter(user=user).first()
                            
                            

#                             data.append({
#                                 "theme": theme.theme_name,
#                                 "objective": objective.objective_name,
#                                 "kpi": kpi.name,
#                                 "main_activity": main_activity.name,
#                                 "activity": activity.name,
#                                 "status": report.goal_score if report else "No Report",
#                                 "q1": "",  # Leave empty for now
#                                 "report_details": report.report_details if report else "No details",
#                             })

#         context["data"] = data
#         return context




class AdminReportsListView(RoleAndDesignationRequiredMixin, ListView):
    model = Designation
    template_name = 'admin-reports.html'  # Update with actual template path
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the currently logged-in user
        user = self.request.user

        # Check if the user's role is "Elder"
        if user.role and user.role.name == "Elder":
            # Fetch designations (departments) for the current user
            context['departments'] = user.designation.all()
        else:
            # Default: all departments
            context['departments'] = Designation.objects.all()

        # Add a range of years (e.g., last 5 years)
        current_year = datetime.now().year
        context['years'] = range(current_year, current_year - 5, -1)

        return context

class AdminPlansListView(RoleAndDesignationRequiredMixin, ListView):
    model = Designation
    template_name = 'admin-plans.html'  # Update with actual template path
    context_object_name = 'departments'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the currently logged-in user
        user = self.request.user

        # Check if the user's role is "Elder"
        if user.role and user.role.name == "Elder":
            # Fetch designations (departments) for the current user
            context['departments'] = user.designation.all()
        else:
            # Default: all departments
            context['departments'] = Designation.objects.all()

        # Add a range of years (e.g., last 5 years)
        current_year = datetime.now().year
        context['years'] = range(current_year, current_year - 5, -1)

        return context
    
class AdminReportListView(TemplateView):
    template_name = 'reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get activities and reports
        activities = Activity.objects.all()
        reports = Report.objects.filter(designation=self.request.user.designation.first())

        # Create a mapping of activity IDs to their reports
        reports_by_activity = {report.activity_id: report for report in reports}

        # Pass activities, reports, and the form to the context
        context['activities'] = activities
        context['reports_by_activity'] = reports_by_activity  # Pre-filtered reports by activity ID
        context['form'] = ReportForm()
        return context
    
    
def download_pdf(request):
    themes = StrategicTheme.objects.prefetch_related(
        'objectives__kpis__main_activities__activities'
    ).all()

    data = []
    for theme in themes:
        theme_row_span = 0
        objectives_data = []
        for obj in theme.objectives.all():
            objective_row_span = 0
            kpis_data = []
            for kpi in obj.kpis.all():
                kpi_row_span = kpi.main_activities.count() or 1
                main_activities_data = [
                    {
                        "main_activity": ma,
                        "activities": ma.activities.all()
                    } for ma in kpi.main_activities.all()
                ]
                kpis_data.append({
                    "kpi": kpi,
                    "kpi_row_span": kpi_row_span,
                    "main_activities": main_activities_data,
                })
                objective_row_span += kpi_row_span
            objectives_data.append({
                "objective": obj,
                "objective_row_span": objective_row_span,
                "kpis": kpis_data,
            })
            theme_row_span += objective_row_span
        data.append({
            "theme": theme,
            "theme_row_span": theme_row_span,
            "objectives": objectives_data,
        })
    
    # Generate the PDF
    pdf_filename = "strategic_themes.pdf"
    return FileResponse(open(pdf_filename, 'rb'), as_attachment=True, filename=pdf_filename)

def apply_filters(queryset, request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    quarter = request.GET.get('quarter')

    if year:
        queryset = queryset.filter(start_date__year=year)

        if month:
            queryset = queryset.filter(start_date__month=month)
        
        if quarter:
            start_month, end_month = get_quarter_months(int(quarter))
            queryset = queryset.filter(start_date__month__gte=start_month, start_date__month__lte=end_month)
    
    return queryset

def get_quarter_months(quarter):
    """
    Returns the start and end months of the quarter.
    """
    quarters = {
        1: (1, 3),   # Q1: January to March
        2: (4, 6),   # Q2: April to June
        3: (7, 9),   # Q3: July to September
        4: (10, 12), # Q4: October to December
    }
    return quarters.get(quarter, (1, 3))