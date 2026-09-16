from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_admin_user(apps, schema_editor):
    User = apps.get_model("strategic_planning", "User")
    Role = apps.get_model("strategic_planning", "Role")
    Designation = apps.get_model("strategic_planning", "Designation")

    admin_role, _ = Role.objects.get_or_create(name="Admin")
    pastor_designation, _ = Designation.objects.get_or_create(name="SPEMEC")

    admin_user, created = User.objects.get_or_create(
        email="admin@gmail.com",
        defaults={
            "first_name": "Admin",
            "last_name": "User",
            "dob": "1990-01-01",
            "contact": "1234567890",
            "physical_address": "Admin Address",
            "role": admin_role,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
            "password": make_password("@uni$da2#"),
        },
    )

    if created:
        # Add the Many-to-Many relation
        admin_user.designation.add(pastor_designation)


def remove_admin_user(apps, schema_editor):
    User = apps.get_model("strategic_planning", "User")
    User.objects.filter(email="admin@gmail.com").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('strategic_planning', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, reverse_code=remove_admin_user),
    ]
