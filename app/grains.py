from  flask  import *
import  salt.client
import MySQLdb
app=Flask(__name__)
local=salt.client.LocalClient()
grains= local.cmd('minion-02',['grains.items'],[[],])
def  host_info():
         result= grains['minion-02']['grains.items']
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
sql='select * from sys_info '
cur.execute(sql)
content=cur.fetchall()
def info():
    for line in content:
           result_mysql={
                'ip': line[1],
                'hostname':line[2],
                'os':line[3] , 
                'cpu':line[4] ,  
                'cpu_num':line[5], 
                'mem':line[6]  } 
           return result_mysql    
con.commit()
cur.close()
con.close()

@app.route("/view",methods=['POST','GET'])
def view():
      if request.method=='GET':
               return render_template('index.html')
      if request.method=='POST':
          host= request.form.get('minion')
          result_ip=info()
          if  host==info()['hostname']:
             return render_template('index.html',cont=result_ip)
          else:
             return render_template('index.html',cont=result_ip)


app.run(host='192.168.100.100',port=5000,debug='True')
























