# Generated by Django 4.1.5 on 2023-02-15 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_alter_choices_question_alter_quizattempt_user_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='user_choice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_quiz_answer', to='contents.choices', verbose_name='User Choice'),
        ),
    ]
