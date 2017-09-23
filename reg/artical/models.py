from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType

# Create your models here.

#论文实体
class paper(models.Model):
    paper_Theme=models.CharField(_('论文主题'),max_length=255,null=True)

    paperChineseName=models.CharField(_('论文中文名称'),max_length=255)
    paperEnglishName=models.CharField(_('论文英文名称'),max_length=255)
    paperChineseSummary=models.CharField(_('论文中文摘要'),max_length=1000)
    paperEnglishSummary=models.CharField(_('论文英文摘要'),max_length=1000,null=True)
    submission_Time=models.DateTimeField(_('投稿时间'),null=True)
    paper_ModifyTime=models.DateTimeField(_('修改时间'),null=True)
    paperFiles=models.FileField(_('论文附件'),null=True)
    paper_Scores=models.FloatField(_('论文分数'),null=True)#由多个专家评分得出
    paper_level=models.CharField(_('论文优秀等级'),null=True,max_length=1,choices=(('0',_('非优秀论文')),('1',_('一等论文')),('2',_('二等论文')),('3',_('三等论文'))))
    paperStatus=models.CharField(_('论文录用状态'),null=True,max_length=1,choices=(('0',_('已投稿')),('1',_('审稿')),('2',_('已录用')),('3',_('已拒绝'))))
    paper_reportNumber=models.IntegerField(_('论文报告序号'),null=True)
    is_reported=models.BooleanField(_('论文是否已报告'),default=False)
    def __str__(self):
        return self.paper_Theme
    class Meta:
        verbose_name=_('论文')
        verbose_name_plural=_('论文')

#主题实体
class theme(models.Model):
    paper=models.ManyToManyField(paper)
    theme_ChineseName=models.CharField(_('主题中文名称'),max_length=255,null=True)
    theme_EnglishName=models.CharField(_('主题英文名称'),max_length=255,null=True)
    def __str__(self):
        return self.theme_ChineseName
    class Meta:
        verbose_name=_('论文主题')
        verbose_name_plural=('论文主题')
  

#论文与主题之间的联系
class paper_theme(models.Model):
    paper=models.ForeignKey(paper)
    theme=models.ForeignKey(theme)
    important_Order=models.CharField(_('重要程度顺序'),max_length=255,null=True)
    def __str__(self):
        return self.paeper.paper_Theme
    class Meta:
        verbose_name=_('论文-主题')
        verbose_name_plural=_('论文-主题')


#期刊实体
class journal(models.Model):
    jourName=models.CharField(_('期刊名称'),max_length=30)
    jourLevel=models.CharField(_('期刊等级'),null=True,choices=(('A1',_('A1学术期刊')),('A2',_('A2学术期刊')),('B1',_('B1学术期刊')),('B2',_('B2学术期刊')),('C',_('C普通期刊'))),max_length=4)#用编码表示
    jourManager=models.CharField(_('期刊联系人'),max_length=30)
    jourPhone=models.CharField(_('期刊联系手机号'),max_length=11)
    jourOfficePhone=models.CharField(_('期刊办公电话'),max_length=12,null=True)
    jourEmail=models.EmailField(_('期刊邮件地址'),max_length=128,null=True)
    jourUrl=models.CharField(_('期刊网址'),max_length=255)
    def __str__(self):
        return self.jourName
    class Meta:
        verbose_name=_('期刊')
        verbose_name_plural=_('期刊')

#推荐（期刊与论文之间的联系）
class recommend(models.Model):
    paper=models.ForeignKey(paper)
    journal=models.ForeignKey(journal)
    recommender=models.CharField(_('推荐人'),null=True,max_length=30)
    recommendTime=models.DateTimeField(_('推荐时间'),null=True)
    recommendOpinion=models.TextField(_('推荐意见'),null=True)
    recommendStatus=models.CharField(_('推荐状态'),max_length=1,null=True,choices=(('0',_('已推荐')),('1',_('在审稿')),('2',_('在录用')),('3',_('被拒绝'))))
    def __str__(self):
        return self.journal.jourName
    class Meta:
        verbose_name=_('推荐')
        verbose_name_plural=_('推荐')



#作者实体
class author(models.Model):
    paper=models.ManyToManyField(paper,blank=True)
    authorName=models.CharField(_('作者姓名'),max_length=30) 
    authorCompany=models.CharField(_('作者工作单位'),max_length=255,null=True)
    authorAddress=models.CharField(_('作者地址'),max_length=255,null=True)
    authorPhone=models.CharField(_('作者手机号'),max_length=11,null=True)
    authorOfficePhone=models.CharField(_('作者办公电话'),max_length=12,null=True)
    authorEmail=models.EmailField(_('作者邮件地址'),max_length=128,null=True)
    authorJob=models.CharField(_('作者职称'),max_length=30,null=True)#用编码表示，是否为学生，学生类型
    def __str__(self):
        return self.authorName
    class Meta:
        verbose_name=_('作者')
        verbose_name_plural=_('作者')
	
	
