from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField

from .conf import settings
from .fields import HoneyPotField, PasswordField, UsersEmailField,UsernameField,UserphonenumberField
from .models import accessrecord

class UserCreationForm(forms.ModelForm):#用户表单

    error_messages = {
        'duplicate_email': _('该邮箱已被注册.'),
        'password_mismatch': _('两次密码不一致.'),
	}
    email = UsersEmailField(label= _('邮箱地址'), max_length= 255)
    email2 = UsersEmailField(label=_('确认邮箱'),max_length=255)
    password1 = PasswordField(label=_('密码'))
    password2 = PasswordField(
        label=_('确认密码'),
        help_text=_('输入相同的密码，以便确认'))
    name=UsernameField(label=_('用户名'),max_length=30)
    realname=forms.CharField(label=_('真实姓名'),max_length=15)
    sex=forms.ChoiceField(label=_('性别'),choices=(('0',_('男')),('1',_('女'))))
    phonenumber=UserphonenumberField(label=_('手机号码'))
    birth=forms.DateField(label=_('出生日期'))
    captcha = CaptchaField(_('验证码'))
    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_email(self):

        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )
	#检验重复的email
    def clean_email2(self):
        email=self.cleaned_data.get('email')
        email2=self.cleaned_data.get('email2')
        if email and email2 and email!=email2:
            raise forms.ValidationError(
               _("邮箱不匹配"),code="email_mismatch"
        )
    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
	#两次密码不一致
    def clean_name(self):
        name=self.cleaned_data.get('name')
        if len(name)>15:
            raise forms.ValidationError(_('用户名过长'),code='namelong')
        return name
    def clean_realname(self):
        realname=self.cleaned_data['realname']
        if len(realname)==0:
            raise forms.ValidationError(_('姓名不能为空'),code='empty name')
        return realname
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = not settings.USERS_VERIFY_EMAIL
        user.name=self.cleaned_data['name']
        user.sex=self.cleaned_data['sex']
        user.phonenumber=self.cleaned_data['phonenumber']
        user.realname=self.cleaned_data['realname']
        if commit:
            user.save()
        return user

	
class UserChangeForm(forms.ModelForm):
	#只读的哈希字段
    password = ReadOnlyPasswordHashField(label=_('密码'))

    class Meta:
        model = get_user_model()
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)#父对象初始化
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        try:
            return self.initial['password']
        except KeyError:
            pass
            


class RegistrationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'


class RegistrationFormTermsOfService(RegistrationForm):#添加同意条款的单选框
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.

    """
    tos = forms.BooleanField(
        label=_('I have read and agree to the Terms of Service'),
        widget=forms.CheckboxInput,
        error_messages={
            'required': _('You must agree to the terms to register')
        })


class RegistrationFormHoneypot(RegistrationForm):#防止非人类注册
    """
    Subclass of ``RegistrationForm`` which adds a honeypot field
    for Spam Prevention

    """
    accept_terms = HoneyPotField()
