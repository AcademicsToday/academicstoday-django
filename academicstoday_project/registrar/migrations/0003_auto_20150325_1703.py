# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_auto_20150325_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(max_length=127, choices=[('Aeronautics & Astronautics', 'Aeronautics & Astronautics'), ('Anesthesia', 'Anesthesia'), ('Anthropology', 'Anthropology'), ('Applied Physics', 'Applied Physics'), ('Art or Art History', 'Art & Art History'), ('Astrophysics', 'Astrophysics'), ('Biochemistry', 'Biochemistry'), ('Bioengineering', 'Bioengineering'), ('Biology', 'Biology'), ('Business', 'Business'), ('Cardiothoracic Surgery', 'Cardiothoracic Surgery'), ('Chemical and Systems Biology', 'Chemical and Systems Biology'), ('Chemical Engineering', 'Chemical Engineering'), ('Chemistry', 'Chemistry'), ('Civil and Environmental Engineering', 'Civil and Environmental Engineering'), ('Classics', 'Classics'), ('Communication', 'Communication'), ('Comparative Literature', 'Comparative Literature'), ('Comparative Medicine', 'Comparative Medicine'), ('Computer Science', 'Computer Science'), ('Dermatology', 'Dermatology'), ('Developmental Biology', 'Developmental Biology'), ('East Asian Languages and Cultures', 'East Asian Languages and Cultures'), ('Economics', 'Economics'), ('Education', 'Education'), ('Electrical Engineering', 'Electrical Engineering'), ('English', 'English'), ('French', 'French'), ('Genetics', 'Genetics'), ('Geological and Environmental Sciences', 'Geological and Environmental Sciences'), ('Geophysics', 'Geophysics'), ('Health', 'Health'), ('History', 'History'), ('Latin American Cultures', 'Latin American Cultures'), ('Law School', 'Law School'), ('Linguistics', 'Linguistics'), ('Management', 'Management'), ('Materials Science', 'Materials Science'), ('Mathematics', 'Mathematics'), ('Mechanical Engineering', 'Mechanical Engineering'), ('Medicine', 'Medicine'), ('Microbiology and Immunology', 'Microbiology and Immunology'), ('Molecular and Cellular Physiology', 'Molecular and Cellular Physiology'), ('Music', 'Music'), ('Neurobiology', 'Neurobiology'), ('Neurology', 'Neurology'), ('Neurosurgery', 'Neurosurgery'), ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'), ('Ophthalmology', 'Ophthalmology'), ('Orthopaedic Surgery', 'Orthopaedic Surgery'), ('Other', 'Other'), ('Otolaryngology', 'Otolaryngology'), ('Pathology', 'Pathology'), ('Pediatrics', 'Pediatrics'), ('Philosophy', 'Philosophy'), ('Physics', 'Physics'), ('Political Science', 'Political Science'), ('Psychiatry', 'Psychiatry'), ('Psychology', 'Psychology'), ('Radiation Oncology', 'Radiation Oncology'), ('Radiology', 'Radiology'), ('Religious Studies', 'Religious Studies'), ('Slavic Languages and Literature', 'Slavic Languages and Literature'), ('Sociology', 'Sociology'), ('Statistics', 'Statistics'), ('Surgery', 'Surgery'), ('Theater and Performance Studies', 'Theater and Performance Studies'), ('Urology', 'Urology')]),
            preserve_default=True,
        ),
    ]
