from user_sql_parse.sql_parse import Parse
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import yaml
import requests
from django.conf import settings
import json

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
        parsed_query = Parse(user_sql, schema).get_parsed_query()
        spark_result = call_service(parsed_query,settings.SPARK_ENDPOINT,"spark")
        storm_result = call_service(parsed_query,settings.STORM_ENDPOINT,"storm")
        hadoop_result = call_service(parsed_query,settings.HADOOP_ENDPOINT,"hadoop")
        result = {'spark_time' : spark_result['time'],'spark_url': spark_result['output_url'] ,'storm_time' : storm_result['time'],'storm_url': storm_result['output_url'],'hadoop_time' : hadoop_result['time'],'hadoop_url': hadoop_result['output_url'] }
        return JsonResponse(result)

def call_service(parsed_query,endpoint,service_name):    
    r = requests.post(endpoint, json=parsed_query)
    return r.json()

