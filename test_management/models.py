from django.db import models
from django.contrib.auth.models import User
import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import xml.etree.ElementTree as etree
import difflib


class TailwindTreeprocessor(Treeprocessor):
    def run(self, root):
        for element in root.iter():
            if element.tag == 'h1':
                element.set('class', 'text-2xl font-bold mb-4')
            elif element.tag == 'h2':
                element.set('class', 'text-xl font-bold mb-3')
            elif element.tag == 'h3':
                element.set('class', 'text-lg font-bold mb-2')
            elif element.tag == 'p':
                element.set('class', 'mb-4')
            elif element.tag == 'ul':
                element.set('class', 'list-disc list-inside mb-4')
            elif element.tag == 'ol':
                element.set('class', 'list-decimal list-inside mb-4')
            elif element.tag == 'li':
                element.set('class', 'mb-1')
            elif element.tag == 'a':
                element.set('class', 'text-primary hover:text-primary-dark')
            elif element.tag == 'code':
                element.set('class', 'bg-gray-100 px-1 py-0.5 rounded')
            elif element.tag == 'pre':
                element.set('class', 'bg-gray-100 p-4 rounded-lg mb-4')
            elif element.tag == 'blockquote':
                element.set('class', 'border-l-4 border-gray-300 pl-4 mb-4')
            elif element.tag == 'hr':
                element.set('class', 'my-4 border-t border-gray-200')
            elif element.tag == 'table':
                element.set('class', 'min-w-full divide-y divide-gray-200 mb-4')
            elif element.tag == 'thead':
                element.set('class', 'bg-gray-50')
            elif element.tag == 'th':
                element.set('class', 'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider')
            elif element.tag == 'td':
                element.set('class', 'px-6 py-4 whitespace-nowrap text-sm text-gray-900')
        return root


class TailwindExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(TailwindTreeprocessor(md), 'tailwind', 175)


class Project(models.Model):
    name = models.CharField('プロジェクト名', max_length=200)
    description = models.TextField('説明', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'プロジェクト'
        verbose_name_plural = 'プロジェクト'


class TestSuite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='プロジェクト')
    name = models.CharField('スイート名', max_length=200)
    description = models.TextField('説明', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

    class Meta:
        verbose_name = 'テストスイート'
        verbose_name_plural = 'テストスイート'


class TestCaseAttachment(models.Model):
    test_case = models.ForeignKey('TestCase', on_delete=models.CASCADE, related_name='attachments', verbose_name='テストケース')
    file = models.FileField('ファイル', upload_to='test_case_attachments/%Y/%m/%d/')
    filename = models.CharField('ファイル名', max_length=255)
    uploaded_at = models.DateTimeField('アップロード日時', auto_now_add=True)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = 'テストケース添付ファイル'
        verbose_name_plural = 'テストケース添付ファイル'


class TestCase(models.Model):
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE, verbose_name='テストスイート')
    title = models.CharField('タイトル', max_length=200)
    description = models.TextField('説明', blank=True)
    preconditions = models.TextField('前提条件', blank=True)
    steps = models.TextField('テストステップ')
    expected_result = models.TextField('期待される結果')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='作成者')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    current_version = models.IntegerField('現在のバージョン', default=1)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            # 既存のテストケースが更新される場合
            old_instance = TestCase.objects.get(pk=self.pk)
            if (old_instance.title != self.title or
                old_instance.description != self.description or
                old_instance.preconditions != self.preconditions or
                old_instance.steps != self.steps or
                old_instance.expected_result != self.expected_result):
                # 内容が変更された場合のみ履歴を作成
                def generate_diff(old_text, new_text):
                    """2つのテキスト間の差分を生成する"""
                    if old_text == new_text:
                        return ''
                    d = difflib.Differ()
                    diff = list(d.compare(old_text.splitlines(), new_text.splitlines()))
                    return '\n'.join(line for line in diff if line.startswith(('+ ', '- ', '  ')))

                self.current_version += 1
                TestCaseHistory.objects.create(
                    test_case=self,
                    title_diff=generate_diff(old_instance.title, self.title),
                    description_diff=generate_diff(old_instance.description, self.description),
                    preconditions_diff=generate_diff(old_instance.preconditions, self.preconditions),
                    steps_diff=generate_diff(old_instance.steps, self.steps),
                    expected_result_diff=generate_diff(old_instance.expected_result, self.expected_result),
                    changed_by=self.created_by,
                    version=self.current_version - 1
                )
        super().save(*args, **kwargs)
        if is_new:
            # 新規作成時は初期バージョンを履歴として保存
            TestCaseHistory.objects.create(
                test_case=self,
                title_diff=f"+ {self.title}",
                description_diff='\n'.join(f"+ {line}" for line in self.description.splitlines()) if self.description else '',
                preconditions_diff='\n'.join(f"+ {line}" for line in self.preconditions.splitlines()) if self.preconditions else '',
                steps_diff='\n'.join(f"+ {line}" for line in self.steps.splitlines()) if self.steps else '',
                expected_result_diff='\n'.join(f"+ {line}" for line in self.expected_result.splitlines()) if self.expected_result else '',
                changed_by=self.created_by,
                version=1
            )

    def get_description_as_markdown(self):
        return markdown.markdown(self.description or '', extensions=['extra', 'nl2br', 'sane_lists', 'tables', TailwindExtension()])

    def get_preconditions_as_markdown(self):
        return markdown.markdown(self.preconditions or '', extensions=['extra', 'nl2br', 'sane_lists', 'tables', TailwindExtension()])

    def get_steps_as_markdown(self):
        return markdown.markdown(self.steps or '', extensions=['extra', 'nl2br', 'sane_lists', 'tables', TailwindExtension()])

    def get_expected_result_as_markdown(self):
        return markdown.markdown(self.expected_result or '', extensions=['extra', 'nl2br', 'sane_lists', 'tables', TailwindExtension()])

    def revert_to_version(self, version):
        try:
            history = self.history.get(version=version)
            self.title = history.get_title()
            self.description = history.get_description()
            self.preconditions = history.get_preconditions()
            self.steps = history.get_steps()
            self.expected_result = history.get_expected_result()
            self.save()
            return True
        except TestCaseHistory.DoesNotExist:
            return False

    class Meta:
        verbose_name = 'テストケース'
        verbose_name_plural = 'テストケース'


