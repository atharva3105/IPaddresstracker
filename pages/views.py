from django.shortcuts import render
import requests
import json
import re


# Create your views here.
def home_view(request, *args, **kwargs):
    ip_add = request.POST.get("ipadd")
    
    if ip_add == None or ip_add =="":
        ip_add = get_client_ip(request)
    elif isvalidIP(ip_add) == False:
        ip_add = get_client_ip(request)
        
        

    
    print(ip_add)
    
    context = getIPinfo(str(ip_add))
    
    p = json.loads(context)
    location = p['location']['city'] +", " + p['location']['region']+ ", " + p['location']['country']
    lat = p['location']['lat']
    lng = p['location']['lng']
    latlng = []
    latlng.append(lat)
    latlng.append(lng)
    context={
        "IP" : p['ip'],
        "LOC" : location,
        "LATLNG" : list(latlng),
        "ISP" : p['isp'],
        "TZ"  : p['location']['timezone'],
    }
    
    return render(request, "home.html", context)

#{'ip': '8.8.8.8', 'location': {'country': 'US', 'region': 'California', 'city': 'Mountain View', 'lat': 37.38605, 'lng': -122.08385, 'postalCode': '94035', 'timezone': '-08:00', 'geonameId': 5375480}, 'domains': ['andrewwheeler.net', 'grafana.rekola.wftech.eu', 'incubator.vodafone.de', 'ns2.bokomaroo.pw', 'ns2.jlebmilser.ru'], 'as': {'asn': 15169, 'name': 'GOOGLE', 'route': '8.8.8.0/24', 'domain': 'https://about.google/intl/en/', 'type': 'Content'}, 'isp': 'Google LLC'}
           

def getIPinfo(ipaddress):
    url = "https://geo.ipify.org/api/v2/country,city?apiKey=at_DKfO5k9ne5lzC0Ng9vkpENIx4XG86"
    final_url = url + "&ipAddress=" + ipaddress
    r = requests.get(final_url)
    return r.content

def isvalidIP(str):
    result = True
    match_obj = re.search( r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", str)
    if  match_obj is None:
        result = False
    else:
        for value in match_obj.groups():
            if int(value) > 255:
                result = False
                break
    return result

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip