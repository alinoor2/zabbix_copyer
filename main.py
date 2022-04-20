import src.get_item_zabbix as get
import src.compare_json as compare
import src.db_worker as db
import src.config as conf
import time

if __name__ == '__main__':
    start = time.time()
    getitems_hostref = get.GetItemsHosts(zabbixip="192.168.0.29",
                                         token="1eb1a810f7ecaa0d6e33a30fe43d0f5a849aa31ff6ac5ddfc6bb88e02efa2326",
                                         types="ref")
    getitems_hostcpy = get.GetItemsHosts(zabbixip="192.168.0.31",
                                         token="a66bfc4d120a5357ec2b75cfab84be67b9eb8c52c76dbc4d1f4e9cfebb33bc0d")
    end = time.time()
    total_time = end - start
    print("\n"+ str(total_time))