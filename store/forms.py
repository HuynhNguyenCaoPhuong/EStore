from django import forms
from . models import Contact

class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=150, label='Name', widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Name',
        'required' : 'required'
    }))
    # name là tên trong field input, TextInput tương ứng type="text", 'class' : 'form-control' tương ứng class="form-control", 'placeholder' : 'Your Name' tương ứng placeholder="Your Name", 'required' : 'required' tương ứng required trong html
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Email',
        'required' : 'required'
    }))
    # EmailField ý nghĩa là xác định đây là dữ liệu email
    subject = forms.CharField(max_length=20, label='Subject', widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Subject',
        'required' : 'required'
    }))
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Message',
        'rows' : '5',
        'required' : 'required'
    }))
    # TextInput chỉ được input một dòng, Textarea có thể input nhiều dong tương ứng với rows 

    class Meta:
        model = Contact
        fields = '__all__'
    # khai báo các field tương ứng vào model Contact, all là tương ứng với tất cả field
    # trường hợp khai báo tương ứng một số field, khai báo tupple hoặc list-> fields = ('name', 'email') or fields = ['name', 'email']