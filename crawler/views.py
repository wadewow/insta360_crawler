# coding=utf-8

import json, sys, datetime, time, collections

reload(sys)
sys.setdefaultencoding('utf-8')
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from models import SalesStatus
from models import ElectronicSales
from models import UserDistribution
from models import UseCondition
from models import ErrorCondition
from models import SearchIndex
from models import CompetitorSales
# from task import get_taobao_sales as t

@csrf_exempt
def sales_status(request):
    if request.method == 'POST':
        body = json.loads(request.body, encoding='utf-8')
        data = body['data']
        week = body['week']
        is_native = body['is_native']
        week_date = datetime.datetime.strptime(week, '%Y-%m-%d').date()
        next_week = (week_date + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        SalesStatus.objects.filter(week=week, is_native=is_native).delete()
        for item in data:
            SalesStatus.objects.update_or_create(week=item['week'], location=item['location'], defaults=item)
            SalesStatus.objects.update_or_create(week=next_week, location=item['location'], is_native=is_native)
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        delta = today.weekday()
        is_native = 1
        if para.__contains__('is_native'):
            is_native = para.__getitem__('is_native')
        week = (today - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
        if para.__contains__('week'):
            week = para.__getitem__('week')
        else:
            weeks = SalesStatus.objects.filter(is_native=is_native).order_by('-week')
            for item in weeks:
                 week = item.week
                 break
        data = []
        res = SalesStatus.objects.filter(week=week, is_native=is_native)
        for item in res:
            temp = {'week': item.week,'location': item.location,'pick_up': item.pick_up,'sales_online': item.sales_online,'sales_offline': item.sales_offline,'inventory_first': item.inventory_first,'inventory_lower': item.inventory_lower,'reject':item.reject,'is_native':item.is_native}
            data.append(temp)
        result = {'week': week, 'data':data }
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')


@csrf_exempt
def get_sales_status(request):
    if request.method == 'POST':
        return HttpResponse('Do Nothing.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        is_native = 1
        location = "all"
        if para.__contains__('is_native'):
            is_native = para.__getitem__('is_native')
        if para.__contains__('start_time'):
            startTime = datetime.datetime.strptime(para.__getitem__('start_time'), '%Y-%m-%d').date()
            start_time = (startTime - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('location'):
            location = para.__getitem__('location')
        result = collections.OrderedDict()
        if location == 'all':
            res = SalesStatus.objects.filter(week__range=(start_time, end_time), is_native=is_native).values('week').annotate(pick_up_total=Sum('pick_up'), sales_online_total=Sum('sales_online'), sales_offline_total=Sum('sales_offline'), inventory_first_total=Sum('inventory_first'), inventory_lower_total=Sum('inventory_lower'), reject_total=Sum('reject')).order_by('week')
            for item in res:
                temp = {'pick_up': item['pick_up_total'],'sales_online': item['sales_online_total'],'sales_offline': item['sales_offline_total'],'inventory_first': item['inventory_first_total'],'inventory_lower': item['inventory_lower_total'],'reject':item['reject_total']}
                end = (item['week'] + datetime.timedelta(days=6)).strftime('%m-%d')
                result[item['week'].strftime('%m-%d')+'~'+end] = temp
        else:
            res = SalesStatus.objects.filter(week__range=(start_time, end_time), is_native=is_native, location = location).order_by('week')
            for item in res:
                temp = {'pick_up': item.pick_up,'sales_online': item.sales_online,'sales_offline': item.sales_offline,'inventory_first': item.inventory_first,'inventory_lower': item.inventory_lower,'reject':item.reject}
                end = (item.week + datetime.timedelta(days=6)).strftime('%m-%d')
                result[item.week.strftime('%m-%d')+'~'+end] = temp
        locations = SalesStatus.objects.filter(is_native=is_native).values('location').distinct()
        last = SalesStatus.objects.filter(week__lt=start_time, is_native=is_native).order_by('-week').first()
        last_inventory_first = 0
        last_inventory_lower = 0
        last_reject = 0
        if (last != None):
            last_inventory_first = last.inventory_first
            last_inventory_lower = last.inventory_lower
            last_reject = last.reject
        res_last = {}
        res_last['inventory_first'] = last_inventory_first
        res_last['inventory_lower'] = last_inventory_lower
        res_last['reject'] = last_reject
        temp = []
        for item in locations:
            temp.append(item['location'])
        return JsonResponse({'locations':temp, 'data':result, 'last':res_last},safe=False)
    else:
        return HttpResponse('Error.')


@csrf_exempt
def electronic_sales(request):
    if request.method == 'POST':
        body = json.loads(request.body, encoding='utf-8')
        data = body['data']
        week = body['week']
        week_date = datetime.datetime.strptime(week, '%Y-%m-%d').date()
        next_week = (week_date + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        ElectronicSales.objects.filter(week=week).delete()
        for item in data:
            ElectronicSales.objects.update_or_create(week=item['week'], location=item['location'], defaults=item)
            ElectronicSales.objects.update_or_create(week=next_week, location=item['location'])
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        delta = today.weekday()
        week = (today - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
        if para.__contains__('week'):
            week = para.__getitem__('week')
        else:
            weeks = ElectronicSales.objects.dates('week', 'day', order='DESC')
            for item in weeks:
                week = item
                break
        data = []
        res = ElectronicSales.objects.filter(week=week)
        for item in res:
            temp = {'week': item.week,'location': item.location,'view': item.view,'visitor': item.visitor,'payment': item.payment,'number': item.number,'buyer':item.buyer}
            data.append(temp)
        result = {'week': week, 'data':data }
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def get_electronic_sales(request):
    if request.method == 'POST':
        return HttpResponse('Do Nothing.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        location = "all"
        if para.__contains__('start_time'):
            startTime = datetime.datetime.strptime(para.__getitem__('start_time'), '%Y-%m-%d').date()
            start_time = (startTime - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('location'):
            location = para.__getitem__('location')

        result = collections.OrderedDict()
        if location == 'all':
            res = ElectronicSales.objects.filter(week__range=(start_time, end_time)).values('week').annotate(view_total=Sum('view'), visitor_total=Sum('visitor'), payment_total=Sum('payment'), number_total=Sum('number'), buyer_total=Sum('buyer')).order_by('week')
            for item in res:
                temp = {'view': item['view_total'],'visitor': item['visitor_total'],'payment': item['payment_total'],'number': item['number_total'],'buyer': item['buyer_total']}
                end = (item['week'] + datetime.timedelta(days=6)).strftime('%m-%d')
                result[item['week'].strftime('%m-%d')+'~'+end] = temp
        else:
            res = ElectronicSales.objects.filter(week__range=(start_time, end_time), location = location).order_by('week')
            for item in res:
                temp = {'view': item.view,'visitor': item.visitor,'payment': item.payment,'number': item.number,'buyer': item.buyer}
                end = (item.week + datetime.timedelta(days=6)).strftime('%m-%d')
                result[item.week.strftime('%m-%d')+'~'+end] = temp
        locations = ElectronicSales.objects.values('location').distinct()
        temp = []
        for item in locations:
            temp.append(item['location'])
        return JsonResponse({'locations':temp, 'data':result},safe=False)
    else:
        return HttpResponse('Error.')


@csrf_exempt
def user_distribution(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        res_native = []
        res_abroad = []
        native = UserDistribution.objects.filter(date__range=(start_time, end_time), is_native=1).values('location').annotate(total=Sum('new_user')).order_by('-total')
        abroad = UserDistribution.objects.filter(date__range=(start_time, end_time), is_native=0).values('location').annotate(total=Sum('new_user')).order_by('-total')
        fp = open('crawler/dict.json', 'r')
        dict = json.loads(fp.read(),encoding='utf-8')
        fp.close()
        for item in native:
            # temp = {'location': item['location'],'total': item['total']}
            # res_native.append({item['location']: temp})
            res_native.append(item)
        for item in abroad:
            try:
                location = dict[item['location']]
            except KeyError:
                location = item['location']
            item['location'] = location
            # temp = {'location': location,'total': item['total']}
            res_abroad.append(item)
        result={'abroad':res_abroad, 'native':res_native}
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')


@csrf_exempt
def user_area(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        is_native = 1
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('is_native'):
            is_native = para.__getitem__('is_native')
        result = collections.OrderedDict()
        res = UserDistribution.objects.filter(date__range=(start_time, end_time), is_native=is_native)
        locations = res.values('location').annotate(total=Sum('new_user')).order_by('-total')[:10]
        dates = res.dates('date', 'day')
        for date in dates:
            temp = collections.OrderedDict()
            for item in locations:
                location = item['location']
                try:
                    query = res.filter(date=date, location=location).first()
                    temp[location] = query.new_user
                except AttributeError:
                    temp[location] = 0
            result[date.strftime('%m-%d')] = temp
        return JsonResponse(result,safe=False)
    else:
         return HttpResponse('Error.')


@csrf_exempt
def use_condition(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        result = []
        res = UseCondition.objects.filter(date__range=(start_time, end_time)).order_by('date')
        for item in res:
            temp = {'date': item.date.strftime('%m-%d'),'new_user': item.new_user,'active_user': item.active_user,'duration': item.duration}
            result.append(temp)
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def search_index(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        result = []
        res = SearchIndex.objects.filter(date__range=(start_time, end_time)).order_by('date')
        for item in res:
            temp = {'date': item.date.strftime('%m-%d'),'key': item.key,'baidu_index': item.baidu_index}
            result.append(temp)
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')


@csrf_exempt
def error_condition(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        result = []
        res = ErrorCondition.objects.filter(date__range=(start_time, end_time)).order_by('date')
        for item in res:
            temp = {'date': item.date.strftime('%m-%d'), 'total_error': item.total_error}
            result.append(temp)
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')


@csrf_exempt
def market_environment(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        result = collections.OrderedDict()
        res = SearchIndex.objects.filter(date__range=(start_time, end_time)).order_by('date')
        dates = res.dates('date', 'day')
        for date in dates:
            res_temp = res.filter(date=date)
            temp = {}
            for item in res_temp:
                temp[item.key] = item.baidu_index
            result[date.strftime('%m-%d')] = temp
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')


@csrf_exempt
def competitor_data(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        source = 'all'
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
            # endTime = datetime.datetime.strptime(para.__getitem__('end_time'), '%Y-%m-%d').date()
            # end_time = (endTime + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('source'):
            source = para.__getitem__('source')
        result = collections.OrderedDict()
        res = CompetitorSales.objects.filter(date__range=(start_time, end_time)).order_by('date')
        dates = res.dates('date', 'day')
        for date in dates:
            res_temp = res.filter(date=date)
            temp = collections.OrderedDict()
            if source == 'all':
                for item in res_temp:
                    temp[item.commodity + ' 淘宝'] = item.taobao_sales
                    temp[item.commodity + ' 京东'] = item.jd_sales
            elif source == 'taobao':
                for item in res_temp:
                    temp[item.commodity + ' 淘宝'] = item.taobao_sales
            elif source == 'jd':
                for item in res_temp:
                    temp[item.commodity + ' 京东'] = item.jd_sales
            result[date.strftime('%m-%d')] = temp
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        username = 'jack'
        password = 'slow fuck'
        if para.__contains__('username'):
            username = para.__getitem__('username')
        if para.__contains__('password'):
            password = para.__getitem__('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                res = []
                groups = user.groups.all()
                for group in groups:
                    res.append(group.name)
                return JsonResponse({'result':True, 'group':res},safe=False)
            else:
                return JsonResponse({'result':False},safe=False)

        else:
            return JsonResponse({'result':False},safe=False)
    else:
        return HttpResponse('Error.')


@csrf_exempt
def test(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        # t()
        return HttpResponse('Task submitted.')
    else:
        return HttpResponse('Error.')