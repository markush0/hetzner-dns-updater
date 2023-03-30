from fastapi import FastAPI
import re
import os
import requests
import json

app = FastAPI()
target_host = os.environ['target_host']
api_key = os.environ['api_key']
env_user = os.environ['user']
env_pass = os.environ['password']


def check_user(user, password):
    if user != env_user or password != env_pass:
        raise Exception('wrong credentials' + user)
    pass


def check_host(target_host, host):
    if host != target_host:
        raise Exception("wrong host" + host)
    pass


def check_ip(ip):
    pattern_str = '^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\\b){4}$'
    pattern = re.compile(pattern_str)
    m = pattern.fullmatch(ip)
    if not m:
        raise Exception("wrong ip: " + ip)
    pass


def check_ip6(ip6):
    if ip6 == '':
        return

    pattern_str = '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]' \
                  '{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]' \
                  '{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]' \
                  '{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|' \
                  '([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]' \
                  '{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}' \
                  '(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]' \
                  '{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]' \
                  '{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]' \
                  '{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}' \
                  '%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}' \
                  '((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.)' \
                  '{3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])' \
                  '|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9])' \
                  '{0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
    pattern = re.compile(pattern_str)
    m = pattern.fullmatch(ip6)
    if not m:
        raise Exception("wrong ip6" + ip6)
    pass


def get_all_records(zone_id, api_key):
    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/records",
            params={
                "zone_id": zone_id,
            },
            headers={
                "Auth-API-Token": api_key,
            },
        )
        #print('Response HTTP Status Code: {status_code}'.format(
        #    status_code=response.status_code))
        #print('Response HTTP Response Body: {content}'.format(
        #    content=response.content))
        return json.loads(response.content)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def update_record(a_record_id, zone_id, ip, api_key):

    try:
        response = requests.put(
            url="https://dns.hetzner.com/api/v1/records/"+a_record_id,
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": api_key,
            },
            data=json.dumps({
                "value": ip,
                "ttl": 0,
                "type": "A",
                "name": "www",
                "zone_id": zone_id
            })
        )
        #print('Response HTTP Status Code: {status_code}'.format(
        #    status_code=response.status_code))
        #print('Response HTTP Response Body: {content}'.format(
        #    content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    pass


def get_a_record_id(records):
    for r in records['records']:
        if r['type'] == 'A':
            return r['id']


def get_all_zones(api_key):
    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/zones",
            headers={
                "Auth-API-Token": api_key,
            },
        )
        #print('Response HTTP Status Code: {status_code}'.format(
        #    status_code=response.status_code))
        #print('Response HTTP Response Body: {content}'.format(
        #    content=response.content))
        return json.loads(response.content)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def get_host_zone(zones, host):
    for z in zones['zones']:
        if z['name'] == host:
            return z['id']


def call_api(host, ip, api_key):
    zones = get_all_zones(api_key)
    zone_id = get_host_zone(zones, host)
    records = get_all_records(zone_id, api_key)
    a_record_id = get_a_record_id(records)
    update_record(a_record_id, zone_id, ip, api_key)
    pass


@app.get("/ip/")
async def update_ip(user: str, password: str, host: str, ip: str, ip6: str = None):
    try:
        check_user(user, password)
        check_host(target_host, host)
        check_ip(ip)
        if not ip6:
            check_ip6(ip6)
        print("Updated zone: " + target_host + " with IP: " + ip + " " + ip6)
        call_api(host, ip, api_key)
        return("IP updated")
    except Exception as error:
        print(error)
        return str(error)
