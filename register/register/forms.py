from django import  forms
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from camera_imagefield import CameraImageField
from fractions import Fraction
from webcam.fields import CameraField



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
    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)
 
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = "createForm"
        self.helper.form_method = 'post'
 
        super(createForm, self).__init__(*args, **kwargs)
    
    
    # adhar = request.POST.get('adhar')
