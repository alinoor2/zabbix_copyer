import yaml


class ConfigParse(object):
    def __init__(self):
        self.ZABBIX_REF_ADDRESS = ''
        self.ZABBIX_REF_TOKEN = ''
        self.ZABBIX_CPY_ADDRESS = ''
        self.ZABBIX_CPY_TOKEN = ''
        self.ZABBIX_GROUP_DEF = ''
        self.LOG_FILE_ADDRESS = ''
        self.LOGGING_LEVEL = ''
        self.conf_json = {}
        self.address = "config/config.yaml"
        self.load_config_file()

    def load_config_file(self):
        with open(self.address, "r") as f:
            self.conf_json = yaml.safe_load(f)

        for zabbix in self.conf_json["zabbix's"]:
            if self.conf_json["zabbix's"][zabbix]['type'] == 'ref':
                self.ZABBIX_REF_ADDRESS = 'http://{}/zabbix/api_jsonrpc.php'.format(self.conf_json["zabbix's"][zabbix]['addr'])
                self.ZABBIX_REF_TOKEN = self.conf_json["zabbix's"][zabbix]['token']
            elif self.conf_json["zabbix's"][zabbix]['type'] == 'cpy':
                self.ZABBIX_CPY_ADDRESS = 'http://{}/zabbix/api_jsonrpc.php'.format(self.conf_json["zabbix's"][zabbix]['addr'])
                self.ZABBIX_CPY_TOKEN = self.conf_json["zabbix's"][zabbix]['token']

        self.ZABBIX_GROUP_DEF = self.conf_json["general"]["group_host"]
        self.LOG_FILE_ADDRESS = self.conf_json["general"]["log_file_address"]
        self.LOGGING_LEVEL = self.conf_json["general"]["logging_level"]
