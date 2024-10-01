# Generated by Django 5.0.2 on 2024-10-01 16:31

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='RoleModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(choices=[('ADMIN', 'Administrador'), ('EMPLOYEE', 'Empleado'), ('VIEWER', 'Vista')], default='EMPLOYEE', max_length=64, unique=True)),
                ('description', models.TextField(blank=True, max_length=128, null=True)),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('role', models.ManyToManyField(related_name='users', to='accounts.rolemodel')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='ProviderModel',
            fields=[
                ('personmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.personmodel')),
                ('RFC', models.CharField(max_length=13, unique=True)),
                ('NSS', models.CharField(max_length=11, unique=True)),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
            },
            bases=('accounts.personmodel',),
        ),
        migrations.CreateModel(
            name='StudentModel',
            fields=[
                ('personmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.personmodel')),
                ('control_number', models.CharField(max_length=64, unique=True)),
                ('degree', models.CharField(choices=[('Architecture', 'Arquitectura'), ('B.A. in Administration', 'Licenciatura en Administración'), ('Public Accountant', 'Contador Público'), ('Environmental Engineering', 'Ingeniería Ambiental'), ('Biomedical Engineering', 'Ingeniería Biomedica'), ('Civil Engineering', 'Ingeniería Civil'), ('Industrial Design Eng.', 'Ingeniería de Diseno Industrial'), ('Electronics Engineering', 'Ingeniería Electromecânica'), ('Business Management Engineering', 'Ingeniería de Negocios'), ('Logistics Engineering', 'Ingeniería Logística'), ('Nanotechnology Engineering', 'Ingeniería Nanotécnica'), ('Chemical Engineering', 'Ingeniería Química'), ('Aeronautical Engineering', 'Ingeniería Aeronaúutica'), ('Biochemical Engineering', 'Ingeniería Bioquímica'), ('Electromechanical Engineering', 'Ingeniería Electromecánica'), ('Computer Engineering', 'Ingeniería de Computación'), ('Computer Systems Engineering', 'Ingeniería de Sistemas de Computación'), ('Information Technology and Communications Engineering', 'Ingeniería de Telecomunicaciones y de la Información'), ('Cybersecurity Engineering', 'Ingeniería de Seguridad Informática'), ('Artificial Intelligence Engineering', 'Ingeniería de la Inteligencia Artificial'), ('Industrial Engineering', 'Ingeniería Industrial'), ('Mechanical Engineering', 'Ingeniería Mecânica')], default='Computer Systems Engineering', max_length=64)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
            bases=('accounts.personmodel',),
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Hombre'), ('F', 'Mujer'), ('O', 'Otro')], default='M', max_length=8)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, max_length=128, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
