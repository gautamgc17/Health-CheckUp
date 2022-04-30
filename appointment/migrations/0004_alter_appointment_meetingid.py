from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_doctor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='meetingId',
            field=models.CharField(max_length=250),
        ),
    ]
