import os
import salt.client
import salt.config
import salt.key
import sys
from  flask import  *
app=Flask(__name__)
local=salt.client.LocalClient()
def push_file(target,file_path):
   local=salt.client.LocalClient()
   cmd=local.cmd(target,'cp.push',[file_path])
   return cmd

def  minion_list():
     opt=salt.config.client_config('/etc/salt/master')
     manger=salt.key.Key(opt).list_keys()
     manger=manger['minions']
     return manger
@app.route("/down",methods=['POST','GET'])
def download():
      if request.method=='GET':
            return render_template('down.html')
      if request.method=='POST':
            target=request.form.get('phost')
            file_path=request.form.get('pfile')
            output=push_file(target,file_path)
      if target not in minion_list() or not  os.path.exists(file_path) :
             print  "target: %s is not in minions or %s file_path:is not exists"%(target,file_path)
      else:
             output 
             return render_template('down.html')
       
         
app.run(host='192.168.100.100',port=5000,debug='True')











