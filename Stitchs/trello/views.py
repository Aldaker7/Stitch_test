from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model, login,
    logout)
from .forms import (UserSignupForm, BoardForm, CardForm,
                    ListForm, MemberForm)
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import (StitchCard, StitchList, StitchBoard,
                     Members, Label)
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
import json
import requests
from operator import itemgetter


def login_user(request):
    """
        :return: Logging user
        Cookies: to avoid keep logging in if browser closed
    """
    if request.COOKIES.get('sessionid'):
        return HttpResponseRedirect(reverse("boards"))
    if request.method == "POST":
        print(request.POST.get('username'))
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            request.session.set_expiry(86400)
            request.COOKIES['username'] = request.user
            login(request, user)
            return HttpResponseRedirect(reverse("boards"))
    return render(request, 'login.html', context={})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def signup_user(request):
    form = UserSignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('login'))
    context = {
        'form': form,
    }
    return render(request, 'registeration.html', context=context)


@login_required(login_url='login')
def get_user_board(request):
    """
        :return: after calling REST it will return all board for user
        :API: GET
    """
    url = "http://localhost:8000/apis/api/board/%s" % request.user.id
    header = {"Content-Type": "application/json"}
    req = requests.get(url, data='', headers=header)
    if req.status_code in [200, 201]:
        board = req.json()
        return render(request, 'board.html', context={'form': board})
    return render(request, 'board.html',context={})


@login_required(login_url='login')
def create_board(request):
    """
    :return: Creating New Board & Creating 6 labels for this board
    :API: POST
     """
    if request.method == "POST":
        url = "http://localhost:8000/apis/api/board/%s" % request.user.id
        header = {"Content-Type": "application/json"}
        data = json.dumps({
            'title': request.POST.get('title_board'),
            'user': request.user.id,
        })
        req = requests.post(url, data=data, headers=header)
        if req.status_code in [200, 201]:
            count = 1
            board_id = req.json().get('id')
            url = "http://localhost:8000/apis/api/board/list/label/%s" % board_id
            while count < 7:
                data = json.dumps({
                    'title': "Label%s" % count,
                    'active': True,
                    'board': board_id,
                })
                count += 1
                req = requests.post(url, data=data, headers=header)
            return HttpResponseRedirect(reverse("boards"))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def updates_board(request, pk):
    """
    :param pk: Board id
    :return: renaming board
    :API: PATCH for partial update
    """
    if request.method == 'POST':
        url = "http://localhost:8000/apis/api/update/board/%s" % pk
        header = {"Content-Type": "application/json"}
        data = json.dumps({
            'title': request.POST.get('title_board'),
            'user': request.user.id,
            'active': True,
        })
        req = requests.patch(url, data=data, headers=header)
        if req.status_code in [200, 201]:
            return HttpResponseRedirect(reverse("boards"))
    else:
        url = "http://localhost:8000/apis/api/update/board/%s" % pk
        header = {"Content-Type": "application/json"}
        req = requests.get(url, data='', headers=header)
        if req.status_code in [200, 201]:
            return render(request, 'board.html',
                          context={'board':req.json(),
                                   'board_id': req.json()['id'],
                                   'update': True})


@login_required(login_url='login')
def get_list(request, pk, order):
    """
    :param pk: board_id to get all lists for it
    :param order: from old to new (2) or opposite (1)
    :return: list of all Lists
    :API: GET
    """
    url = "http://localhost:8000/apis/api/list/%s" % pk
    header = {"Content-Type": "application/json"}
    req = requests.get(url, data='', headers=header)
    if req.status_code in [200, 201]:
        lists = req.json()
        if order == '2':
            lists = sorted(lists, key=itemgetter('id'), reverse=True)
            return render(request, 'list_page.html',
                          context={'list': lists, 'pk': pk,
                                   'select': 2,})
        else:
            return render(request, 'list_page.html',
                          context={'list': lists, 'pk': pk,
                                   'select': 1})


@login_required(login_url='login')
def create_list(request, pk):
    """
    :param pk: board_id
    :return: Creating New List using REST
    :API: POST
    """
    if request.method == "POST":
        url = "http://localhost:8000/apis/api/list/%s" % pk
        header = {"Content-Type": "application/json"}
        data = json.dumps({
            'title': request.POST.get('title_list'),
            'board': pk
        })
        req = requests.post(url, data=data, headers=header)
        if req.status_code in [200, 201]:
            return HttpResponseRedirect(reverse('list', kwargs={'pk': pk,
                                                                'order': 1}))
    return HttpResponseRedirect(reverse('list', kwargs={'pk': pk,
                                                        'order': 1}))


