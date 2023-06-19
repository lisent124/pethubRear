import os
import re
import time

from django.db import models
from django.utils.html import format_html

from pethubRear.settings import BASE_DIR


# Create your models here.


def rename_head_user(instance, filename):
    suffix = filename.split(".")[1]
    return "static/user/{0}/{1}".format(instance.id,
                                        instance.name + '_head.' + suffix)


class User(models.Model):
    """
    用户表，包含用户基本信息 以及银行卡信息
    """
    gender_chioces = (
        ('m', "男"),
        ('w', "女")
    )
    id = models.AutoField(verbose_name="用户ID", primary_key=True)
    name = models.CharField(verbose_name="用户名",
                            max_length=16)
    gender = models.CharField(verbose_name="性别",
                              max_length=1,
                              choices=gender_chioces,
                              default='m')
    phone = models.CharField(verbose_name="用户电话",
                             max_length=12,
                             unique=True)
    location = models.CharField(verbose_name="用户地址",
                                max_length=64,
                                null=True,
                                blank=True)
    password = models.CharField(verbose_name="用户登录密码", max_length=64)
    bank_number = models.CharField(verbose_name="银行卡号",
                                   max_length=12,
                                   null=True,
                                   blank=True)
    pay_password = models.CharField(verbose_name="用户支付密码",
                                    max_length=6,
                                    null=True,
                                    blank=True)

    head_picture = models.ImageField(verbose_name="头像",
                                     upload_to=rename_head_user,
                                     default="static/user/None/com_head.jpg",
                                     null=True,
                                     blank=True)

    # 对象显示格式
    def __str__(self):
        return str(self.name)

    def saveHead(self, file):
        """
        保存图片
        :param file:
        :return:
        """
        head = rename_head_user(self, file.name)
        self.head_picture = head
        path = os.path.join(os.path.join(BASE_DIR, r'static\user'), str(self.id))

        suffix = file.name.split(".")[1]
        filename = self.name + '_head.' + suffix

        if os.path.exists(path) is False:
            os.makedirs(path)
        destination = open(os.path.join(path, filename), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        self.save()

    class Meta:
        # 单数显示表名
        verbose_name = "用户"
        # 复数显示表民
        verbose_name_plural = "用户"


def rename_blog_picture(instance, filename):
    suffix = filename.split(".")[1]
    return "static/user/{0}/blogs/{1}/{2}".format(instance.user_id,
                                                  instance.id,
                                                  'blog.' + suffix)


class Blog(models.Model):
    """
    博客表，用户发送的博客，支持文字与图片
    """
    id = models.AutoField(verbose_name="BlogID", primary_key=True)
    user = models.ForeignKey(verbose_name="用户ID",
                             to=User,
                             on_delete=models.CASCADE)
    release_time = models.DateTimeField(verbose_name="Blog发布时间",
                                        auto_now_add=True)
    content = models.TextField(verbose_name="文字内容")
    picture = models.ImageField(verbose_name="图片地址",
                                upload_to=rename_blog_picture,
                                null=True,
                                blank=True)
    visible = models.BooleanField(verbose_name="对外显示",
                                  default=True)

    def savePicture(self, file):
        """
        保存图像
        :param file:
        :return:
        """
        self.picture = rename_blog_picture(self, file.name)
        path = os.path.join(os.path.join(BASE_DIR, r'static\user'), str(self.user_id))
        path = os.path.join(os.path.join(path, "blogs"), str(self.id))

        suffix = file.name.split(".")[1]
        filename = 'blog.' + suffix

        if os.path.exists(path) is False:
            os.makedirs(path)
        destination = open(os.path.join(path, filename), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        self.save()

    def image_mian(self):
        if self.picture is None:
            return None
        return format_html('<img src="/%s" height="40px" >' % self.picture)

    def __str__(self):
        return str(self.user) + str(self.id)

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = "博客"


class Accountant(models.Model):
    """
    财务人员，财务属于管理员，表含财务登录密码，以及财务的权限等级
    """
    job_grade = (
        ("0", "总会计师"),
        ("1", "小组组长"),
        ("2", "组员")
    )
    id = models.AutoField(verbose_name="财务ID", primary_key=True)
    password = models.CharField(verbose_name="财务人员密码", max_length=64)
    grade = models.CharField(verbose_name="财务职务等级",
                             choices=job_grade,
                             max_length=1,
                             default="2")

    def __str__(self):
        return self.job_grade[int(self.grade)][1] + str(self.id)

    class Meta:
        verbose_name = "财务"
        verbose_name_plural = "财务"


def rename_head_parlour(instance, filename):
    suffix = filename.split(".")[1]
    return "static/parlour/{0}/{1}".format(instance.id, instance.name + '_head.' + suffix)


class Parlour(models.Model):
    """
    店铺表，包含店铺基本信息，以及店铺登录的相关信息
    """

    id = models.AutoField(verbose_name="店铺ID", primary_key=True)
    name = models.CharField(verbose_name="店铺名", max_length=32, unique=True)
    phone = models.CharField(verbose_name="店铺电话", max_length=12, unique=True)
    location = models.CharField(verbose_name="店铺地址", max_length=64,
                                null=True,
                                blank=True)
    password = models.CharField(verbose_name="店铺密码", max_length=64)
    accountant = models.ForeignKey(verbose_name="负责店铺的财务ID",
                                   related_name="aid_parlour",
                                   to=Accountant,
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    # description = models.CharField
    head_picture = models.ImageField(verbose_name="店铺头像",
                                     upload_to=rename_head_parlour,
                                     null=True,
                                     blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "店铺"
        verbose_name_plural = "店铺"


def rename_commodity_picture(instance, filename):
    suffix = filename.split(".")[1]
    return "static/parlour/{0}/commodities/{1}".format(instance.parlour_id, str(instance.name) + '.' + suffix)


class Commodity(models.Model):
    """
    商品，商品的基本信息
    """
    id = models.AutoField(verbose_name="商品ID", primary_key=True)
    parlour = models.ForeignKey(to=Parlour,
                                verbose_name="隶属店铺",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    name = models.CharField(verbose_name="商品名", max_length=64)
    price = models.FloatField(verbose_name="价格")
    unit = models.CharField(verbose_name="价格单位", max_length=32, default="个")
    stock = models.IntegerField(verbose_name="库存", default=0)
    picture = models.ImageField(verbose_name="商品图片",
                                upload_to=rename_commodity_picture,
                                default="static/parlour/None/com.png",
                                null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"


# class monitor(models.Model):
#     pass


class Interactives(models.Model):
    """
    用户之间的Blog交互信息表
    """
    id = models.AutoField(primary_key=True)

    blog = models.ForeignKey(verbose_name="BlogID",
                             to=Blog,
                             related_name="bid_interactives",
                             on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="与该Blog交互的用户",
                             to=User,
                             related_name="uid_interactives",
                             on_delete=models.DO_NOTHING)
    like = models.BooleanField(verbose_name="点赞", default=False)
    comment = models.CharField(verbose_name="评论",
                               max_length=64,
                               null=True,
                               blank=True)
    create_time = models.DateTimeField(verbose_name="交互创建时间",
                                       auto_now=True)

    def __str__(self):
        return str(self.blog) + ' with ' + str(self.user)

    class Meta:
        verbose_name = "用户交互"
        verbose_name_plural = "用户交互"


class Transactions(models.Model):
    """
    交易记录
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name="用户ID",
                             related_name="uid_transactions",
                             to=User,
                             on_delete=models.DO_NOTHING)
    commodity = models.ForeignKey(verbose_name="商品ID",
                                  related_name="cid_transactions",
                                  to=Commodity,
                                  on_delete=models.DO_NOTHING)
    accountant = models.ForeignKey(verbose_name="财务ID",
                                   related_name="aid_transactions",
                                   to=Accountant,
                                   on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(verbose_name="交易创建时间",
                                      auto_now_add=True)
    amount = models.IntegerField(verbose_name="交易数量", default=1)
    state = models.BooleanField(verbose_name="订单完成状态",
                                default=False)

    def __str__(self):
        return str(self.id) + str(self.user) + str(self.commodity)

    class Meta:
        verbose_name = "交易订单"
        verbose_name_plural = "交易订单"
