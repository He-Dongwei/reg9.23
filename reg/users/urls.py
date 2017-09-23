from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views import static
from reg import settings
from django.urls import reverse, reverse_lazy
from .views import (activate, activation_complete, register,
                    registration_closed, registration_complete ,index)

urlpatterns = [
    url(r'^register/$', register, name='users_register'),
	#注册
    url(r'^register/closed/$', registration_closed,
        name='users_registration_closed'),
	#注册关闭
    url(r'^register/complete/$', registration_complete,
        name='users_registration_complete'),
	#注册完成
    url(r'^activate/complete/$', activation_complete,
        name='users_activation_complete'),
	#激活完成
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='users_activate'),

    url(r'^login/$', auth_views.LoginView.as_view(
        template_name='users/login.html'),
        name='users_login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(
        template_name='users/logout.html',next_page='users_login'),

        name='users_logout'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
        name='users_password_change_done'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url=reverse_lazy('users_password_change_done')),
        name='users_password_change'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.html',
            success_url=reverse_lazy('users_password_reset_done')),
        name='users_password_reset'),
    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
        name='users_password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users_password_reset_complete')),
        name='users_password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name='users_password_reset_complete'),
    url(r'^index/$',index,name='index'),
    url(r'^accounts/static/(?P<path>.*)$', static.serve, {'document_root':settings.STATIC_ROOT}, name='static'),
]
