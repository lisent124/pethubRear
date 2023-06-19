"""pethubRear URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

import petHub.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('petHub/login', petHub.views.loginVerify),
    path('petHub/register', petHub.views.registerVerify),
    path('test', petHub.views.test),
    path('petHub/parlour/commodities', petHub.views.commodityList),
    path('petHub/parlour/commoditiesByParlour', petHub.views.commodityList),
    path('petHub/order', petHub.views.getAndCreateTransactions),
    path('petHub/user', petHub.views.getUserInfo),
    path('petHub/user/update', petHub.views.updateUser),
    path('petHub/user/head', petHub.views.updateUserHead),
    path('petHub/parlour', petHub.views.parlourInfo),
    path('petHub/blogs', petHub.views.getAndCreateBlogs),
    path('petHub/blogs/show', petHub.views.showAndHideBlog),
    path('petHub/blogs/delete', petHub.views.deleteBlog),
    path('petHub/blogs/like', petHub.views.like),
    path('petHub/blogs/comment', petHub.views.getAndCreateComment),
]
