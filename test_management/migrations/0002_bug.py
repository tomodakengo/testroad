# Generated by Django 5.1.3 on 2025-02-06 07:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('description', models.TextField(verbose_name='説明')),
                ('priority', models.CharField(choices=[('critical', '最重要'), ('high', '高'), ('medium', '中'), ('low', '低')], default='medium', max_length=20, verbose_name='優先度')),
                ('status', models.CharField(choices=[('open', '未対応'), ('in_progress', '対応中'), ('resolved', '解決済み'), ('closed', '完了')], default='open', max_length=20, verbose_name='ステータス')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_bugs', to=settings.AUTH_USER_MODEL, verbose_name='担当者')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_bugs', to=settings.AUTH_USER_MODEL, verbose_name='起票者')),
                ('test_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_management.testresult', verbose_name='テスト結果')),
            ],
            options={
                'verbose_name': '不具合',
                'verbose_name_plural': '不具合',
            },
        ),
    ]
