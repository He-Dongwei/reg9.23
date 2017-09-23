from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from .models import accessrecord
from .compat import urlsafe_base64_decode
from .conf import settings,UsersAppConf
from .signals import user_activated, user_registered
from .utils import EmailActivationTokenGenerator, send_activation_email

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site


if UsersAppConf.USERS_SPAM_PROTECTION:  # pragma: no cover
    from .forms import RegistrationFormTermsOfService as RegistrationForm
else:
    from .forms import RegistrationForm


@csrf_protect
@never_cache
def register(request,
             template_name='users/registration_form.html',#模板文件
             activation_email_template_name='users/activation_email.html',#邮件内容
             activation_email_subject_template_name='users/activation_email_subject.html',#标题
             activation_email_html_template_name=None,
             registration_form=RegistrationForm,#表单
             registered_user_redirect_to=None,#注册用户跳转
             post_registration_redirect=None,
             activation_from_email=None,
             current_app=None,
             extra_context=None):#附加说明

    if registered_user_redirect_to is None:
        registered_user_redirect_to = getattr(settings, 'LOGIN_REDIRECT_URL')#登陆后跳转控制

    if request.user.is_authenticated():
            return redirect(registered_user_redirect_to)#如果已有用户登录，则跳转

    if not settings.USERS_REGISTRATION_OPEN:
        return redirect(reverse('users_registration_closed'))#注册功能关闭，则跳转注册关闭页面

    if post_registration_redirect is None:
        post_registration_redirect = reverse('users_registration_complete')#注册后跳转页面

    if request.method == 'POST':
        form = registration_form(request.POST)#获取表单
        if form.is_valid():#表单没有错误
            user = form.save()#返回用户实例
            if settings.USERS_AUTO_LOGIN_AFTER_REGISTRATION:#注册后自动登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            elif not user.is_active and settings.USERS_VERIFY_EMAIL:#用户没有激活并且需要邮箱验证
                opts = {
                    'user': user,#用户
                    'request': request,#请求
                    'from_email': activation_from_email,
                    'email_template': activation_email_template_name,#邮件内容模板
                    'subject_template': activation_email_subject_template_name,#邮件标题模板
                    'html_email_template': activation_email_html_template_name,
                }
                send_activation_email(**opts)#发送注册邮件
                user_registered.send(sender=user.__class__, request=request, user=user)
            return redirect(post_registration_redirect)
    else:
        form = registration_form()

    current_site = get_current_site(request)#取得请求的主机名

    context = {
        'form': form,#表单
        'site': current_site,#当前的主机名
        'site_name': current_site.name,#域名？？？
        'title': _('Register'),#标题
    }

    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    if request.GET.get('newsn')=='1':
        csn=CaptchaStore.generate_key()
        cimageurl= captcha_image_url(csn)
        return HttpResponse(cimageurl)
    return TemplateResponse(request, template_name, context)


def registration_closed(request,
                        template_name='users/registration_closed.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': _('Registration closed'),#标题
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)

@csrf_protect
def registration_complete(request,
                          template_name='users/registration_complete.html',
                          current_app=None,
                          extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),#获取url_name
        'title': _('Registration complete'),
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


@never_cache
def activate(request,
             uidb64=None,#用户主码id
             token=None,#令牌号
             template_name='users/activate.html',
             post_activation_redirect=None,
             current_app=None,
             extra_context=None):

    context = {
        'title': _('Account activation '),
    }

    if post_activation_redirect is None:
        post_activation_redirect = reverse('users_activation_complete')#激活后重定向

    UserModel = get_user_model()#使用用户自定义的用户模型
    assert uidb64 is not None and token is not None#断言用户ID及令牌不为空

    token_generator = EmailActivationTokenGenerator()#令牌产生器

    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.activate()
        user_activated.send(sender=user.__class__, request=request, user=user)
        if settings.USERS_AUTO_LOGIN_ON_ACTIVATION:#激活后自动登录
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # todo - remove this hack
            login(request, user)
            messages.info(request, 'Thanks for registering. You are now logged in.')
        return redirect(post_activation_redirect)#激活后重定向
    else:
        title = _('Email confirmation unsuccessful')
        context = {
            'title': title,
        }

    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


def activation_complete(request,
                        template_name='users/activation_complete.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': _('Activation complete'),
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)
@login_required
def index(request):
	Internetrecord.objects.create(page=request.get_full_path(),IP=request.META['REMOTE_ADDR'])
	return render(request,'index.html')