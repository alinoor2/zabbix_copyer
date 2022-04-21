# In this class, work is done on the Sqlite database.
# The outputs that need to be stored due to data security are stored in a database based on pre-designed tables.
# And read database

import sqlite3
import src.config as conf


class DataBaseLoader(object):
    def __init__(self, zabbix_address, hosts_dic):
        # input from class is zabbix address for create
        # database name and hosts detail dict
        self.output_data = None
        self.zabbix_db_name = "dbs/output_{}db.sqlite".format(zabbix_address.split('.')[2] + '_' +
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

    # def insert_json_to_database(self):
    #     connect = sqlite3.connect(self.zabbix_db_name_cpy)
    #     cursor = connect.cursor()
    #     try:
    #         if self.zabbix_type == "ref":
    #             cursor.execute('CREATE TABLE hosts_name (hostname VARCHAR, hostid VARCHAR, stat VARCHAR)')
    #         elif self.zabbix_type == "cpy":
    #             cursor.execute('CREATE TABLE hosts_name (hostname VARCHAR, hostid VARCHAR)')
    #         else:
    #             pass
    #         if self.zabbix_type == "ref":
    #             cursor.execute('CREATE TABLE host_detailes (hostid VARCHAR, itemid VARCHAR, itemname VARCHAR, itemkey VARCHAR, iteminterval VARCHAR, \
    #                 itemunit VARCHAR, itemstatus VARCHAR, itemvaluetype VARCHAR, stat VARCHAR)')
    #         elif self.zabbix_type == "cpy":
    #             cursor.execute('CREATE TABLE host_detailes (hostid VARCHAR, itemid VARCHAR, itemname VARCHAR, itemkey VARCHAR, iteminterval VARCHAR, \
    #                 itemunit VARCHAR, itemstatus VARCHAR, itemvaluetype VARCHAR)')
    #         else:
    #             pass
    #
    #     except:
    #         pass
    #     for host in self.hosts:
    #         command = 'INSERT INTO hosts_name (hostname, hostid) SELECT "{0}", "{1}" WHERE NOT EXISTS(SELECT 1 FROM hosts_name WHERE hostname = \
    #             "{0}" AND hostid =  "{1}")'.format(host, self.hosts[host]["hostid"])
    #         cursor.execute(command)
    #         for item in self.hosts[host]["items"]:
    #             # print(item)
    #             item.replace('"', '')
    #             if self.zabbix_type == "ref":
    #                 command = 'INSERT INTO host_detailes (hostid, itemid, itemname, itemkey, iteminterval, itemunit, itemstatus, itemvaluetype, stat) SELECT \
    #                     "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}" , "{8}" WHERE NOT EXISTS(SELECT 1 FROM host_detailes WHERE hostid =  "{0}" AND \
    #                         itemname = "{2}")'.format(self.hosts[host]["hostid"],
    #                                                   self.hosts[host]["items"][item]["itemid"],
    #                                                   item.replace('"', ''), \
    #                                                   self.hosts[host]["items"][item]["itemkey"].replace('"', ''),
    #                                                   self.hosts[host]["items"][item]["iteminterval"], \
    #                                                   self.hosts[host]["items"][item]["itemunit"],
    #                                                   self.hosts[host]["items"][item]["itemstatus"], \
    #                                                   self.hosts[host]["items"][item]["itemvaluetype"],
    #                                                   self.hosts[host]["items"][item]["stat"])
    #             else:
    #                 command = 'INSERT INTO host_detailes (hostid, itemid, itemname, itemkey, iteminterval, itemunit, itemstatus, itemvaluetype) SELECT \
    #                     "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}"  WHERE NOT EXISTS(SELECT 1 FROM host_detailes WHERE hostid =  "{0}" AND \
    #                         itemname = "{2}")'.format(self.hosts[host]["hostid"],
    #                                                   self.hosts[host]["items"][item]["itemid"],
    #                                                   item.replace('"', ''), \
    #                                                   self.hosts[host]["items"][item]["itemkey"].replace('"', ''),
    #                                                   self.hosts[host]["items"][item]["iteminterval"], \
    #                                                   self.hosts[host]["items"][item]["itemunit"],
    #                                                   self.hosts[host]["items"][item]["itemstatus"], \
    #                                                   self.hosts[host]["items"][item]["itemvaluetype"])
    #             cursor.execute(command)
    #     connect.commit()

    def read_from_database(self):
        connect = sqlite3.connect(self.zabbix_db_name)
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM host_detailes')
        self.output_data = cursor.fetchall()
