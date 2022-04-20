

class JsonComparer(object):
    def __init__(self, ref, cpy):
        self.dic_ref = ref
        self.dic_cpy = cpy
        self.out_dic = ref
        self.extract_name_items_diff()

    def extract_name_items_diff(self):
        for host in self.dic_ref:
            if host in self.dic_cpy:
                self.out_dic[host]["stat"] = "NO"
                for item in self.dic_ref[host]["items"]:
                    if item in self.dic_cpy[host]["items"]:
                        self.out_dic[host]["items"][item]["stat"] = "NO"
                    else:
                        self.out_dic[host]["items"][item]["stat"] = "YES"
            else:
                self.out_dic[host]["stat"] = "YES"
                for item in self.dic_ref[host]["items"]:
                    self.out_dic[host]["items"][item]["stat"] = "YES"
