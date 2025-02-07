from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Project, TestSuite, TestCase, TestPlan, TestRun, TestResult, Bug, TestCaseAttachment
from .forms import ProjectForm, TestSuiteForm, TestCaseForm, TestPlanForm, TestRunForm, TestResultForm, BugForm, TestCaseImportForm
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse


@login_required
def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'test_management/project_list.html', {
        'project_list': projects
    })


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'test_management/project_detail.html', {
        'project': project
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'プロジェクトを作成しました。')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'test_management/project_form.html', {
        'form': form
    })


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロジェクトを更新しました。')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'test_management/project_form.html', {
        'form': form
    })


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'プロジェクトを削除しました。')
        return redirect('project_list')
    return render(request, 'test_management/confirm_delete.html', {
        'object': project,
        'object_name': project.name,
        'object_type': 'プロジェクト',
        'back_url': reverse('project_detail', args=[pk])
    })


@login_required
def testsuite_detail(request, pk):
    testsuite = get_object_or_404(TestSuite, pk=pk)
    return render(request, 'test_management/testsuite_detail.html', {
        'testsuite': testsuite
    })


@login_required
def testsuite_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        form = TestSuiteForm(request.POST)
        if form.is_valid():
            testsuite = form.save(commit=False)
            testsuite.project = project
            testsuite.save()
            messages.success(request, 'テストスイートを作成しました。')
            return redirect('testsuite_detail', pk=testsuite.pk)
    else:
        form = TestSuiteForm()
    
    return render(request, 'test_management/testsuite_form.html', {
        'form': form,
        'project': project
    })


@login_required
def testsuite_update(request, pk):
    testsuite = get_object_or_404(TestSuite, pk=pk)
    
    if request.method == 'POST':
        form = TestSuiteForm(request.POST, instance=testsuite)
        if form.is_valid():
            form.save()
            messages.success(request, 'テストスイートを更新しました。')
            return redirect('testsuite_detail', pk=testsuite.pk)
    else:
        form = TestSuiteForm(instance=testsuite)
    
    return render(request, 'test_management/testsuite_form.html', {
        'form': form,
        'project': testsuite.project
    })


@login_required
def testsuite_delete(request, pk):
    testsuite = get_object_or_404(TestSuite, pk=pk)
    if request.method == 'POST':
        project_id = testsuite.project.id
        testsuite.delete()
        messages.success(request, 'テストスイートを削除しました。')
        return redirect('project_detail', pk=project_id)
    return render(request, 'test_management/confirm_delete.html', {
        'object': testsuite,
        'object_name': testsuite.name,
        'object_type': 'テストスイート',
        'back_url': reverse('testsuite_detail', args=[pk])
    })


@login_required
def testcase_detail(request, pk):
    testcase = get_object_or_404(TestCase, pk=pk)
    return render(request, 'test_management/testcase_detail.html', {
        'testcase': testcase
    })


@login_required
def testcase_create(request, testsuite_pk):
    testsuite = get_object_or_404(TestSuite, pk=testsuite_pk)
    
    if request.method == 'POST':
        form = TestCaseForm(request.POST, request.FILES)
        if form.is_valid():
            testcase = form.save(commit=False)
            testcase.suite = testsuite
            testcase.created_by = request.user
            testcase.save()

            # 添付ファイルの処理
            files = request.FILES.getlist('attachments')
            if files:
                for f in files:
                    try:
                        TestCaseAttachment.objects.create(
                            test_case=testcase,
                            file=f,
                            filename=f.name
                        )
                    except Exception as e:
                        messages.error(request, f'ファイル {f.name} のアップロードに失敗しました: {str(e)}')

            messages.success(request, 'テストケースを作成しました。')
            return redirect('testcase_detail', pk=testcase.pk)
    else:
        form = TestCaseForm()
    
    return render(request, 'test_management/testcase_form.html', {
        'form': form,
        'testsuite': testsuite
    })


