# This class is written to compare two dictionaries, in which one dictionary is considered as a reference.
# The difference in a part of the reference dictionary itself is tagged with the "stat" key and the value "YES"
# means non-existence in the destination dictionary or "NO" in the sense of existence in the destination dictionary.
# The dictionary structure is as follows:
# {host: {"hostid": r.json()["result"][i]["hostid"], "items": {{"itemid": "", "itemkey": "", "iteminterval": "",
# "itemunit": "", "itemstatus": "", "itemvaluetype": "", "stat": "NULL"}}, "stat": "NULL"}}
import src.db_worker as dbw
import src.config as conf


class JsonComparer(object):
    def __init__(self, ref, cpy):
        # The input to this class is a reference dictionary named "ref" and a copy dictionary named "cpy"
        self.config = conf.ConfigParse()
        dbw.copy_database(self.config.ZABBIX_REF_ADDRESS)
        self.dic_ref = ref
        self.dic_cpy = cpy
        self.out_dic = ref
        self.out_dic["Zabbix server copy"] = self.out_dic["Zabbix server"]
        self.out_list = [[], []]  # [[different hostname list], [different items list]]
        self.extract_name_items_diff()

    def extract_name_items_diff(self):
        for host in self.dic_ref:  # Read the reference dictionary for each host
            if ("Zabbix server copy" if host == "Zabbix server" else host) in self.dic_cpy:
                # The comparison of hosts is done in the destination dictionary.
                # If the host is available, the existence of the items is checked
                self.out_dic["Zabbix server copy" if host == "Zabbix server" else host]["stat"] = "NO"
                dbw.change_host_value_db(self.config.ZABBIX_REF_ADDRESS,
                                         self.dic_ref["Zabbix server copy" if host == "Zabbix server" else host][
                                             "hostid"],
                                         "stat", "NO")
                # If present, the stat value is changed to "NO"
                for item in self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"]:
                    if item in self.dic_cpy["Zabbix server copy" if host == "Zabbix server" else host]["items"]:
                        # If present, the stat value is changed to "NO" else "YES"
                        self.out_dic["Zabbix server copy" if host == "Zabbix server" else host]["items"][item]["stat"] \
                            = "NO"
                        dbw.change_item_value_db(self.config.ZABBIX_REF_ADDRESS,
                                                 self.dic_ref[
                                                     "Zabbix server copy" if host == "Zabbix server" else host][
                                                     "hostid"],
                                                 self.out_dic[
                                                     "Zabbix server copy" if host == "Zabbix server" else host][
                                                     "items"][item]["itemid"],
                                                 "stat", "NO")
                    else:
                        self.out_dic["Zabbix server copy" if host == "Zabbix server" else host]["items"][item]["stat"] \
                            = "YES"
                        dbw.change_item_value_db(self.config.ZABBIX_REF_ADDRESS,
                                                 self.dic_ref[
                                                     "Zabbix server copy" if host == "Zabbix server" else host][
                                                     "hostid"],
                                                 self.out_dic[
                                                     "Zabbix server copy" if host == "Zabbix server" else host][
                                                     "items"][item]["itemid"],
                                                 "stat", "YES")
                        intervale = '5m' if \
                            self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                                "iteminterval"] == '0' else \
                            self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                                "iteminterval"]
                        item_new = ["Zabbix server copy" if host == "Zabbix server" else host,
                                    self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["hostid"],
                                    self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][
                                        item]["itemid"],
                                    item,
                                    self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][
                                        item]["itemkey"],
                                    intervale,
                                    self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][
                                        item]["itemunit"],
                                    self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][
                                        item]["itemstatus"],
                                    self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][
                                        item]["itemvaluetype"],
                                    self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][
                                        item]["stat"]]
                        self.out_list[1].append(item_new)
            else:  # If the host isn't available, the stat values is changed to "YES"
                self.out_dic["Zabbix server copy" if host == "Zabbix server" else host]["stat"] = "YES"
                host_id = self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["hostid"]
                host_new = ["Zabbix server copy" if host == "Zabbix server" else host, host_id]
                self.out_list[0].append(host_new)
                for item in self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"]:
                    host = "Zabbix server" if host == "Zabbix server copy" else host
                    self.out_dic["Zabbix server copy" if host == "Zabbix server" else host]["items"][item][
                        "stat"] = "YES"
                    intervale = '5m' if \
                    self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                        "iteminterval"] == '0' else \
                        self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                            "iteminterval"]
                    item_new = ["Zabbix server copy" if host == "Zabbix server" else host,
                                self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["hostid"],
                                self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                                    "itemid"],
                                item,
                                self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                                    "itemkey"],
                                intervale,
                                self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                                    "itemunit"],
                                self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                                    "itemstatus"],
                                self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                                    "itemvaluetype"],
                                self.dic_ref["Zabbix server" if host == "Zabbix server copy" else host]["items"][item][
                                    "stat"]]
                    self.out_list[1].append(item_new)
