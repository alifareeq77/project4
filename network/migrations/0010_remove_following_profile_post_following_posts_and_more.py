# Generated by Django 4.0.4 on 2022-05-02 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_remove_profile_following_following_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='profile',
        ),
        migrations.AddField(
            model_name='post',
            name='following_posts',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='network.following'),
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(to='network.following'),
        ),
    ]