@login_required
def testcase_update(request, pk):
    testcase = get_object_or_404(TestCase, pk=pk)
    
    if request.method == 'POST':
        form = TestCaseForm(request.POST, request.FILES, instance=testcase)
        if form.is_valid():
            testcase = form.save()

            # 添付ファイルの処理
            files = request.FILES.getlist('attachments')
            if files:
                for f in files:
                    try:
                        TestCaseAttachment.objects.create(
                            test_case=testcase,
                            file=f,
                            filename=f.name
                        )
                    except Exception as e:
                        messages.error(request, f'ファイル {f.name} のアップロードに失敗しました: {str(e)}')

            messages.success(request, 'テストケースを更新しました。')
            return redirect('testcase_detail', pk=testcase.pk)
    else:
        form = TestCaseForm(instance=testcase)
    
    return render(request, 'test_management/testcase_form.html', {
        'form': form,
        'testsuite': testcase.suite,
        'testcase': testcase
    })


@login_required
def testcase_attachment_delete(request, pk):
    attachment = get_object_or_404(TestCaseAttachment, pk=pk)
    testcase_id = attachment.test_case.id
    
    if request.method == 'POST':
        attachment.file.delete()
        attachment.delete()
        messages.success(request, '添付ファイルを削除しました。')
    
    return redirect('testcase_detail', pk=testcase_id)


@login_required
def testcase_duplicate(request, pk):
    source_case = get_object_or_404(TestCase, pk=pk)
    
    if request.method == 'POST':
        form = TestCaseForm(request.POST, request.FILES)
        if form.is_valid():
            new_case = form.save(commit=False)
            new_case.suite = source_case.suite
            new_case.created_by = request.user
            new_case.save()

            # 添付ファイルの複製
            for attachment in source_case.attachments.all():
                TestCaseAttachment.objects.create(
                    test_case=new_case,
                    file=attachment.file,
                    filename=attachment.filename
                )

            messages.success(request, 'テストケースを複製しました。')
            return redirect('testcase_detail', pk=new_case.pk)
    else:
        initial_data = {
            'title': f'{source_case.title} (複製)',
            'description': source_case.description,
            'preconditions': source_case.preconditions,
            'steps': source_case.steps,
            'expected_result': source_case.expected_result,
        }
        form = TestCaseForm(initial=initial_data)
    
    return render(request, 'test_management/testcase_form.html', {
        'form': form,
        'testsuite': source_case.suite,
        'is_duplicate': True,
        'source_case': source_case,
    })


@login_required
def testcase_delete(request, pk):
    testcase = get_object_or_404(TestCase, pk=pk)
    if request.method == 'POST':
        suite_id = testcase.suite.id
        testcase.delete()
        messages.success(request, 'テストケースを削除しました。')
        return redirect('testsuite_detail', pk=suite_id)
    return render(request, 'test_management/confirm_delete.html', {
        'object': testcase,
        'object_name': testcase.title,
        'object_type': 'テストケース',
        'back_url': reverse('testcase_detail', args=[pk])
    })


@login_required
def testplan_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        form = TestPlanForm(project, request.POST)
        if form.is_valid():
            testplan = form.save(commit=False)
            testplan.project = project
            testplan.created_by = request.user
            testplan.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'テストプランを作成しました。')
            return redirect('testplan_detail', pk=testplan.pk)
    else:
        form = TestPlanForm(project)
    
    return render(request, 'test_management/testplan_form.html', {
        'form': form,
        'project': project
    })


@login_required
def testplan_detail(request, pk):
    testplan = get_object_or_404(TestPlan, pk=pk)
    return render(request, 'test_management/testplan_detail.html', {
        'testplan': testplan
    })


@login_required
def testplan_update(request, pk):
    testplan = get_object_or_404(TestPlan, pk=pk)
    
    if request.method == 'POST':
        form = TestPlanForm(testplan.project, request.POST, instance=testplan)
        if form.is_valid():
            form.save()
            messages.success(request, 'テストプランを更新しました。')
            return redirect('testplan_detail', pk=testplan.pk)
    else:
        form = TestPlanForm(testplan.project, instance=testplan)
    
    return render(request, 'test_management/testplan_form.html', {
        'form': form,
        'project': testplan.project
    })


