# This class collects the necessary information from the configured
# host in the configuration file using the Http Request feature.
import requests
import yaml
import threading
import time
import src.config as conf


def get_item_from_host(hostid, zabbix_address, zabbix_token):
    # This function is based on the requested inputs, which include hostid, hostname, zabbix_address,
    # zabbix_token, zabbix_type (ref or cpy).
    # Prepares the output as a dictionary as follows
    items = {}
    r = requests.post(zabbix_address,
                      json={
                          "jsonrpc": "2.0",
                          "method": "item.get",
                          "params": {
                              "output": "extend",
                              "hostids": hostid,
                              "search": {
                              },
                              "sortfield": "name"
                          },

                          "id": 2,
                          "auth": zabbix_token
                      })

    for i in range(len(r.json()["result"])):
        # item = {"itemid": "", "itemkey": "", "iteminterval": "", "itemunit": "", "itemstatus": "",
        #         "itemvaluetype": "", "stat": "NULL"}
        item = {"itemid": r.json()["result"][i]["itemid"],
                "itemkey": r.json()["result"][i]["key_"],
                "iteminterval": r.json()["result"][i]["delay"],
                "itemunit": r.json()["result"][i]["units"],
                "itemstatus": r.json()["result"][i]["status"],
                "itemvaluetype": r.json()["result"][i]["value_type"],
                "stat": "NULL"}
        items[r.json()["result"][i]["name"]] = item
    return items


class GetItemsHosts(object):
    def __init__(self, config_dict):
        self.conf = config_dict
        self.hosts_ref = {}  # output dictionary of reference host
        self.hosts_cpy = {}  # output dictionary of copy host
        self.get_host_ref()
        self.get_host_cpy()

    def get_item_from_host(self, hostid, hostname, zabbix_address, zabbix_token, host_rule):
        # This function is based on the requested inputs, which include hostid, hostname, zabbix_address,
        # zabbix_token, zabbix_type (ref or cpy).
        # Prepares the output as a dictionary as follows
        items = {}
        r = requests.post(zabbix_address,
                          json={
                              "jsonrpc": "2.0",
                              "method": "item.get",
                              "params": {
                                  "output": "extend",
                                  "hostids": hostid,
                                  "search": {
                                  },
                                  "sortfield": "name"
                              },

                              "id": 2,
                              "auth": zabbix_token
                          })

        for i in range(len(r.json()["result"])):
            # item = {"itemid": "", "itemkey": "", "iteminterval": "", "itemunit": "", "itemstatus": "",
            #         "itemvaluetype": "", "stat": "NULL"}
            item = {"itemid": r.json()["result"][i]["itemid"],
                    "itemkey": r.json()["result"][i]["key_"],
                    "iteminterval": r.json()["result"][i]["delay"],
                    "itemunit": r.json()["result"][i]["units"],
                    "itemstatus": r.json()["result"][i]["status"],
                    "itemvaluetype": r.json()["result"][i]["value_type"],
                    "stat": "NULL"}
            items[r.json()["result"][i]["name"]] = item
        host = {"hostid": [hostid], "items": items, "stat": "NULL"}
        if host_rule == 'ref':
            self.hosts_ref[hostname] = host
        elif host_rule == 'cpy':
            self.hosts_cpy[hostname] = host

    def get_host_ref(self):
        host_rule = 'ref'
        r = requests.post(self.conf.ZABBIX_REF_ADDRESS,  # send request to reference zabbix for get hosts detail
                          # with zabbix notation mode
                          json={
                              "jsonrpc": "2.0",
                              "method": "host.get",
                              "params": {
                                  "output": "extend",
                                  "selectAcknowledges": "extend"
                              },
                              "id": 2,
                              "auth": self.conf.ZABBIX_REF_TOKEN
                          })
        for i in range(len(r.json()["result"])):  # parse output json from request and written to output dict
            # thread_i = threading.Thread(target=self.get_item_from_host, args=(r.json()["result"][i]["hostid"], i,
            #                             self.conf.ZABBIX_REF_ADDRESS,
            #                             self.conf.ZABBIX_REF_TOKEN, host_rule))
            # thread_i.start()
            # thread_i.join()
            items = get_item_from_host(r.json()["result"][i]["hostid"],
                                       self.conf.ZABBIX_REF_ADDRESS,
                                       self.conf.ZABBIX_REF_TOKEN)
            host = {"hostid": r.json()["result"][i]["hostid"], "items": items, "stat": "NULL"}
            self.hosts_ref[r.json()["result"][i]["host"]] = host
        self.convert_dict_to_yaml(host_rule)

    def get_host_cpy(self):
        host_rule = 'cpy'
        r = requests.post(self.conf.ZABBIX_CPY_ADDRESS,  # send request to copy zabbix for get hosts detail
                          # with zabbix notation mode
                          json={
                              "jsonrpc": "2.0",
                              "method": "host.get",
                              "params": {
                                  "output": "extend",
                                  "selectAcknowledges": "extend"
                              },
                              "id": 2,
                              "auth": self.conf.ZABBIX_CPY_TOKEN
                          })
        for i in range(len(r.json()["result"])):  # parse output json from request and written to output dict
            # thread_i = threading.Thread(target=self.get_item_from_host, args=(r.json()["result"][i]["hostid"], i,
            #                                                                   self.conf.ZABBIX_REF_ADDRESS,
            #                                                                   self.conf.ZABBIX_REF_TOKEN, host_rule))
            # thread_i.start()
            # thread_i.join()
            items = get_item_from_host(r.json()["result"][i]["hostid"],
                                       self.conf.ZABBIX_CPY_ADDRESS,
                                       self.conf.ZABBIX_CPY_TOKEN)
            host = {"hostid": r.json()["result"][i]["hostid"], "items": items}
            self.hosts_cpy[r.json()["result"][i]["host"]] = host
        self.convert_dict_to_yaml(host_rule)

    def convert_dict_to_yaml(self, typ):
        # This function stores its input dictionary in a file
        # in the "log/" path in Yaml format
        if typ == 'ref':
            z_na = "log/output_{}_{}.yaml".format(self.conf.ZABBIX_REF_ADDRESS.split(".")[2],
                                                  self.conf.ZABBIX_REF_ADDRESS.split(".")[3].split('/')[0])
            with open(z_na, "w") as f:
                f.write(yaml.dump(self.hosts_ref, default_flow_style=False))
        elif typ == 'cpy':
            z_na = "log/output_{}_{}.yaml".format(self.conf.ZABBIX_CPY_ADDRESS.split(".")[2],
                                                  self.conf.ZABBIX_CPY_ADDRESS.split(".")[3].split('/')[0])
            with open(z_na, "w") as f:
                f.write(yaml.dump(self.hosts_cpy, default_flow_style=False))
