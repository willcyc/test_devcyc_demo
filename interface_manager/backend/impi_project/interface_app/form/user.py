from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=20,
                               min_length=3,
                               required=True,
                               error_messages={'required':'用户名不能为空！'})

    password = forms.CharField(max_length=20,
                               min_length=3,
                               required=True,
                               error_messages={'required':'密码不能为空！'})

    #num = forms.IntegerField(min_value=10,required=False)

    # def clean_username(self):
    #     pass
    #
    # def clean_password(self):
    #     pass
    # def clean(self):
    #     pass