from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# ENUM Choices
class QuaterEnum(models.TextChoices):
    FIRST = '1st', '1st'
    SECOND = '2nd', '2nd'
    THIRD = '3rd', '3rd'
    FOURTH = '4th', '4th'

class GoalScoreEnum(models.TextChoices):
    GREEN =  'green', 'Completed'
    ORANGE = 'orange','Progressing' 
    YELLOW = 'yellow', 'Early Stage' 
    RED = 'red','No Activity'

# Models
class Designation(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Still hashed
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    physical_address = models.TextField()
    last_logged_in = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required by PermissionsMixin

    # Relationships
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True, related_name="users")
    designation = models.ManyToManyField(Designation, related_name="users")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # The field used for login
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Required when creating superusers

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StrategicTheme(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme_name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.theme_name

class StrategicObjective(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    objective_name = models.CharField(max_length=200)
    strategic_theme = models.ForeignKey(StrategicTheme, on_delete=models.CASCADE, related_name="objectives") 
    designation = models.ManyToManyField(Designation, related_name="objectives")
    def __str__(self):
        return self.objective_name

class KPI(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    strategic_objective = models.ForeignKey(StrategicObjective, on_delete=models.CASCADE, related_name="kpis")
    def __str__(self):
        return self.name

class MainActivity(models.Model):
    date_created = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    kpi = models.ForeignKey('KPI', on_delete=models.CASCADE, related_name="main_activities", null=True, default=None)


    def __str__(self):
        return self.name

class Activity(models.Model):
    date_created = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField()
    kpi = models.ForeignKey('KPI', on_delete=models.CASCADE, related_name="activities")
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, related_name='Activities')
    status = models.IntegerField(default=0)
    main_activity = models.ForeignKey(MainActivity, on_delete=models.CASCADE, null=True, 
        blank=True, 
        related_name="activities"
    ) 
    estimated_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


class Report(models.Model):
    report_date= models.DateField(null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="reports")
    goal_score = models.CharField(max_length=20, choices=GoalScoreEnum.choices)
    report_details = models.TextField()
    actual_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    def __str__(self):
        return f"Report by {self.user.first_name}"


