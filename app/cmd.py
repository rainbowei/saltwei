from  flask import  *
import  salt.client
import MySQLdb
app=Flask(__name__)
local=salt.client.LocalClient()
@app.route("/cmd",methods=['POST','GET'])
def cmd():
        if request.method=='GET':
            return render_template('cmd.html')
        if request.method=='POST':
            host=request.form.get('host')
            command=request.form.get('command')
            result = local.cmd(host,'cmd.run',[command])
        return render_template('cmd.html',cont=result)
       


app.run(host='192.168.100.100',port=5000,debug='True')
