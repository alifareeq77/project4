# Generated by Django 4.0.3 on 2022-04-28 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_profile_follower_alter_profile_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='profile',
        ),
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='post_profile', to='network.profile'),
            preserve_default=False,
        ),
    ]