from django import forms
from .models import Project, TestSuite, TestCase, TestPlan, TestRun, TestResult, Bug


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class TestSuiteForm(forms.ModelForm):
    class Meta:
        model = TestSuite
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            value = files.get(name)
            if isinstance(value, list):
                return value
            return [value] if value is not None else []


class TestCaseForm(forms.ModelForm):
    attachments = forms.FileField(
        label='添付ファイル',
        required=False,
        widget=MultipleFileInput(),
        help_text='複数のファイルを選択できます。'
    )

    class Meta:
        model = TestCase
        fields = ['title', 'description', 'preconditions', 'steps', 'expected_result']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Markdownが使用できます',
                'class': 'markdown-editor'
            }),
            'preconditions': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Markdownが使用できます',
                'class': 'markdown-editor'
            }),
            'steps': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Markdownが使用できます',
                'class': 'markdown-editor'
            }),
            'expected_result': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Markdownが使用できます',
                'class': 'markdown-editor'
            }),
        }


class TestPlanForm(forms.ModelForm):
    test_cases = forms.ModelMultipleChoiceField(
        queryset=TestCase.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='テストケース'
    )

    class Meta:
        model = TestPlan
        fields = ['name', 'description', 'test_cases']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            self.fields['test_cases'].queryset = TestCase.objects.filter(
                suite__project=project
            ).select_related('suite').order_by('suite__name', 'title')
            
            if self.instance.pk:
                self.initial['test_cases'] = self.instance.test_cases.all()


class TestRunForm(forms.ModelForm):
    class Meta:
        model = TestRun
        fields = ['name', 'description', 'assigned_to']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['status', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description', 'priority', 'assigned_to']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class TestCaseImportForm(forms.Form):
    csv_file = forms.FileField(
        label='CSVファイル',
        help_text='CSVファイルを選択してください。ヘッダー行には「タイトル」「説明」「前提条件」「テストステップ」「期待される結果」を含める必要があります。'
    ) 