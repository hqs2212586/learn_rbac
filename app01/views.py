from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from rbac.models import *
import re
from rbac.service.permissions import *


class Per(object):
    def __init__(self, actions):
        self.actions = actions

    def add(self):
        return "add" in self.actions

    def delete(self):
        return "delete" in self.actions

    def edit(self):
        return "edit" in self.actions

    def list(self):
        return "list" in self.actions


def users(request):
    user_list = User.objects.all()
    permission_list = request.session.get("permission_list")
    print(permission_list)  # ['/users/', '/users/add', '/roles/', '/users/delete/(\\d+)', '/users/edit/(\\d+)']

    # 查询当前登录人的名字
    id = request.session.get("user_id")
    user = User.objects.filter(id=id).first()

    per = Per(request.actions)

    return render(request, "users.html", locals())


def add_user(request):
    permission_list = request.session["permission_list"]  # ['/users/', '/users/add', '/users/delete/(\\d+)', '/users/edit/(\\d+)']

    current_path = request.path_info   # 当前路径的属性

    flag = False
    for permission in permission_list:
        permission = "^%s$" % permission
        ret = re.match(permission, current_path)  # 第一个参数是匹配规则，第二个参数是匹配项
        if ret:
            flag = True
            break
    if not flag:
        return HttpResponse("没有访问权限！")


def del_user(request, id):
    return HttpResponse("del" + id)


def roles(request):
    role_list = Role.objects.all()

    per = Per(request.actions)

    return render(request, "roles.html", locals())


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user = User.objects.filter(name=user, pwd=pwd).first()
        if user:
            # 保存登录状态，request.session

            ############### 在session中注册用户id ################
            request.session["user_id"] = user.pk

            ############### 在sessions中注册权限列表 #############

            # 登录成功
            # 查询当前登录用户的所有角色
            # ret = user.roles.all()
            # print(ret)   # <QuerySet [<Role: 保洁>, <Role: 销售>]>

            # 查看当前用户所有的权限
            # 1、用values()来遍历QuerySet;  2、跨表查询  3、distinct去重
            # permissions = user.roles.all().values("permissions__url").distinct()
            # print(permissions)  # <QuerySet [{'permissions__url': '/users/'}, {'permissions__url': '/users/add'}]>
            #
            # permission_list = []
            # for item in permissions:
            #     permission_list.append(item["permissions__url"])
            #
            # print(permission_list)  # ['/users/', '/users/add']

            # ret = user.roles.all().values("title", "permissions__url")
            # print(ret)  # <QuerySet [{'title': '保洁', 'permissions__url': '/users/'}, {'title': '销售', 'permissions__url': '/users/'}, {'title': '销售', 'permissions__url': '/users/add'}]>
            """value解析：
            上面的代码可以解释为如下步骤：
            temp = []
            for role in user.roles.all():
                temp.append({
                    "title": role.title,
                    "permissions_url": role.permissions.url,
                })
            """
            # request.session["permission_list"] = permission_list

            inital_session(user, request)

            return HttpResponse("登录成功！")

    return render(request, "login.html")