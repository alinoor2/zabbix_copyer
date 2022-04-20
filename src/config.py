import yaml

# ZABBIX_REF_ADDRESS = ''
# ZABBIX_REF_TOKEN = ''
# ZABBIX_CPY_ADDRESS = ''
# ZABBIX_CPY_TOKEN = ''
address = "config/config.yaml"
with open(address, "r") as f:
    conf_file = yaml.safe_load(f)

for zabb in conf_file:
    if conf_file[zabb]['type'] == 'ref':
        ZABBIX_REF_ADDRESS = 'http://{}/zabbix/api_jsonrpc.php'.format(conf_file[zabb]['addr'])
        ZABBIX_REF_TOKEN = conf_file[zabb]['token']
    elif conf_file[zabb]['type'] == 'cpy':
        ZABBIX_CPY_ADDRESS = 'http://{}/zabbix/api_jsonrpc.php'.format(conf_file[zabb]['addr'])
        ZABBIX_CPY_TOKEN = conf_file[zabb]['token']
