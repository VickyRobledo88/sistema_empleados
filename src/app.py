from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'empleados'

mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()  # Llama a la función connect()
    cursor = conn.cursor()  # Obtiene el cursor de la conexión

    sql = "SELECT * FROM empleados;"
    cursor.execute(sql)

    empleados = cursor.fetchall()

    return render_template('index.html',empleados=empleados)

    #conn.commit()
    #cursor.close()      
    #conn.close()  
    return render_template('index.html')


@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store',methods=['POST'])
def store():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    sql="INSERT INTO empleados (nombre, correo, foto) VALUES (%s,%s,%s);"

    datos=[_nombre, _correo, _foto.filename]
    conn = mysql.connect()  # Llama a la función connect()
    cursor = conn.cursor()  # Obtiene el cursor de la conexión

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')  

if __name__ == "__main__":
    app.run(debug=True)
