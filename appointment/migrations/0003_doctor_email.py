from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_alter_appointment_options_appointment_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
