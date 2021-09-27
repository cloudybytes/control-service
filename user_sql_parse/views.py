from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def user_sql_parse(sql_string):
    tokenized_sql = sql_string.split()
    return tokenized_sql

@csrf_exempt
def user_sql_endpoint(request):
    if request.method == 'POST':
        user_sql=request.POST['user_sql']
        tokenized_sql = user_sql_parse(user_sql)
        return HttpResponse('reached here '+"".join(tokenized_sql))


