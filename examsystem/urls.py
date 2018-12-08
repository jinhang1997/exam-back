"""examsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from backend import views
from backend import login_manage
from backend import test_manage
# import indata_tool_api.urls
from django.conf import settings
from django.conf.urls.static import static
import examsystem
import django

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login_manage.login),
    url(r'^logout/', login_manage.logout),

    #url(r'^test-list-ava/', test_manage.get_avaliable),
    #url(r'^test-history/', test_manage.get_history),
    url(r'^paper-get-list-stu/', test_manage.get_stu_testlist),
    url(r'^paper-get-list-tea/', test_manage.get_tea_testlist),
    url(r'^paper-manage/', test_manage.manage_paper),
    url(r'^paper-get-detail/', test_manage.get_paper_detail),
    url(r'^paper-prolist/', test_manage.modify_paper_prolist),
    url(r'^paper-stulist/', test_manage.modify_paper_stulist),

    url(r'^test-manage/', test_manage.get_test_detail),

    url(r'^my-info/', login_manage.myinfo),
    url(r'^user-list/', login_manage.get_all_user),
    url(r'^user-add/', login_manage.add_user),
    url(r'^user-add-batch/', login_manage.add_user_batch),
    url(r'^user-delete/', login_manage.delete_user),

    url(r'^echo/', views.httpecho),
    url(r'^', views.notfound),
    # url(r'^$', TemplateView.as_view(template_name="index.html")),
]