#审稿专家实体
class reviewer(models.Model):
    paper=models.ManyToManyField(paper,through='review')
    reviewerName=models.CharField(_('姓名'),max_length=30)
    reviewer_Sex=models.CharField(_('性别'),max_length=1,null=True,choices=(('0',_('男')),('1',_('女'))))
    reviewer_birth=models.DateTimeField(_('出生日期'),null=True)
    reviewer_IDnumber=models.CharField(_('身份证号'),max_length=18,null=True)
    reviewerWorkplace=models.CharField(_('工作单位'),max_length=255)
    reviewerTitle=models.CharField(_('职称'),max_length=3)
    reviewerPhone=models.CharField(_('手机'),max_length=11)
    reviewerOfficePhone=models.CharField(_('办公电话'),max_length=12)
    reviewerEmail=models.EmailField(_('邮件地址'),max_length=128)
    reviewerSecondEmail=models.EmailField(_('备用邮箱'),max_length=128)
    reviewerBankName=models.CharField(_('银行名称'),max_length=255)
    reviewerBanknumber=models.CharField(_('银行账号'),max_length=30)
    reviewerMoney=models.DecimalField(_('审稿金额'),max_digits=8,decimal_places=2,null=True)
    reviewernumber=models.IntegerField(_('审稿论文数'),null=True)
    def __str__(self):
        return self.reviewerName
    class Meta:
        verbose_name=_('专家')
        verbose_name_plural=_('专家')


#审稿
class review(models.Model):
    paper=models.ForeignKey(paper)
    reviewer=models.ForeignKey(reviewer)
    reviewer_paper_Kmownlevel=models.CharField(_('专家对论文的熟悉程度'),null=True,max_length=2,choices=(('10',_('10分（最为熟悉）')),('9',_('9分')),('8',_('8分')),('7',_('7分')),('6',_('6分')),('5',_('5分')),('4',_('4分')),('3',_('3分')),('2',_('2分')),('1',_('1分（最不熟悉）'))))
    reviewTime=models.DateTimeField(_('审稿时间'),null=True)
    reviewOpinionToAuthor=models.TextField(_('给作者的审稿意见'),null=True)
    reviewOpinionToEditor=models.TextField(_('给编辑的审稿意见'),null=True)
    reviewResult=models.CharField(_('审稿结果'),max_length=1,null=True,choices=(('0',_('强烈推荐')),('1',_('推荐')),('2',_('弱推荐')),('3',_('弱拒绝')),('4',_('拒绝')),('5',_('强烈拒绝'))))
    review_Scores=models.FloatField(_('论文评分'),null=True)
    def __str__(self):
        return self.reviewer.reviewerName
    class Meta:
        verbose_name=_('审稿')
        verbose_name_plural=_('审稿')
#审稿结果用编码表示


#网页实体
class web(models.Model):
    webTitle=models.CharField(_('网页title'),max_length=255)
    webUrl=models.CharField(_('网址'),max_length=255)
    webDetail=models.TextField(_('网页内容'),null=True)
    webAuthor=models.CharField(_('作者'),max_length=30)
    webCreateTime=models.DateTimeField(_('生成时间'),null=True)
    webModifyTime=models.DateTimeField(_('修改时间'),null=True)
    webModifier=models.CharField(_('修改人'),max_length=30)
    firstReviewer=models.CharField(_('第一审核人'),max_length=30,null=True)
    firstReviewTime=models.DateTimeField(_('一审时间'),null=True)
    firstReviewOpinion=models.TextField(_('一审意见'),null=True)
    firstReviewStatus=models.CharField(_('一审状态'),max_length=1,null=True,choices=(('0',_('未审核')),('1',_('正在审核')),('2',_('已审核')),('3',_('批准')),('4',_('拒绝'))))
    secondReviewer=models.CharField(_('第二审核人'),max_length=30,null=True)
    secondReviewTime=models.DateTimeField(_('二审时间'),null=True)
    secondReviewOpinion=models.TextField(_('二审意见'),null=True)
    secondReviewStatus=models.CharField(_('二审状态'),max_length=1,null=True,choices=(('0',_('未审核')),('1',_('正在审核')),('2',_('已审核')),('3',_('批准')),('4',_('拒绝'))))
    approver=models.CharField(_('批准人'),max_length=30)
    approvalTime=models.DateTimeField(_('批准时间'),null=True)
    approvalOpinion=models.TextField(_('批准意见'),null=True)
    approvalStatus=models.CharField(_('批准状态'),max_length=1,null=True,choices=(('0',_('正在批准')),('1',_('批准')),('2',_('拒绝'))))
    def __str__(self):
        return self.webTitle
    class Meta:
        verbose_name=_('网页')
        verbose_name_plural=_('网页')


