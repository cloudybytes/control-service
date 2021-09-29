from user_sql_parse.sql_parse import Parse
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import yaml

# Create your views here.
@csrf_exempt
def user_sql_endpoint(request):
    if request.method == 'POST':
        schema = {}
        user_sql=request.POST['user_sql']
        with open('static/admin/schema.yaml', 'r') as file:
            schema = yaml.load(file, Loader=yaml.FullLoader)
        # user_sql = "Select userid, rating from users inner join rating on users.userid = rating.userid where rating > 3"
        # user_sql = "Select userid, rating from users where rating > 3 group by userid having min(userid) >= 3;"  
        print(user_sql)
        parsed_query = Parse(user_sql, schema).get_parsed_query()
        return JsonResponse(parsed_query)


