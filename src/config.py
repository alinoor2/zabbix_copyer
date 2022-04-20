import yaml
root_folder = 'C:\\Users\\Internet\\Documents\\python projects\\zabbix_copyer'
ZABBIX_REF_ADDRESS = ''
ZABBIX_REF_TOKEN = ''
ZABBIX_CPY_ADDRESS = ''
ZABBIX_CPY_TOKEN = ''
address = "{}/config/config.yaml".format(root_folder)
with open(address, "r") as f:
    conf_file = yaml.safe_load(f)
print(conf_file)

for zabb in conf_file:
    if conf_file[zabb]['type'] == 'ref':
        ZABBIX_REF_ADDRESS = 'http://{}/zabbix/api_jsonrpc.php'.format(conf_file[zabb]['addr'])
        ZABBIX_REF_TOKEN = conf_file[zabb]['token']
    elif conf_file[zabb]['type'] == 'cpy':
        ZABBIX_CPY_ADDRESS = 'http://{}/zabbix/api_jsonrpc.php'.format(conf_file[zabb]['addr'])
        ZABBIX_CPY_TOKEN = conf_file[zabb]['token']

print("ZABBIX_REF_ADDRESS: {}".format(ZABBIX_REF_ADDRESS))
print("ZABBIX_REF_TOKEN: {}".format(ZABBIX_REF_TOKEN))
print("ZABBIX_CPY_ADDRESS: {}".format(ZABBIX_CPY_ADDRESS))
print("ZABBIX_CPY_TOKEN: {}".format(ZABBIX_CPY_TOKEN))