from appconf import AppConf
from django.conf import settings


class UsersAppConf(AppConf):
    VERIFY_EMAIL = False#验证邮箱激活开关
    CREATE_SUPERUSER = settings.DEBUG
    SUPERUSER_EMAIL = 'superuser@djangoproject.com'
    SUPERUSER_PASSWORD = 'django'
    SUPERUSER_NAEM = 'django'
    EMAIL_CONFIRMATION_TIMEOUT_DAYS = 3#邮箱确认时间
    SPAM_PROTECTION = True #垃圾邮箱保护
    REGISTRATION_OPEN = True #注册开关
    AUTO_LOGIN_ON_ACTIVATION = True #激活后自动登录开关
    AUTO_LOGIN_AFTER_REGISTRATION = False #注册后自动登录开关
    PASSWORD_MIN_LENGTH = 5 #密码最小长度
    PASSWORD_MAX_LENGTH = None #密码最大长度
    CHECK_PASSWORD_COMPLEXITY = True #检测密码复杂性
    PASSWORD_POLICY = {
        'UPPER': 0,       # Uppercase 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        'LOWER': 0,       # Lowercase 'abcdefghijklmnopqrstuvwxyz'
        'DIGITS': 0,      # Digits '0123456789'
        'PUNCTUATION': 0  # Punctuation """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    } #密码规则
    VALIDATE_EMAIL_DOMAIN = True
    EMAIL_DOMAINS_BLACKLIST = [] #邮箱黑名单
    EMAIL_DOMAINS_WHITELIST = [] #邮箱白名单
    USERS_SPAM_PROTECTION=True
    class Meta:
        prefix = 'users'
