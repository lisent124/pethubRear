from django.contrib import admin, messages
from petHub.models import *


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 需要展示的属性
    list_display = ("id", "name", "gender", "phone", "location")
    # 过滤选择器
    list_filter = ("gender",)
    # 分页
    list_per_page = 5
    # 可编辑的属性
    list_editable = ("location",)
    # 可搜索的属性
    search_fields = ("location",)
    verbose_name = "用户"

    # 对于添加页的信息展示
    fieldsets = (
        ("个人信息", {"fields": ("name", "gender", "phone", "location", "password","head_picture"), "description": '<b>hello</b>'}),
        ("支付信息", {"fields": ("bank_number", "pay_password"), "description": '这是一些形容'})
    )

    def has_module_permission(self, request):
        # 权限的逻辑判断
        # request.user.info 可获取当前访问的用户信息
        return True

    def has_add_permission(self, request):
        # 是否再后台中添加
        return True

    def has_view_permission(self, request, obj=None):
        # 是否可进入详情页
        return True


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "image_mian", "visible")
    # 注册声明操作
    actions = ["to_show", "to_hide"]

    # 绑定操作
    @admin.action(description="对外公开")
    def to_show(self, request, queryset):

        queryset.update(visible=True)
        # self.message_user(request, message="已对外公开")
        messages.success(request, "已对外公开")  # from django.contrib import messages

    @admin.action(description="对外隐藏")
    def to_hide(self, request, queryset):
        queryset.update(visible=False)
        self.message_user(request, message="已对外隐藏")


@admin.register(Accountant)
class AccountantAdmin(admin.ModelAdmin):

    pass


@admin.register(Parlour)
class ParlourAdmin(admin.ModelAdmin):
    pass


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    pass


@admin.register(Interactives)
class InteractivesAdmin(admin.ModelAdmin):
    pass


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    pass
