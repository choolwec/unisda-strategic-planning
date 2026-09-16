from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import (MainActivity, User, Designation, StrategicTheme, StrategicObjective, KPI, 
    Activity, Role, Report
)


class StrategicThemeForm(forms.ModelForm):
    class Meta:
        model = StrategicTheme
        fields = ['theme_name', 'description']
        labels = {
            'theme_name': 'Theme Name',
            'description': 'Description',
        }
        widgets = {
            'theme_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter theme name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }

class StrategicObjectiveForm(forms.ModelForm):
    class Meta:
        model = StrategicObjective
        fields = ['objective_name', 'strategic_theme', 'designation' ]
        labels = {
            'objective_name': 'Objective',
            'strategic_theme': 'Strategic Theme',
            'designation' : 'Department'
        }
        
        widgets = {
            'objective_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Objective'}),
            'strategic_theme': forms.Select(attrs={
                'class': 'form-control'
                }),     
            'designation': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),

        }

class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ['name','strategic_objective']
        labels = {
            'name': 'KPI Name',
            'strategic_objective': 'Strategic Objective',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter KPI name',
            }),
            'strategic_objective': forms.Select(attrs={'class': 'form-control'}),
        }

class MainActivityForm(forms.ModelForm):
    class Meta:
        model = MainActivity
        fields = ['name', 'description']  # Exclude 'created_by'
        labels = {
            'name': 'Main Activity Name',
            'description': 'Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter main activity name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description',
                'rows': 4,
            }),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'name', 'description', 'start_date', 'end_date',
             'estimated_amount'
        ]  # Exclude 'created_by'
        labels = {
            'name': 'Activity Name',
            'description': 'Description',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'estimated_amount': 'Estimated Amount',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter activity name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description',
                'rows': 4,
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),            
            'estimated_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the estimated amount',
            }),
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        labels = {
            'name': 'Role Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter role name'}),
        }


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name']
        labels = {
            'name': 'Designation Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation name'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_date', 'report_details', 'goal_score', 'actual_spent',]
        labels = {
            'report_date': 'Report Date:',
            'report_details': 'Report Details:',
            'goal_score': 'Goal Score:',
            'actual_spent': 'Total Spent'
        }
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'actual_spent': forms.NumberInput(attrs={ 'class': 'form-control'}),
            'report_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'goal_score': forms.Select(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =  ['first_name', 'last_name', 'password', 'contact', 'email', 'physical_address', 'role', 'designation', 'is_active']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'physical_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address', 'rows': 3}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password': 'Password',
            'contact': 'Contact Number',
            'email': 'Email Address',
            'physical_address': 'Physical Address',
            'role': 'User Role',
            'designation': 'Designation',
            'is_active': 'Active Status',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.all().order_by('name')

    def save(self, commit=True):
        """
        Override save method to handle password hashing.
        """
        user = super().save(commit=False)
        if user.password:  # Hash password before saving
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
  
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Email",)
    password = forms.Field(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password"
    )