class TestCaseHistory(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='history', verbose_name='テストケース')
    title_diff = models.TextField('タイトルの差分', blank=True)
    description_diff = models.TextField('説明の差分', blank=True)
    preconditions_diff = models.TextField('前提条件の差分', blank=True)
    steps_diff = models.TextField('テストステップの差分', blank=True)
    expected_result_diff = models.TextField('期待される結果の差分', blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='変更者')
    changed_at = models.DateTimeField('変更日時', auto_now_add=True)
    change_comment = models.TextField('変更コメント', blank=True)
    version = models.IntegerField('バージョン')

    def __str__(self):
        return f"{self.test_case.title} - v{self.version}"

    class Meta:
        verbose_name = 'テストケース履歴'
        verbose_name_plural = 'テストケース履歴'
        ordering = ['-version']

    def apply_diff(self, text, diff):
        """差分を適用してテキストを復元する"""
        if not diff:
            return text
        patches = diff.split('\n')
        lines = text.split('\n')
        result_lines = []
        i = 0
        for patch in patches:
            if patch.startswith('+'):
                result_lines.append(patch[1:])
            elif patch.startswith('-'):
                i += 1
            else:
                if i < len(lines):
                    result_lines.append(lines[i])
                i += 1
        return '\n'.join(result_lines)

    def get_title(self):
        """タイトルを復元する"""
        return self.apply_diff(self.test_case.title, self.title_diff)

    def get_description(self):
        """説明を復元する"""
        return self.apply_diff(self.test_case.description, self.description_diff)

    def get_preconditions(self):
        """前提条件を復元する"""
        return self.apply_diff(self.test_case.preconditions, self.preconditions_diff)

    def get_steps(self):
        """テストステップを復元する"""
        return self.apply_diff(self.test_case.steps, self.steps_diff)

    def get_expected_result(self):
        """期待される結果を復元する"""
        return self.apply_diff(self.test_case.expected_result, self.expected_result_diff)


class TestPlan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='プロジェクト')
    name = models.CharField('プラン名', max_length=200)
    description = models.TextField('説明', blank=True)
    test_cases = models.ManyToManyField(TestCase, through='TestPlanCase', verbose_name='テストケース')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='作成者')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'テストプラン'
        verbose_name_plural = 'テストプラン'


class TestPlanCase(models.Model):
    test_plan = models.ForeignKey(TestPlan, on_delete=models.CASCADE, verbose_name='テストプラン')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='テストケース')
    order = models.IntegerField('実行順序', default=0)

    class Meta:
        verbose_name = 'テストプランケース'
        verbose_name_plural = 'テストプランケース'
        ordering = ['order']


class TestRun(models.Model):
    STATUS_CHOICES = [
        ('not_started', '未開始'),
        ('in_progress', '実行中'),
        ('completed', '完了'),
    ]

    test_plan = models.ForeignKey(TestPlan, on_delete=models.CASCADE, verbose_name='テストプラン')
    name = models.CharField('実行名', max_length=200)
    description = models.TextField('説明', blank=True)
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='not_started')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='担当者')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'テスト実行'
        verbose_name_plural = 'テスト実行'


class TestResult(models.Model):
    STATUS_CHOICES = [
        ('passed', '合格'),
        ('failed', '不合格'),
        ('blocked', 'ブロック'),
        ('skipped', 'スキップ'),
    ]

    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE, verbose_name='テスト実行')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='テストケース')
    status = models.CharField('結果', max_length=20, choices=STATUS_CHOICES)
    comment = models.TextField('コメント', blank=True)
    executed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='実行者')
    executed_at = models.DateTimeField('実行日時', auto_now_add=True)

    def __str__(self):
        return f"{self.test_case.title} - {self.get_status_display()}"

    class Meta:
        verbose_name = 'テスト結果'
        verbose_name_plural = 'テスト結果'


class Bug(models.Model):
    PRIORITY_CHOICES = [
        ('critical', '最重要'),
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    ]

    STATUS_CHOICES = [
        ('open', '未対応'),
        ('in_progress', '対応中'),
        ('resolved', '解決済み'),
        ('closed', '完了'),
    ]

    title = models.CharField('タイトル', max_length=200)
    description = models.TextField('説明')
    priority = models.CharField('優先度', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='open')
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, verbose_name='テスト結果')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_bugs', verbose_name='起票者')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bugs', verbose_name='担当者')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '不具合'
        verbose_name_plural = '不具合'
