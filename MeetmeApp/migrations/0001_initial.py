# Generated by Django 3.1.3 on 2020-12-10 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, null=True)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], max_length=50)),
                ('more_about_myself', models.TextField(null=True)),
                ('career', models.CharField(max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('blocked_by', models.ManyToManyField(blank=True, related_name='blocked', to=settings.AUTH_USER_MODEL)),
                ('likeability', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guy_seeking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_guy_seeking', to=settings.AUTH_USER_MODEL, verbose_name='Guy_seeking')),
                ('lady_seeking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_lady_seeking', to=settings.AUTH_USER_MODEL, verbose_name='Lady seeking')),
            ],
        ),
    ]