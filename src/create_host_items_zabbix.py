import json
import requests


def create_host_group(zabbix_address, zabbix_token, group_name):
    r = requests.post(zabbix_address,
                      json={
                          "jsonrpc": "2.0",
                          "method": "hostgroup.create",
                          "params": {
                              "name": group_name
                          },
                          "auth": zabbix_token,
                          "id": 1
                      })
    return r.json()


def get_host_group(group_name, zabbix_address, zabbix_token):
    r = requests.post(zabbix_address,
                      json={
                          "jsonrpc": "2.0",
                          "method": "hostgroup.get",
                          "params": {
                              "output": "extend",
                              "filter": {
                                  "name": [
                                      group_name
                                  ]
                              }
                          },
                          "auth": zabbix_token,
                          "id": 1
                      })
    return r.json()["result"][0]["groupid"]


def create_host(group_name, zabbix_address, zabbix_token):
    group_id = get_host_group(group_name, zabbix_address, zabbix_token)
    r = requests.post(zabbix_address,
                      json={
                          "jsonrpc": "2.0",
                          "method": "host.create",
                          "params": {
                              "host": "Host test",

                              "groups": [
                                  {
                                      "groupid": group_id
                                  }
                              ],

                          },
                          "auth": zabbix_token,
                          "id": 1
                      }
                      )
    return r.json()


def get_host_id(host_name, zabbix_address, zabbix_token):
    r = requests.post(zabbix_address,
                      json={
                          "jsonrpc": "2.0",
                          "method": "host.get",
                          "params": {
                              "filter": {
                                  "host": [
                                      host_name
                                  ],
                              },
                          },
                          "auth": zabbix_token,
                          "id": 1
                      }
                      )
    return r.json()["result"][0]["hostid"]


def create_new_host(host_name, group_name, zabbix_address, zabbix_token):
    group_id = get_host_group(group_name, zabbix_address, zabbix_token)
    r = requests.post(zabbix_address,
                      json={
                          "jsonrpc": "2.0",
                          "method": "host.create",
                          "params": {
                              "host": host_name,
                              "groups": [
                                  {
                                      "groupid": group_id
                                  }
                              ],
                          },
                          "auth": zabbix_token,
                          "id": 1
                      }
                      )
    if "error" not in r.json():
        return r.json()["result"][0]["hostids"]
    elif "error" in r.json() and "already exists" in r.json()["error"]["data"]:
        return get_host_id(host_name, zabbix_address, zabbix_token)
    else:
        return r.json()["error"]["data"]


def get_item_id(hostid, item_name, zabbix_address, zabbix_token):
    r = requests.post(zabbix_address,
                      json={
                          "jsonrpc": "2.0",
                          "method": "item.get",
                          "params": {
                              "hostids": hostid,
                              "filter": {
                                  "name": item_name,
                              },
                          },
                          "auth": zabbix_token,
                          "id": 1
                      }
                      )
    return r.json()["result"][0]["itemid"]


def create_update_item(host_id, item_name, itemkey, item_delay, item_valuetype, item_unit, host_id_ref,
                       zabbix_cpy_address, zabbix_cpy_token, zabbix_ref_address, zabbix_ref_token):

    global r1
    query_field = [{"Content-Type": "application/json-rpc"}]
    query_posts = {"jsonrpc": "2.0",
                   "method": "item.get",
                   "params":
                       {
                           "output": "extend",
                           "hostids": host_id_ref,
                           "search":
                               {
                                   "key_": itemkey
                               },
                           "sortfield": "name"
                       },
                   "auth": zabbix_ref_token,
                   "id": 1
                   }
    query_posts = json.dumps(query_posts)
    # query_create =
    try:
        r1 = requests.post(zabbix_cpy_address,
                           json={
                              "jsonrpc": "2.0",
                              "method": "item.create",
                              "auth": zabbix_cpy_token,
                              "id": 1,
                              "params": {
                                  "name": item_name,
                                  "key_": itemkey,
                                  "hostid": host_id,
                                  "value_type": item_valuetype,
                                  "type": "19",  # Http_agent
                                  "units": item_unit,
                                  "delay": item_delay,
                                  "url": zabbix_ref_address,
                                  "authtype": 0,
                                  "request_method": 1,
                                  "retrieve_mode": 0,
                                  "query_fields": query_field,
                                  "posts": query_posts,
                                  "post_type": 2,
                                  "preprocessing": [
                                      {
                                          "type": "12",  # json-path
                                          "params": "$.result[0].lastvalue",
                                          "error_handler": "1",
                                          "error_handler_params": ""
                                      }
                                  ]
                              }
                           }
                           )
    except KeyError as er:
        pass
    if "already exists" in r1.json()['error']['data']:
        item_id = get_item_id(host_id, item_name, zabbix_cpy_address, zabbix_cpy_token)
        r = requests.post(zabbix_cpy_address,
                          json={
                              "jsonrpc": "2.0",
                              "method": "item.update",
                              "auth": zabbix_cpy_token,
                              "id": 1,
                              "params": {
                                  "itemid": item_id,
                                  "name": item_name,
                                  "key_": itemkey,
                                  "hostid": host_id,
                                  "value_type": item_valuetype,
                                  "type": "19",  # Http_agent
                                  "units": item_unit,
                                  "delay": item_delay,
                                  "url": zabbix_ref_address,
                                  "authtype": 0,
                                  "request_method": 1,
                                  "retrieve_mode": 0,
                                  "query_fields": query_field,
                                  "posts": query_posts,
                                  "post_type": 2,
                                  "preprocessing": [
                                      {
                                          "type": "12",  # json-path
                                          "params": "$.result[0].lastvalue",
                                          "error_handler": "1",
                                          "error_handler_params": ""
                                      }
                                  ]
                              }
                          }
                          )
        return r.json()
    else:
        return r1.json()


def get_item(host_id, item_key, zabbix_address, zabbix_token):
    r = requests.post(zabbix_address,
                      json={
                          "jsonrpc": "2.0",
                          "method": "item.get",
                          "params": {
                              "output": "extend",
                              "hostids": host_id,
                              "search": {
                                  "key_": item_key
                              },
                              "sortfield": "name"
                          },

                          "id": 2,
                          "auth": zabbix_token
                      })
    return r.json()["result"][0]


# TODO develop create items from list of object or database
def create_new_items(hostid, items: list):
    for item in items:
        pass

    pass


