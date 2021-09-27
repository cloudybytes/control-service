from user_sql_parse.sql_parse import Parse
from django.http.response import HttpResponse, JsonResponse
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
        # user_sql = "Select user_id, rating from users inner join rating on users.user_id = rating.user_id where rating.rating > 3"
        # user_sql = "Select user_id, rating from users where rating.rating > 3 group by user_id having min(user_id) >= 3;"  
        print(user_sql)
        parsed_query = Parse(user_sql).get_parsed_query()
        # tokenized_sql = user_sql_parse(user_sql)
        # return HttpResponse('reached here '+"".join(tokenized_sql))
        return JsonResponse(parsed_query)


