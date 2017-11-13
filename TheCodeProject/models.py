# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class codes(models.Model):
    username = models.TextField()
    code_id = models.TextField()
    code_content = models.TextField()
    lang = models.TextField()
    code_input = models.TextField()
    compile_status= models.TextField()
    run_status_status=models.TextField()
    run_status_time=models.TextField()
    run_status_memory=models.TextField()
    run_status_output=models.TextField()
    run_status_stderr=models.TextField()
