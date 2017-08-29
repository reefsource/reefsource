from django.db import migrations


def convert_to_dict(apps, schema_editor):
    import json

    # We can't import the Result model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Result = apps.get_model('results', 'Result')

    for r in Result.objects.all():
        tmp = r.json
        if isinstance(tmp, str):
            r.json = json.loads(tmp)
            r.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('results', '0010_auto_20170615_0543'),
    ]

    operations = [
        migrations.RunPython(convert_to_dict, noop),
    ]
