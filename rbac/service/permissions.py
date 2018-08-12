# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'


def inital_session(user,request):
    """
    查看当前用户所有的权限
    :param user:
    :param request:
    :return:
    """
    # 方案1：
    # permissions = user.roles.all().values("permissions__url").distinct()
    # print(permissions)  # <QuerySet [{'permissions__url': '/users/'}, {'permissions__url': '/users/add'}]>
    #
    # permission_list = []
    # for item in permissions:
    #     permission_list.append(item["permissions__url"])
    #
    # print(permission_list)
    #
    # request.session["permission_list"] = permission_list


    # 方案2：
    # 角色表跨到权限表查找
    permissions = user.roles.all().values("permissions__url", "permissions__group_id", "permissions__action").distinct()
    print("permissions", permissions)  # 有一个权限QuerySet中就有一个字典
    """
    permissions <QuerySet [{'permissions__url': '/users/', 
                            'permissions__group_id': 1, 
                            'permissions__action': 'list'}]>
    """
    # 对上述数据进行处理： 以组为键，以字典为值
    permission_dict = {}
    for item in permissions:
        gid = item.get("permissions__group_id")

        if not gid in permission_dict:
            permission_dict[gid] = {
                "urls": [item["permissions__url"], ],
                "actions": [item["permissions__action"], ]

            }
        else:
            # 组id已经在字典中
            permission_dict[gid]["urls"].append(item["permissions__url"])
            permission_dict[gid]["actions"].append(item["permissions__action"])

    print(permission_dict)  # {1: {'urls': ['/users/', '/users/add', '/users/delete/(\\d+)', '/users/edit/(\\d+)'],
    #                              'actions': ['list', 'add', 'delete', 'edit']}}

    request.session['permission_dict']=permission_dict