@login_required(login_url='login')
def updates_list(request, pk):
    """
    :param pk:  List id to update using REST
    :return: Updating List Title
    :API: PATCH
    """
    url = "http://localhost:8000/apis/api/update/list/%s" % pk
    header = {"Content-Type": "application/json"}
    if request.method == 'POST':
        data = json.dumps({
            'title': request.POST.get('title_list'),
        })
        req = requests.patch(url, data=data, headers=header)
        board_id = req.json()['board']
        if req.status_code in [200, 201]:
            return HttpResponseRedirect(reverse("list",
                                                kwargs={'pk': board_id,
                                                        'order': 1}))
    else:
        req = requests.get(url, data='', headers=header)
        if req.status_code in [200, 201]:
            return render(request, 'list_page.html',
                          context={'update_list_dic': req.json(),
                                   'pk': req.json()['board']})


@login_required(login_url='login')
def get_card(request, pk, order):
    """
    :param pk: list id
    :param order: old to new (2) opposite (1)
    :return: Listing all cards usin REST
    :API: GET
    """
    url = "http://localhost:8000/apis/api/card/%s" % pk
    header = {"Content-Type": "application/json"}
    req = requests.get(url, data='', headers=header)
    if req.status_code in [200, 201]:
        cards = req.json()
        for i in cards:
            obj = Label.objects.get(pk=i['labels'])
            i['label_name'] = obj.title
        if order == '2':
            cards = sorted(cards, key=itemgetter('id'), reverse=True)
            return render(request, 'cards.html',
                          context={'cards': cards, 'list_id': pk,
                                   'cards_exist': True if cards else False,
                                   'select': 2})
        else:
            return render(request, 'cards.html',
                          context={'cards': cards, 'list_id': pk,
                                   'cards_exist': True if cards else False,
                                   'select': 1})


@login_required(login_url='login')
def create_card(request, list_id):
    """
    :param list_id
    :return: Creating New card using REST
    :API: POST
    """
    form = CardForm(request.POST or None)
    board_id = StitchList.objects.get(pk=list_id).board.id
    url_labels = "http://localhost:8000/apis/api/board/list/label/%s" % board_id
    header = {"Content-Type": "application/json"}
    req_label = requests.get(url_labels, headers=header, data='')
    if request.method == 'POST':
        url = "http://localhost:8000/apis/api/card/%s" % list_id
        data = json.dumps({
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'DueDate': request.POST.get('DueDate'),
            'list': list_id,
            'labels': request.POST.get('labels'),
        })

        req = requests.post(url, data=data, headers=header)
        if req.status_code in [200, 201]:
            return HttpResponseRedirect(reverse('cards',
                                                kwargs={'pk': list_id,
                                                        'order': 1}))

    context = {'form': form,
               'list_id': list_id,
               'create_card': True,
               'list_labels': req_label.json()}

    return render(request, 'cards.html', context=context)


@login_required(login_url='login')
def updates_card(request, pk):
    """
    :param pk: Card id
    :return: Cards info to update using REST
    :API: GET, PATCH
    """
    url = "http://localhost:8000/apis/api/update/card/%s" % pk
    header = {"Content-Type": "application/json"}
    req = requests.get(url, data='', headers=header)
    list_id = req.json()['list']
    if request.method == 'POST':
        data = json.dumps({
            'title': request.POST.get('title_card'),
            'description': request.POST.get('description'),
            'DueDate': request.POST.get('DueDate'),
            'labels': request.POST.get('labels_options'),
            'list': request.POST.get('list_option'),
        })
        reqs = requests.patch(url, data=data, headers=header)
        if reqs.status_code in [200, 201]:
            return HttpResponseRedirect(reverse('cards',
                                                kwargs={'pk': list_id,
                                                        'order': 1}))
    else:

        board_id = StitchList.objects.get(id=req.json()['list']).board.id
        url_label = "http://localhost:8000/apis/api/board/list/label/%s" % board_id
        req_label = requests.get(url_label, data='', headers=header)
        labels = req_label.json()
        if req.status_code in [200, 201]:
            board_id = StitchList.objects.get(pk=req.json()['list']).board.id
            url_board = "http://localhost:8000/apis/api/list/%s" % board_id
            req_board = requests.get(url_board, data='', headers=header)
            return render(request, 'cards.html',
                          context={'update_card_dic': req.json(),
                                   'list_id': req.json()['list'],
                                   'list_options': req_board.json(),
                                   'label_options': labels})


@login_required(login_url='login')
def archive_board(request, pk):
    """
    :param pk: board id
    :return: making active = False
    :API: PATCH
    """
    url = "http://localhost:8000/apis/api/update/board/%s" % pk
    headers = {"Content-Type": "application/json"}
    data = json.dumps({'active': False})
    req = requests.patch(url, data=data, headers=headers)
    if req.status_code in [200, 201]:
        return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def archive_list(request, pk):
    """
    :param pk: list id
    :return: making active = False
    :API: PATCH
    """
    url = "http://localhost:8000/apis/api/update/list/%s" % pk
    headers = {"Content-Type": "application/json"}
    data = json.dumps({'active': False})
    req = requests.patch(url, data=data, headers=headers)
    board_id = req.json()['board']
    if req.status_code in [200, 201]:
        return HttpResponseRedirect(reverse('list',
                                            kwargs={'pk': board_id,
                                                    'order': 1}))
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def create_member(request):
    """
    :return: Creating New Member
    """
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('login'))
    context = {
        'form': form,
        'create_member': True,
    }
    return render(request, 'members.html', context=context)


