import yaml

import src.get_item_zabbix as get
import src.compare_json as compare
import src.db_worker as db
import src.config as conf
import time

if __name__ == '__main__':
    start = time.time()
    getitems_host = get.GetItemsHosts()
    getitems_host.main()
    host_ref = getitems_host.hosts_ref
    host_cpy = getitems_host.hosts_cpy
    comp_items = compare.JsonComparer(host_ref, host_cpy)
    comp_items_dic = comp_items.out_dic
    with open('log/out_dic.yaml', "w") as f:
        f.write(yaml.dump(comp_items_dic, default_flow_style=False))
    db_ref = db.DataBaseLoader(conf.ZABBIX_REF_ADDRESS, host_ref)
    db_ref.insert_json_to_database()
    db_cpy = db.DataBaseLoader(conf.ZABBIX_CPY_ADDRESS, host_cpy)
    db_cpy.insert_json_to_database()

    end = time.time()
    total_time = end - start
    print("\n"+ str(total_time))
