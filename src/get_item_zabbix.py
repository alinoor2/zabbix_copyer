import requests
import json
import yaml
import src.config as conf


class GetItemsHosts(object):

    def __init__(self):
        self.hosts_ref = {}
        self.hosts_cpy = {}

        self.main()

    def get_host_ref(self):
        r = requests.post(conf.ZABBIX_REF_ADDRESS,
                          json={
                              "jsonrpc": "2.0",
                              "method": "host.get",
                              "params": {
                                  "output": "extend",
                                  "selectAcknowledges": "extend"
                              },
                              "id": 2,
                              "auth": conf.ZABBIX_REF_TOKEN
                          })
        for i in range(len(r.json()["result"])):
            host = {"hostid": r.json()["result"][i]["hostid"], "items": {}, "stat": "NULL"}
            self.hosts_ref[r.json()["result"][i]["host"]] = host

    def get_host_cpy(self):
        r = requests.post(conf.ZABBIX_CPY_ADDRESS,
                          json={
                              "jsonrpc": "2.0",
                              "method": "host.get",
                              "params": {
                                  "output": "extend",
                                  "selectAcknowledges": "extend"
                              },
                              "id": 2,
                              "auth": conf.ZABBIX_CPY_TOKEN
                          })
        for i in range(len(r.json()["result"])):
            host = {"hostid": r.json()["result"][i]["hostid"], "items": {}}
            self.hosts_cpy[r.json()["result"][i]["host"]] = host

    def get_item_from_host(self, hostid, hostname, zabbix_address, zabbix_token, zabbix_type):
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
            item = {"itemid": "", "itemkey": "", "iteminterval": "", "itemunit": "", "itemstatus": "",
                    "itemvaluetype": "", "stat": "NULL"}
            item = {"itemid": r.json()["result"][i]["itemid"], "itemkey": r.json()["result"][i]["key_"],
                    "iteminterval": r.json()["result"][i]["delay"],
                    "itemunit": r.json()["result"][i]["units"], "itemstatus": r.json()["result"][i]["status"],
                    "itemvaluetype": r.json()["result"][i]["value_type"], "stat": "NULL"}
            items[r.json()["result"][i]["name"]] = item
        if zabbix_type == 'ref':
            self.hosts_ref[hostname]["items"] = items
        elif zabbix_type == 'cpy':
            self.hosts_cpy[hostname]["items"] = items

    def convert_dict_to_yaml(self, dict_name, zabbix_address):
        z_na = "{}.{}".format(zabbix_address.split(".")[2], zabbix_address.split(".")[3].split('/')[0])
        filename = "output.{}.yaml".format(z_na)
        with open(filename, "w") as f:
            f.write(yaml.dump(dict_name, default_flow_style=False))

    def main(self):
        self.get_host_ref()
        self.get_host_cpy()
        for dic in [self.hosts_ref, self.hosts_cpy]:
            for host in dic:
                self.get_item_from_host(dic[host]["hostid"], host)

        # self.insert_json_to_database()
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.hosts, f, ensure_ascii=False, indent=4)
        # self.read_from_database()
        # self.convert_dict_to_yaml()
