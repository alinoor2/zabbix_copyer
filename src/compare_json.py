# This class is written to compare two dictionaries, in which one dictionary is considered as a reference.
# The difference in a part of the reference dictionary itself is tagged with the "stat" key and the value "YES"
# means non-existence in the destination dictionary or "NO" in the sense of existence in the destination dictionary.
# The dictionary structure is as follows:
# {host: {"hostid": r.json()["result"][i]["hostid"], "items": {{"itemid": "", "itemkey": "", "iteminterval": "",
# "itemunit": "", "itemstatus": "", "itemvaluetype": "", "stat": "NULL"}}, "stat": "NULL"}}


class JsonComparer(object):
    def __init__(self, ref, cpy):
        # The input to this class is a reference dictionary named "ref" and a copy dictionary named "cpy"
        self.dic_ref = ref
        self.dic_cpy = cpy
        self.out_dic = ref
        self.extract_name_items_diff()

    def extract_name_items_diff(self):
        for host in self.dic_ref:   # Read the reference dictionary for each host
            if host in self.dic_cpy:    # The comparison of hosts is done in the destination dictionary.
                # If the host is available, the existence of the items is checked
                self.out_dic[host]["stat"] = "NO"   # If present, the stat value is changed to "NO"
                for item in self.dic_ref[host]["items"]:
                    if item in self.dic_cpy[host]["items"]:   # If present, the stat value is changed to "NO" else "YES"
                        self.out_dic[host]["items"][item]["stat"] = "NO"
                    else:
                        self.out_dic[host]["items"][item]["stat"] = "YES"
            else:   # If the host isn't available, the stat values is changed to "YES"
                self.out_dic[host]["stat"] = "YES"
                for item in self.dic_ref[host]["items"]:
                    self.out_dic[host]["items"][item]["stat"] = "YES"
