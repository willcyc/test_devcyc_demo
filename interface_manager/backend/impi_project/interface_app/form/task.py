from django import forms

class TaskForm(forms.Form):
    name = forms.CharField(max_length=200,min_length=1,required=True)
    description = forms.CharField(max_length=500,min_length=1,required=False)