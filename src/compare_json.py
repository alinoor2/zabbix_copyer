import json
from pprint import pprint

class JsonCamparer(object):
    def __init__(self, reff, copys):
        self.file_ref = reff
        self.file_cpy = copys
        self.json_ref = {}
        self.json_cpy = {}

    def _load_json_from_file(self):
        with open(self.file_ref, 'r') as f:
            self.json_ref = json.load(f)
        with open(self.file_cpy, 'r') as f:
            self.json_cpy = json.load(f)

    def _extract_name_items_diff(self):
        for host in self.json_ref:
            if host in self.json_cpy:
                self.json_ref[host]["stat"] = "NO"
                for item in self.json_ref[host]["items"]:
                    if item in self.json_cpy[host]["items"]:
                        self.json_ref[host]["items"][item]["stat"] = "NO"
                    else:
                        self.json_ref[host]["items"][item]["stat"] = "YES"
            else:
                self.json_ref[host]["stat"] = "YES"
                for item in self.json_ref[host]["items"]:
                    self.json_ref[host]["items"][item]["stat"] = "YES"

    def main(self):
        self._load_json_from_file()
        self._extract_name_items_diff()



if __name__ == '__main__':
    test = JsonCamparer('/home/python/log/output_0_29.json', '/home/python/log/output_0_31.json')
    test.main()


