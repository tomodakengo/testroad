from django.contrib import admin
from .models import (
    Project, TestSuite, TestCase, TestPlan,
    TestPlanCase, TestRun, TestResult
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')


@admin.register(TestSuite)
class TestSuiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'created_at', 'updated_at')
    list_filter = ('project',)
    search_fields = ('name', 'description')


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'suite', 'created_by', 'created_at', 'updated_at')
    list_filter = ('suite__project', 'suite', 'created_by')
    search_fields = ('title', 'description', 'steps', 'expected_result')


class TestPlanCaseInline(admin.TabularInline):
    model = TestPlanCase
    extra = 1


@admin.register(TestPlan)
class TestPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'created_by', 'created_at', 'updated_at')
    list_filter = ('project', 'created_by')
    search_fields = ('name', 'description')
    inlines = [TestPlanCaseInline]


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    list_display = ('name', 'test_plan', 'status', 'assigned_to', 'created_at', 'updated_at')
    list_filter = ('status', 'test_plan__project', 'assigned_to')
    search_fields = ('name', 'description')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test_case', 'test_run', 'status', 'executed_by', 'executed_at')
    list_filter = ('status', 'test_run', 'executed_by')
    search_fields = ('test_case__title', 'comment')
