# In this class, work is done on the Sqlite database.
# The outputs that need to be stored due to data security are stored in a database based on pre-designed tables.
# And read database
import os
import sqlite3
import shutil


def copy_database(zabbix_address):
    zabbix_db_name_old = "../dbs/output_{}db.sqlite".format(zabbix_address.split('.')[2] + '_' +
                                                            zabbix_address.split('.')[3].split('/')[0])
    zabbix_db_name_new = "../dbs/output_{}_diff_db.sqlite".format(zabbix_address.split('.')[2] + '_' +
                                                                  zabbix_address.split('.')[3].split('/')[0])
    if not os.path.isfile(zabbix_db_name_new):
        shutil.copy(zabbix_db_name_old, zabbix_db_name_new)
    conn = sqlite3.connect(zabbix_db_name_new)
    curs = conn.cursor()
    command = 'ALTER TABLE host_detailes ADD COLUMN host_copy_id VARCHAR'
    curs.execute('PRAGMA table_info("host_detailes")')
    out = curs.fetchall()
    flag = 0
    for i in range(len(out)):
        if "host_copy_id" in out[i]:
            flag = 1
    if flag == 0:
        curs.execute(command)
    conn.commit()



def change_item_value_db(zabbix_address, host_id, item_id, column, new_value):
    zabbix_db_name = "../dbs/output_{}db.sqlite".format(zabbix_address.split('.')[2] + '_' +
                                                        zabbix_address.split('.')[3].split('/')[0])
    connect = sqlite3.connect(zabbix_db_name)
    cursor = connect.cursor()
    command = 'UPDATE host_details SET "{}"="{}" WHERE hostid = "{}" AND itemid = "{}"'.format(column, new_value,
                                                                                               host_id, item_id)
    cursor.execute(command)
    connect.commit()


def change_host_value_db(zabbix_address, id_num, column, new_value):
    zabbix_db_name = "../dbs/output_{}db.sqlite".format(zabbix_address.split('.')[2] + '_' +
                                                        zabbix_address.split('.')[3].split('/')[0])
    connect = sqlite3.connect(zabbix_db_name)
    cursor = connect.cursor()
    command = 'UPDATE hosts_name SET "{}"="{}" WHERE hostid = "{}"'.format(column, new_value, id_num)
    cursor.execute(command)
    connect.commit()


class DataBaseLoader(object):
    def __init__(self, zabbix_address, hosts_dic):
        # input from class is zabbix address for create
        # database name and hosts detail dict
        self.output_data = None
        self.zabbix_db_name = "../dbs/output_{}db.sqlite".format(zabbix_address.split('.')[2] + '_' +
                                                              zabbix_address.split('.')[3].split('/')[0])
        self.hosts_dic = hosts_dic

    def insert_json_to_database(self):
        connect = sqlite3.connect(self.zabbix_db_name)
        cursor = connect.cursor()
        try:
            cursor.execute('CREATE TABLE hosts_name (hostname VARCHAR, hostid VARCHAR, stat VARCHAR)')
            cursor.execute('CREATE TABLE host_detailes (hostid VARCHAR, itemid VARCHAR, itemname VARCHAR, '
                           'itemkey VARCHAR, iteminterval VARCHAR, itemunit VARCHAR, itemstatus VARCHAR, '
                           'itemvaluetype VARCHAR, stat VARCHAR)')
        except:
            pass
        for host in self.hosts_dic:
            command = 'INSERT INTO hosts_name (hostname, hostid) SELECT "{0}", ' \
                      '"{1}" WHERE NOT EXISTS(SELECT 1 FROM hosts_name WHERE hostname = ' \
                      '"{0}" AND hostid =  "{1}")'.format(host, self.hosts_dic[host]["hostid"])
            cursor.execute(command)
            for item in self.hosts_dic[host]["items"]:
                item.replace('"', '')
                command = 'INSERT INTO host_detailes (hostid, itemid, itemname, itemkey, iteminterval, itemunit, ' \
                          'itemstatus, itemvaluetype, stat) SELECT "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", ' \
                          '"{7}" , "{8}" WHERE NOT EXISTS(SELECT 1 FROM host_detailes WHERE hostid =  "{0}" AND ' \
                          'itemname = "{2}")'.format(self.hosts_dic[host]["hostid"],
                                                     self.hosts_dic[host]["items"][item]["itemid"],
                                                     item.replace('"', ''),
                                                     self.hosts_dic[host]["items"][item]["itemkey"].replace('"', ''),
                                                     self.hosts_dic[host]["items"][item]["iteminterval"],
                                                     self.hosts_dic[host]["items"][item]["itemunit"],
                                                     self.hosts_dic[host]["items"][item]["itemstatus"],
                                                     self.hosts_dic[host]["items"][item]["itemvaluetype"],
                                                     self.hosts_dic[host]["items"][item]["stat"])
                try:
                    cursor.execute(command)
                except:
                    pass
        connect.commit()

    def read_from_database(self):
        connect = sqlite3.connect(self.zabbix_db_name)
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM host_detailes')
        self.output_data = cursor.fetchall()


# change_host_value_db("192.168.0.29", "hosts_name", "10517", "stat", "NO")
# conn = sqlite3.connect("../dbs/output_0_29db.sqlite")
# curs = conn.cursor()
# command = 'PRAGMA table_info("")'
# curs.execute('PRAGMA table_info("host_detailes")')
# out = curs.fetchall()
# for i in range(len(out)):
#     if "stat" in out[i]:
#         print("yes")

# conn.commit()
copy_database("192.168.0.29")