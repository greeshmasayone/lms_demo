# Generated by Django 4.1.5 on 2023-02-16 05:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contents', '0003_alter_quizattempt_user_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_questions', to='contents.question', verbose_name='Question'),
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('total_score', models.PositiveSmallIntegerField(default=0, verbose_name='Mark Percentage')),
                ('user_score', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Score')),
                ('has_passed', models.BooleanField(default=False, verbose_name='Has Passed')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_quiz_results', to='contents.quiz', verbose_name='Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_user_quiz_results', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Quiz Results',
                'verbose_name_plural': 'User Quiz Results',
            },
        ),
    ]