@login_required
def testplan_delete(request, pk):
    testplan = get_object_or_404(TestPlan, pk=pk)
    if request.method == 'POST':
        project_id = testplan.project.id
        testplan.delete()
        messages.success(request, 'テストプランを削除しました。')
        return redirect('project_detail', pk=project_id)
    return render(request, 'test_management/confirm_delete.html', {
        'object': testplan,
        'object_name': testplan.name,
        'object_type': 'テストプラン',
        'back_url': reverse('testplan_detail', args=[pk])
    })


@login_required
def testrun_create(request, testplan_pk):
    testplan = get_object_or_404(TestPlan, pk=testplan_pk)
    
    if request.method == 'POST':
        form = TestRunForm(request.POST)
        if form.is_valid():
            testrun = form.save(commit=False)
            testrun.test_plan = testplan
            testrun.save()
            messages.success(request, 'テスト実行を作成しました。')
            return redirect('testrun_detail', pk=testrun.pk)
    else:
        form = TestRunForm()
    
    return render(request, 'test_management/testrun_form.html', {
        'form': form,
        'testplan': testplan
    })


@login_required
def testrun_detail(request, pk):
    testrun = get_object_or_404(TestRun, pk=pk)
    
    # テストケースごとの最新の結果を取得
    test_cases = testrun.test_plan.test_cases.all()
    results = {}
    for case in test_cases:
        result = TestResult.objects.filter(
            test_run=testrun,
            test_case=case
        ).first()
        if result:
            results[case.id] = result
    
    return render(request, 'test_management/testrun_detail.html', {
        'testrun': testrun,
        'results': results
    })


@login_required
def testrun_update(request, pk):
    testrun = get_object_or_404(TestRun, pk=pk)
    
    if request.method == 'POST':
        form = TestRunForm(request.POST, instance=testrun)
        if form.is_valid():
            form.save()
            messages.success(request, 'テスト実行を更新しました。')
            return redirect('testrun_detail', pk=testrun.pk)
    else:
        form = TestRunForm(instance=testrun)
    
    return render(request, 'test_management/testrun_form.html', {
        'form': form,
        'testplan': testrun.test_plan
    })


@login_required
def testrun_delete(request, pk):
    testrun = get_object_or_404(TestRun, pk=pk)
    if request.method == 'POST':
        plan_id = testrun.test_plan.id
        testrun.delete()
        messages.success(request, 'テスト実行を削除しました。')
        return redirect('testplan_detail', pk=plan_id)
    return render(request, 'test_management/confirm_delete.html', {
        'object': testrun,
        'object_name': testrun.name,
        'object_type': 'テスト実行',
        'back_url': reverse('testrun_detail', args=[pk])
    })


