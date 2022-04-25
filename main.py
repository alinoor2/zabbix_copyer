import yaml
import time
import logging
import src.get_item_zabbix as get
import src.compare_json as compare
import src.db_worker as db
import src.config as conf


def main():
    config = conf.ConfigParse()
    getitems_host = get.GetItemsHosts(config)
    comp_items = compare.JsonComparer(getitems_host.hosts_ref, getitems_host.hosts_cpy)
    comp_items_dic = comp_items.out_dic
    logging_level = config.LOGGING_LEVEL
    if logging_level == "DEBUG":
        logging.basicConfig(filename=config.LOG_FILE_ADDRESS, level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(filename=config.LOG_FILE_ADDRESS, level=logging.CRITICAL,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    with open('old_log/out_dic.yaml', "w") as f:
        f.write(yaml.dump(comp_items_dic, default_flow_style=False))
    db_ref = db.DataBaseLoader(config.ZABBIX_REF_ADDRESS, getitems_host.hosts_ref)
    db_ref.insert_json_to_database()
    db_cpy = db.DataBaseLoader(config.ZABBIX_CPY_ADDRESS, getitems_host.hosts_cpy)
    db_cpy.insert_json_to_database()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    total_time = end - start
    print("\n" + str(total_time))
