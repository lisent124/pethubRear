import json
import os
import random

import django
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers

from pethubRear.settings import BASE_DIR
from petHub.models import User, Commodity, Parlour, Blog, Interactives, Accountant, Transactions
from petHub.FinalCode import HTTP_CODE, Result


# Create your views here.

baseUrl = "http://127.0.0.1:8000/"


# baseUrl = "http://192.168.118.1:8000/"


def addCommodities():
    util = random.Random()
    parlours = list(Parlour.objects.all())

    for i in range(30):
        commodity = Commodity(name="name+" + str(util.random()))
        commodity.parlour = util.choice(parlours)
        commodity.price = util.randrange(0, 100)
        commodity.stock = util.randint(10, 40)
        commodity.picture = "static/parlour/None/com.png"
        Commodity.save(commodity)


def test(request):
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id
    response = Result("HTTP_CODE")
    return response


def registerVerify(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == "POST":
        phone = request.POST.get("phone")
        if phone is not None and len(phone) != 11:
            return Result("请输入正确的手机号", code=HTTP_CODE.NO_REQUEST_DATA)
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist as e:
            passwrod0 = request.POST.get("password0")
            password = request.POST.get("password")

            if password != passwrod0:
                return Result("两次密码不相同", code=HTTP_CODE.PASSWD_NOT_THE_SAME)
            elif password is None or len(password) < 8 or len(password) >= 64:
                return Result("密码长度应大于8 小于64", code=HTTP_CODE.PASSWD_LEN_ERROR)
            password = make_password(password)
            user = User(phone=phone, password=password)
            user.name = "用户" + phone
            user.head_picture = "static/lisent.png"
            user.save()
            return Result("成功注册：" + user.phone)
        return Result("该手机号已被注册", code=HTTP_CODE.USER_REGISTERED)


def loginVerify(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if phone is None and password is None:
            return Result("请输入数据", code=HTTP_CODE.NO_REQUEST_DATA)
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist as e:
            return Result("请先注册", code=HTTP_CODE.USER_IS_NOT_EXIST)
        if check_password(password=password, encoded=user.password) is False:
            return Result("密码错误", code=HTTP_CODE.PASSWD_NOT_THE_SAME)

        response = Result("login success")
        # 设置cookie
        response.set_signed_cookie(key="id", value=user.id, max_age=60 * 60 * 24 * 3)
        response["id"] = user.id
        return response


def IdVerify(request):
    """
    身份验证，防止前端篡改ID
    :param request:
    :return:
    """
    try:
        id0 = request.get_signed_cookie("id")
        # pet_id = request.headers.get("id")
        # if id0 != pet_id:
        #     raise UserWarning("身份验证失败")
    except KeyError as e:
        print("KeyError", e.args)
        return Result("找不到用户ID，请重新登录", code=HTTP_CODE.ID_MISSING)
    except UserWarning as e:
        print(e.args)
        return Result(str(e.args[0]), code=HTTP_CODE.ID_VALIDATION_FAILED)
    except django.core.signing.BadSignature as e:
        print(e.args)
        return Result("签证过期，请重新登录", code=HTTP_CODE.ID_VALIDATION_FAILED)
    return id0


def commoditiesToList(commodities):
    """
    将QuerySet的commodities 封装并以list返回
    :param commodities:
    :return:
    """
    if type(commodities) == Commodity:
        commodities = [commodities]
    dataList = []
    for i in commodities:
        commodity = dict()
        commodity["id"] = i.id
        commodity['parlour'] = Parlour.objects.get(id=i.parlour_id).name
        commodity['parlour_id'] = i.parlour_id
        commodity["name"] = i.name
        commodity['price'] = i.price
        commodity["unit"] = i.unit
        commodity['stock'] = i.stock
        commodity['picture'] = baseUrl + str(i.picture)
        dataList.append(commodity)
    return dataList


def commodityList(request):
    """
    返回展示商品列表
    :param request:
    :return:
    """
    pet_id = request.GET.get("parlour_id")
    if pet_id is None:
        commodities = Commodity.objects.all().order_by("?")[:10]
    else:
        commodities = Commodity.objects.filter(parlour_id=pet_id)[:10]
    dataList = commoditiesToList(commodities)
    response = Result(data=dataList)
    return response


def parlourInfo(request):
    """
    返回店铺基本信息
    :param request:
    :return:
    """
    pet_id = request.GET.get("parlour_id")
    try:
        parlour = Parlour.objects.get(id=pet_id)
    except Parlour.DoesNotExist:
        return Result(message="测试成功")

    res = {
        "name": parlour.name,
        "phone": parlour.phone,
        "location": parlour.location,
        "head_picture": baseUrl + str(parlour.head_picture),
    }

    return Result(data=res)


def getUserInfo(request):
    """
    返回用户的基本信息，但不包括支付信息
    :param request:
    :return:
    """
    res = IdVerify(request)
    if type(res) is Result:
        return res

    user_id = request.GET.get("user_id")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("User is not exist")
        return Result("User is not exist", code=HTTP_CODE.USER_IS_NOT_EXIST)
    res = {
        "id": user.id,
        "name": user.name,
        "gender": user.gender,
        "head_picture": baseUrl + str(user.head_picture),
        "location": user.location
    }

    return Result(data=res)


def getAndCreateBlogs(request):
    """
    返回Blog，创建blog
    :param request:
    :return:
    """
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")
        blog = Blog(user_id=user_id, content=content)
        blog.save()
        if image is not None:
            blog.savePicture(image)
            # print(image.name, image)
        return Result("创建成功")

    if request.GET.get("self") == "true":
        blogs = Blog.objects.filter(user_id=user_id).order_by("-release_time")[:10]
    else:
        blogs = Blog.objects.filter(visible=True).order_by("?")[:5]
    dataList = list()
    for i in blogs:
        blog = dict()
        inter = Interactives.objects.filter(blog=i)
        try:
            user_inter = inter.filter(user_id=user_id).first()
        except Interactives.DoesNotExist as e:
            user_inter = None
        blog["user"] = {
            "id": i.user_id,
            "name": i.user.name,
            "head_picture": baseUrl + str(i.user.head_picture),
            "like": (False if user_inter is None else user_inter.like),
            "comment": (False if user_inter is None else user_inter.comment),
        }
        blog["blog"] = {
            "id": i.id,
            "content": i.content,
            "picture": (baseUrl + str(i.picture)) if i.picture else False,
            "release_time": i.release_time,
            "visible": i.visible

        }
        dataList.append(blog)
    return Result(data=dataList)


def deleteBlog(request):
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id
    if request.method == "POST":
        # 删除Blog
        try:
            blog_id = request.POST.get("blog_id")
            Blog.objects.get(id=blog_id).delete()
        except Blog.DoesNotExist as e:
            return Result("找不到Blog", code=HTTP_CODE.ERROR_REQUEST)
        return Result("删除成功")


def showAndHideBlog(request):
    """
    删除和隐藏Blog
    :param request:
    :return:
    """
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id
    if request.method == "POST":
        # 显示Blog
        blog_id = request.GET.get("blog_id")
        blog = Blog.objects.get(id=blog_id)
        blog.visible = True
        blog.save()
        return Result("显示成功")
    else:
        blog_id = request.GET.get("blog_id")
        blog = Blog.objects.get(id=blog_id)
        blog.visible = False
        blog.save()
        return Result("隐藏成功")


def like(request):
    """
    某用户对指定Blog点赞与取消
    :param request:
    :return:
    """
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id
    blog_id = request.GET.get("blog_id")

    # 判断是否有数据
    if blog_id is None:
        return Result("NO DATA", code=HTTP_CODE.NO_REQUEST_DATA)
    #  第一次交互时创建Interactive
    try:
        Blog.objects.get(id=blog_id)
        item = Interactives.objects.get(blog_id=blog_id, user_id=user_id)
    except Interactives.DoesNotExist as e:
        Interactives(blog_id=blog_id, user_id=user_id, like=True).save()
        return Result("like it success")
    except Blog.DoesNotExist as e:
        return Result("NO DATA")
    # 取反like
    item.like = False if item.like else True
    item.save()
    if item.like:
        return Result("like success")
    else:
        return Result("unlike success")


def getAndCreateComment(request):
    """
    返回某条Blog的评论
    :param request:
    :return:
    """
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id
    # 创建交互
    if request.method == "POST":
        blog_id = request.POST.get("blog_id")
        comment = request.POST.get("comment")
        try:
            Blog.objects.get(id=blog_id)
            item = Interactives.objects.get(blog_id=blog_id, user_id=user_id)
            item.comment = comment
            item.save()
        except Interactives.DoesNotExist as e:
            Interactives(blog_id=blog_id, user_id=user_id, comment=comment).save()
        except Blog.DoesNotExist as e:
            return Result("NO DATA")
        return Result("评论成功")
    blog_id = request.GET.get("blog_id")
    # 判断是否有数据
    if blog_id is None:
        return Result("NO DATA", code=HTTP_CODE.NO_REQUEST_DATA)

    items = list(Interactives.objects.filter(blog_id=blog_id))
    dataList = list()
    for item in items:
        if item.like is False and item.comment is None:
            break
        comment = {
            "blog_id": item.blog_id,
            "like": item.like,
            "comment": False if item.comment is None else item.comment,
            "create_time": item.create_time,
            "user": {
                "name": item.user.name,
                "head_picture": baseUrl + str(item.user.head_picture),
            },
        }
        dataList.append(comment)
    # dataList = serializers.serialize("json",items)

    return Result(data=dataList)


def updateUser(request):
    """
    更新用户的用户名 性别 地区 基本信息
    :param request:
    :return:
    """
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id
    if request.method == "POST":
        user = User.objects.get(id=user_id)

        try:
            user.name = request.POST.get("name")
            user.gender = request.POST.get("gender")
            user.location = request.POST.get("location")

            user.save()
        except KeyError:
            return Result("没有数据", code=HTTP_CODE.NO_REQUEST_DATA)

        return Result("更新成功")
    return Result("请求错误", code=HTTP_CODE.ERROR_REQUEST)


def updateUserHead(request):
    """
    用户更新头像
    :param request:
    :return:
    """
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id

    if request.method == "POST":
        user = User.objects.get(id=user_id)
        myFile = request.FILES.get("head")

        user.saveHead(myFile)

        return Result(str(user.head_picture))


def getAndCreateTransactions(request):
    """
    POST创建交易订单
    GET 返回交易订单
    :param request:
    :return:
    """
    user_id = IdVerify(request)
    if type(user_id) is Result:
        return user_id
    if request.method == "POST":
        commodity_id = request.POST.get("commodity_id")
        count = request.POST.get("count")
        try:
            order = Transactions(user_id=user_id, commodity_id=commodity_id, amount=count)
            order.accountant = Accountant.objects.filter().order_by("?")[0]
            order.save()
        except django.db.utils.IntegrityError:
            return Result("不存在的commodity_id")

        return Result("创建成功")
    # 返回交易订单
    transactions = Transactions.objects.filter(user_id=user_id).order_by("start_time")[:5]
    if transactions.__len__() == 0:
        return Result("没有订单", code=HTTP_CODE.SUCCESS_WITH_NO_DATA)
    dataList = list()
    for i in transactions:
        commodity = i.commodity
        order = {
            "name": commodity.name,
            "parlour": commodity.parlour.name,
            "price": commodity.price,
            "state": i.state,
            "count": str(i.amount) + commodity.unit,
            "start_time": i.start_time
        }
        dataList.append(order)
    return Result(data=dataList)
