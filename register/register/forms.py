from django import  forms
from phonenumber_field.formfields import PhoneNumberField



class signInForm(forms.Form):
    email = forms.EmailField(label='E-mail' ,required=True)
    password = forms.CharField(widget=forms.PasswordInput())

class signUpForm(forms.Form):
    
    email =  forms.EmailField(label='E-mail \n' ,required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    sname = forms.CharField(label='society_name \n')
    nroom = forms.IntegerField(label='number of rooms \n')

class createForm(forms.Form):
    fname = forms.CharField(label='First Name')
    contact1 =  PhoneNumberField(label='Primary Contact Number')
    contact2 =  PhoneNumberField(label='Secondary Contact Number')
    room = forms.CharField(label='Room Number')
    adhar=forms.RegexField(regex="^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$")
    # adhar = request.POST.get('adhar')
