from django import forms
from project_app.models import Module
from interface_app.models import TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['module']
        #exclude = ['create_time']