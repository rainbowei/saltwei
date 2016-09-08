from  flask  import *
import  salt.client
import MySQLdb
app=Flask(__name__)
local=salt.client.LocalClient()
grains= local.cmd('minion-01',['grains.items'],[[],])
def  host_info():
         result= grains['minion-01']['grains.items']
         os=result['os']
         osrelease=result['osrelease']
         osarch=result['osarch']
         os_version='%s-%s,%s'%(os,osrelease,osarch)
         status={
                    'get_hostname':result['host'],
                    'get_network_interfaces': result['ip_interfaces']['eth0'][0],
                    'get_mem_total':result['mem_total'],
                    'get_cpu_model':result['cpu_model'],
                    'get_num_cpus':result['num_cpus'],
                    'get_os_version':os_version
                     }
         return status        
hostname=host_info()['get_hostname']
network_interfaces=host_info()['get_network_interfaces']
mem_total=host_info()['get_mem_total']
cpu_model=host_info()['get_cpu_model']
num_cpus=host_info()['get_num_cpus']
os_version=host_info()['get_os_version']


con=MySQLdb.connect(host='192.168.100.100',user='root',passwd='',db='monitor')
cur=con.cursor()
sql="insert into sys_info(network_interfaces,hostname,os_version,cpu_model,num_cpus,mem_total) values('%s','%s','%s','%s','%s','%s')"%(network_interfaces,hostname,os_version,cpu_model,num_cpus,mem_total)
cur.execute(sql)
con.commit()
cur.close()
con.close()
