@login_required(login_url='login')
def get_members(request):
    """
    :return: Listing all members using REST
    :API: GET
    """
    url = "http://localhost:8000/apis/api/members"
    headers = {"Content-Type": "application/json"}
    req = requests.get(url, data='', headers=headers)
    if req.status_code in [200, 201]:
        members = req.json()
        if members:
            return render(request, 'members.html',
                          context={'members': members,
                                   'list_members': True,
                                   'create_member': False})
        else:
            return HttpResponse("No Members exist please create one")


@login_required(login_url='login')
def rename_member(request, pk):
    """
    :param pk: member id
    :return: Renaming member after getting his info
    :API: GET, PATCH
    """
    url = 'http://localhost:8000/apis/api/member/rename/%s' % pk
    headers = {"Content-Type": "application/json"}
    req_get = requests.get(url, data='', headers=headers)
    if request.method == 'POST':
        data = json.dumps({
            'name': request.POST.get('name_member')
        })
        req = requests.patch(url, data=data, headers=headers)
        if req.status_code in [200, 201]:
            get_members_url = "http://localhost:8000/apis/api/members"
            req_list = requests.get(get_members_url, data='', headers=headers)
            members = req_list.json()
            return render(request, 'members.html',
                          context={'members': members,
                                   'list_members': True,
                                   'create_member': False,
                                   'rename': False})
    return render(request, 'members.html',
                  context={'member': req_get.json(),
                           'list_members': False,
                           'create_member': False,
                           'rename': True})


@login_required(login_url='login')
def archive_member(request, pk):
    """
    :param pk: Member id
    :return: setting active to False
    :API: PATCH
    """
    url = 'http://localhost:8000/apis/api/member/rename/%s' % pk
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        'active': False
    })
    req = requests.patch(url, data=data, headers=headers)
    if req.status_code in [200, 201]:
        get_members_url = "http://localhost:8000/apis/api/members"
        req_list = requests.get(get_members_url, data='', headers=headers)
        members = req_list.json()
        return render(request, 'members.html',
                      context={'members': members,
                               'list_members': True,
                               'create_member': False,
                               'rename': False})


@login_required(login_url='login')
def archive_card(request, pk):
    """
    :param pk: Card id
    :return: Setting active to False
    :API: PATCH
    """
    url = "http://localhost:8000/apis/api/update/card/%s" % pk
    headers = {"Content-Type": "application/json"}
    data = json.dumps({'active': False})
    req = requests.patch(url, data=data, headers=headers)
    list_id = req.json()['list']
    if req.status_code in [200, 201]:
        return HttpResponseRedirect(reverse('cards',
                                            kwargs={'pk': list_id,
                                                    'order': 1}))

    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def get_labels(request, pk):
    """
    :param pk: board id to get its labels
    :return: Listing all labels related to the board
    :API: GET
    """
    url = "http://localhost:8000/apis/api/board/list/label/%s" % pk
    headers = {"Content-Type": "application/json"}
    data = ''
    req = requests.get(url, data=data, headers=headers)
    if req.status_code in [200, 201]:
        return render(request, 'labels.html',
                      context={'labels': req.json(),
                               'list_labels': True})


@login_required(login_url='login')
def rename_label(request, pk):
    """
    :param pk: Label id
    :return: Getting label info then renaming it using REST
    :API: GET, PATCH
    """
    url = "http://localhost:8000/apis/api/board/update/label/%s" % pk
    headers = {"Content-Type": "application/json"}
    get_label = requests.get(url, data='', headers=headers)
    if request.method == 'POST':
        data = json.dumps({'title': request.POST.get('title_label')})
        req = requests.patch(url, data=data, headers=headers)
        board_id = req.json()['board']
        if req.status_code in [200, 201]:
            return HttpResponseRedirect(reverse('get_labels',
                                                kwargs={'pk': board_id}))
    return render(request, 'labels.html',
                  context={'label': get_label.json(),
                           'list_labels': False,
                           'rename': True})


@login_required(login_url='login')
def archive_label(request, pk):
    """
    :param pk: Label id
    :return: Setting active to False
    :API: PATCH
    """
    url = "http://localhost:8000/apis/api/board/update/label/%s" % pk
    headers = {"Content-Type": "application/json"}
    data = json.dumps({'active': False})
    req = requests.patch(url, data=data, headers=headers)
    board_id = req.json()['board']
    if req.status_code in [200, 201]:
        return HttpResponseRedirect(reverse('get_labels',
                                            kwargs={'pk': board_id}))


