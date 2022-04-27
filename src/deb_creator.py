import os
import shutil
import subprocess

project_name = "zabbix-copyer"
py_project_addr = "zabbix_copyer"

root = os.getcwd()
# print(root.split("\\")[0:-2])
roo = ''
for i, add in enumerate(root.split("\\")[0:-2]):
    if i > 0:
        roo = roo + "/{}".format(add)
    else:
        roo = roo + add
print(roo)
deb_dir = "{}/{}/opt/".format(roo, project_name)
py_dir = "{}/{}/".format(roo, py_project_addr)

os.makedirs(deb_dir, exist_ok=True)

for i in ["src", "config", "bin"]:
    shutil.copytree(py_dir + i, deb_dir + i, dirs_exist_ok=True)
shutil.rmtree(deb_dir + "src/__pycache__", ignore_errors=True)
shutil.copy(py_dir + "main.py", deb_dir)
os.makedirs(deb_dir + "log", exist_ok=True)
os.makedirs(deb_dir + "dbs", exist_ok=True)
os.makedirs(deb_dir + "../DEBIAN", exist_ok=True)
if not os.path.isfile(deb_dir + "../DEBIAN/control"):
    shutil.move(deb_dir + "config/control", deb_dir + "../DEBIAN/")

