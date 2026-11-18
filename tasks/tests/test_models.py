from django.test import TestCase
from datetime import date
from tasks.models import Task, TaskList, Tag, RecurringTask

class TaskTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title = 'call',
            slug = 'call',
            description = 'call',
            deadline = date(2026, 11, 20)
        )
        
        self.tag = Tag.objects.create(title = 'call')

    def test_task_created(self):
        self.assertEqual(Task.objects.count(), 1)

    def test_task_fields_saved(self):
        self.assertEqual(self.task.title, 'call')
        self.assertEqual(self.task.description, 'call')
        self.assertEqual(self.task.slug, 'call')
        self.assertEqual(self.task.deadline, date(2026, 11, 20))

    def test_task_has_defaults(self):
        self.assertFalse(self.task.done)
        self.assertEqual(self.task.priority, Task.Priority.MEDIUM)
        self.assertIsNone(self.task.task_list)        

    def test_task_has_no_tag(self):
        self.assertEqual(self.task.tags.count(), 0)

    def test_task_has_tag(self):
        self.task.tags.add(self.tag)
        self.assertEqual(self.task.tags.count(), 1)
    
    def test_slug_not_equal(self):
        self.task2 = Task.objects.create(
            title = 'call',
            description = 'call',
            deadline = date(2026, 11, 20)
        )
        self.assertNotEqual(self.task.slug, self.task2.slug)

    def test_delete_task_list(self):
        self.category = TaskList.objects.create(
            title = 'study'
        )

        self.task4 = Task.objects.create(
            title = 'django',
            slug = 'django',
            description = 'django',
            deadline = date(2026, 11, 30),
            task_list = self.category,
        )

        self.category.delete()
        self.assertTrue(Task.objects.filter(pk=self.task4.pk).exists())
        self.task4.refresh_from_db()
        self.assertIsNone(self.task4.task_list)
    
    def test_ordering(self):
        self.task3 = Task.objects.create(
            title = 'call',
            description = 'call',
            deadline = date(2026, 11, 25)
        )

        tasks = Task.objects.all()

        self.assertEqual(tasks[0], self.task)
        self.assertEqual(tasks[1], self.task3)

    def test_str(self):
        self.assertEqual(str(self.task), 'call')


class RecurringTaskTest(TestCase):
    def setUp(self):

        self.recurring_task = RecurringTask.objects.create(
            title='english',
            description='learn phrasal verbs',
            deadline=date(2026, 11, 19),
            periodicity_days=7,
            previous_task = None,
        )

        self.recurring_task2 = RecurringTask.objects.create(
            title='english',
            description='learn phrasal verbs',
            deadline=date(2026, 11, 19),
            periodicity_days=7,
            previous_task = self.recurring_task
        )

    def test_recurring_task_created(self):
        self.assertIsNotNone(self.recurring_task)
    
    def test_periodicity_days(self):
        self.assertEqual(self.recurring_task.periodicity_days, 7)

    def test_task_inheritance(self):
        self.assertEqual(self.recurring_task.title, 'english')
        self.assertEqual(self.recurring_task.description, 'learn phrasal verbs')
        self.assertEqual(self.recurring_task.deadline, date(2026, 11, 19))
    
    def test_default_values(self):
        self.assertEqual(self.recurring_task.priority, Task.Priority.MEDIUM)
        self.assertFalse(self.recurring_task.done)

    def test_previous_task_is_none(self):
        self.assertIsNone(self.recurring_task.previous_task)

    def test_previous_task_exists(self):
        self.assertEqual(self.recurring_task2.previous_task, self.recurring_task)
    
    def test_next_tasks(self):
        all_tasks = self.recurring_task.next_tasks.all()
        self.assertIn(self.recurring_task2, all_tasks)

    def test_delete_previous_task(self):
        self.recurring_task.delete()
        self.recurring_task2.refresh_from_db()
        self.assertIsNone(self.recurring_task2.previous_task)

    def test_str(self):
         self.assertEqual(str(self.recurring_task), 'english')