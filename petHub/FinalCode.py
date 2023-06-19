from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class HTTP_CODE:
    SUCCESS = 200
    # 没有返回数据
    SUCCESS_WITH_NO_DATA = 230
    # 没有数据
    NO_REQUEST_DATA = 460
    # 用户不存在
    USER_IS_NOT_EXIST = 461
    # 用户已注册
    USER_REGISTERED = 462
    # 前后密码不一致
    PASSWD_NOT_THE_SAME = 463
    # 密码长度应大于8 小于64
    PASSWD_LEN_ERROR = 467
    # cookie验证失败
    ID_VALIDATION_FAILED = 464
    # 找不到ID
    ID_MISSING = 465
    # 错误的请求
    ERROR_REQUEST = 466


class Result(JsonResponse):

    def __init__(self, message="操作成功", code=200, data=None, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs):
        dataDict = {
            "message": message,
            "code": code,
            "data": data
        }
        super().__init__(dataDict, encoder, safe, json_dumps_params, **kwargs)