@login_required
def testresult_create(request, testrun_pk, testcase_pk):
    testrun = get_object_or_404(TestRun, pk=testrun_pk)
    testcase = get_object_or_404(TestCase, pk=testcase_pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        comment = request.POST.get('comment')
        
        # 既存の結果があれば更新、なければ新規作成
        result, created = TestResult.objects.update_or_create(
            test_run=testrun,
            test_case=testcase,
            defaults={
                'status': status,
                'comment': comment,
                'executed_by': request.user
            }
        )
        
        messages.success(request, 'テスト結果を記録しました。')
        
        # テスト実行のステータスを更新
        if testrun.status == 'not_started':
            testrun.status = 'in_progress'
            testrun.save()
        
        # すべてのテストケースが実行済みの場合、テスト実行を完了状態に
        total_cases = testrun.test_plan.test_cases.count()
        executed_cases = testrun.testresult_set.count()
        if total_cases == executed_cases:
            testrun.status = 'completed'
            testrun.save()
    
    return redirect('testrun_detail', pk=testrun_pk)


@login_required
def bug_create(request, testresult_pk):
    test_result = get_object_or_404(TestResult, pk=testresult_pk)
    
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.test_result = test_result
            bug.created_by = request.user
            bug.save()
            messages.success(request, '不具合を起票しました。')
            return redirect('testrun_detail', pk=test_result.test_run.id)
    else:
        # テストケースの情報から初期値を設定
        initial = {
            'title': f'[不具合] {test_result.test_case.title}',
            'description': f'''
テストケース: {test_result.test_case.title}
テストスイート: {test_result.test_case.suite.name}

【期待される結果】
{test_result.test_case.expected_result}

【実際の結果】
{test_result.comment}
'''.strip()
        }
        form = BugForm(initial=initial)
    
    return render(request, 'test_management/bug_form.html', {
        'form': form,
        'test_result': test_result
    })


@login_required
def bug_detail(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    
    if request.method == 'POST':
        # ステータスの更新
        new_status = request.POST.get('status')
        if new_status and new_status in dict(Bug.STATUS_CHOICES):
            bug.status = new_status
            bug.save()
            messages.success(request, '不具合のステータスを更新しました。')
            return redirect('bug_detail', pk=bug.pk)
    
    return render(request, 'test_management/bug_detail.html', {
        'bug': bug,
        'status_choices': Bug.STATUS_CHOICES,
    })


@login_required
def bug_update(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    
    if request.method == 'POST':
        form = BugForm(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            messages.success(request, '不具合を更新しました。')
            return redirect('bug_detail', pk=bug.pk)
    else:
        form = BugForm(instance=bug)
    
    return render(request, 'test_management/bug_form.html', {
        'form': form,
        'bug': bug,
        'is_update': True
    })


@login_required
def bug_delete(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    if request.method == 'POST':
        project_id = bug.test_result.test_run.test_plan.project.id
        bug.delete()
        messages.success(request, 'バグを削除しました。')
        return redirect('project_bugs', project_pk=project_id)
    return render(request, 'test_management/confirm_delete.html', {
        'object': bug,
        'object_name': bug.title,
        'object_type': 'バグ',
        'back_url': reverse('bug_detail', args=[pk])
    })


@login_required
def dashboard(request):
    # プロジェクト数
    total_projects = Project.objects.count()
    
    # テスト実行の状況
    test_runs = TestRun.objects.all()
    total_runs = test_runs.count()
    completed_runs = test_runs.filter(status='completed').count()
    in_progress_runs = test_runs.filter(status='in_progress').count()
    
    # テスト結果の集計
    test_results = TestResult.objects.all()
    total_results = test_results.count()
    results_by_status = {
        'passed': test_results.filter(status='passed').count(),
        'failed': test_results.filter(status='failed').count(),
        'blocked': test_results.filter(status='blocked').count(),
        'skipped': test_results.filter(status='skipped').count(),
    }
    
    # 不具合の状況
    bugs = Bug.objects.all()
    total_bugs = bugs.count()
    bugs_by_status = {
        'open': bugs.filter(status='open').count(),
        'in_progress': bugs.filter(status='in_progress').count(),
        'resolved': bugs.filter(status='resolved').count(),
        'closed': bugs.filter(status='closed').count(),
    }
    bugs_by_priority = {
        'critical': bugs.filter(priority='critical').count(),
        'high': bugs.filter(priority='high').count(),
        'medium': bugs.filter(priority='medium').count(),
        'low': bugs.filter(priority='low').count(),
    }
    
    # 最近の不具合
    recent_bugs = bugs.order_by('-created_at')[:5]
    
    # 最近のテスト実行
    recent_runs = test_runs.order_by('-created_at')[:5]
    
    context = {
        'total_projects': total_projects,
        'total_runs': total_runs,
        'completed_runs': completed_runs,
        'in_progress_runs': in_progress_runs,
        'total_results': total_results,
        'results_by_status': results_by_status,
        'total_bugs': total_bugs,
        'bugs_by_status': bugs_by_status,
        'bugs_by_priority': bugs_by_priority,
        'recent_bugs': recent_bugs,
        'recent_runs': recent_runs,
    }
    
    return render(request, 'test_management/dashboard.html', context)


@login_required
def project_bugs(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    bugs = Bug.objects.filter(
        test_result__test_run__test_plan__project=project
    ).order_by('-created_at')
    
    # ステータスでフィルタリング
    status = request.GET.get('status')
    if status:
        bugs = bugs.filter(status=status)
    
    # 優先度でフィルタリング
    priority = request.GET.get('priority')
    if priority:
        bugs = bugs.filter(priority=priority)
    
    # 担当者でフィルタリング
    assigned_to = request.GET.get('assigned_to')
    if assigned_to:
        bugs = bugs.filter(assigned_to_id=assigned_to)
    
    context = {
        'project': project,
        'bugs': bugs,
        'status_choices': Bug.STATUS_CHOICES,
        'priority_choices': Bug.PRIORITY_CHOICES,
    }
    
    return render(request, 'test_management/project_bugs.html', context)


@login_required
def testcase_export(request, testsuite_pk):
    testsuite = get_object_or_404(TestSuite, pk=testsuite_pk)
    testcases = TestCase.objects.filter(suite=testsuite)
    
    # CSVファイル名の設定
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename = f'testcases_{testsuite.name}_{timestamp}.csv'
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # CSV書き込み
    writer = csv.writer(response)
    writer.writerow(['タイトル', '説明', '前提条件', 'テストステップ', '期待される結果'])
    
    for testcase in testcases:
        writer.writerow([
            testcase.title,
            testcase.description,
            testcase.preconditions,
            testcase.steps,
            testcase.expected_result,
        ])
    
    return response


@login_required
def testcase_import(request, testsuite_pk):
    testsuite = get_object_or_404(TestSuite, pk=testsuite_pk)
    
    if request.method == 'POST':
        form = TestCaseImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'CSVファイルを選択してください。')
                return redirect('testsuite_detail', pk=testsuite_pk)
            
            # CSVファイルの読み込み
            try:
                decoded_file = csv_file.read().decode('utf-8-sig')
                reader = csv.DictReader(decoded_file.splitlines())
                
                required_fields = ['タイトル', '説明', '前提条件', 'テストステップ', '期待される結果']
                if not all(field in reader.fieldnames for field in required_fields):
                    messages.error(request, '必要なヘッダーが含まれていません。')
                    return redirect('testsuite_detail', pk=testsuite_pk)
                
                import_count = 0
                for row in reader:
                    TestCase.objects.create(
                        suite=testsuite,
                        title=row['タイトル'],
                        description=row['説明'],
                        preconditions=row['前提条件'],
                        steps=row['テストステップ'],
                        expected_result=row['期待される結果'],
                        created_by=request.user
                    )
                    import_count += 1
                
                messages.success(request, f'{import_count}件のテストケースをインポートしました。')
                
            except (ValidationError, csv.Error, UnicodeDecodeError) as e:
                messages.error(request, f'CSVファイルの読み込みに失敗しました: {str(e)}')
            
            return redirect('testsuite_detail', pk=testsuite_pk)
    else:
        form = TestCaseImportForm()
    
    return render(request, 'test_management/testcase_import.html', {
        'form': form,
        'testsuite': testsuite
    })


@login_required
def testcase_history(request, pk):
    testcase = get_object_or_404(TestCase, pk=pk)
    histories = testcase.history.all().order_by('-version')
    
    if request.method == 'POST':
        version = request.POST.get('version')
        if version:
            try:
                version = int(version)
                if testcase.revert_to_version(version):
                    messages.success(request, f'テストケースをバージョン{version}に戻しました。')
                else:
                    messages.error(request, '指定されたバージョンが見つかりません。')
            except ValueError:
                messages.error(request, '無効なバージョン番号です。')
        return redirect('testcase_detail', pk=pk)
    
    return render(request, 'test_management/testcase_history.html', {
        'testcase': testcase,
        'histories': histories
    })
