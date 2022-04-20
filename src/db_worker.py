import sqlite3

class DataBaseLoader(object):
    def __init__(self):
        self.zabbix_db_name = self.zabbix_ip.split('.')[2] + '_' + self.zabbix_ip.split('.')[3]
        self.dbname = "log/output_{}db.sqlite".format(self.zabbix_db_name)

    def insert_json_to_database(self):
        
        connect = sqlite3.connect(self.dbname)
        cursor = connect.cursor()
        try:
            if self.zabbix_type == "ref":
                cursor.execute('CREATE TABLE hosts_name (hostname VARCHAR, hostid VARCHAR, stat VARCHAR)')
            elif self.zabbix_type == "cpy":
                cursor.execute('CREATE TABLE hosts_name (hostname VARCHAR, hostid VARCHAR)')
            else:
                pass
            if self.zabbix_type == "ref":
                cursor.execute('CREATE TABLE host_detailes (hostid VARCHAR, itemid VARCHAR, itemname VARCHAR, itemkey VARCHAR, iteminterval VARCHAR, \
                    itemunit VARCHAR, itemstatus VARCHAR, itemvaluetype VARCHAR, stat VARCHAR)')
            elif self.zabbix_type == "cpy":
                cursor.execute('CREATE TABLE host_detailes (hostid VARCHAR, itemid VARCHAR, itemname VARCHAR, itemkey VARCHAR, iteminterval VARCHAR, \
                    itemunit VARCHAR, itemstatus VARCHAR, itemvaluetype VARCHAR)')
            else:
                pass

        except:
            pass
        for host in self.hosts:
            command = 'INSERT INTO hosts_name (hostname, hostid) SELECT "{0}", "{1}" WHERE NOT EXISTS(SELECT 1 FROM hosts_name WHERE hostname = \
                "{0}" AND hostid =  "{1}")'.format(host, self.hosts[host]["hostid"])
            cursor.execute(command)
            for item in self.hosts[host]["items"]:
                # print(item)
                item.replace('"', '')
                if self.zabbix_type == "ref":
                    command = 'INSERT INTO host_detailes (hostid, itemid, itemname, itemkey, iteminterval, itemunit, itemstatus, itemvaluetype, stat) SELECT \
                        "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}" , "{8}" WHERE NOT EXISTS(SELECT 1 FROM host_detailes WHERE hostid =  "{0}" AND \
                            itemname = "{2}")'.format(self.hosts[host]["hostid"], self.hosts[host]["items"][item]["itemid"], item.replace('"', ''), \
                                self.hosts[host]["items"][item]["itemkey"].replace('"', ''), self.hosts[host]["items"][item]["iteminterval"], \
                                    self.hosts[host]["items"][item]["itemunit"], self.hosts[host]["items"][item]["itemstatus"], \
                                        self.hosts[host]["items"][item]["itemvaluetype"], self.hosts[host]["items"][item]["stat"])
                else:
                    command = 'INSERT INTO host_detailes (hostid, itemid, itemname, itemkey, iteminterval, itemunit, itemstatus, itemvaluetype) SELECT \
                        "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}"  WHERE NOT EXISTS(SELECT 1 FROM host_detailes WHERE hostid =  "{0}" AND \
                            itemname = "{2}")'.format(self.hosts[host]["hostid"], self.hosts[host]["items"][item]["itemid"], item.replace('"', ''), \
                                self.hosts[host]["items"][item]["itemkey"].replace('"', ''), self.hosts[host]["items"][item]["iteminterval"], \
                                    self.hosts[host]["items"][item]["itemunit"], self.hosts[host]["items"][item]["itemstatus"], \
                                        self.hosts[host]["items"][item]["itemvaluetype"])
                cursor.execute(command)
        connect.commit()

    def read_from_database(self):
        connect = sqlite3.connect(self.dbname)
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM host_detailes')
        data = cursor.fetchall()
        print(data)