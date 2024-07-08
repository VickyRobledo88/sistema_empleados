import os
from flask import Flask
from flask import render_template,request,redirect, send_from_directory
from flaskext.mysql import MySQL
import datetime

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'empleados'

UPLOADS=os.path.join('src/uploads')
app.config['UPLOADS'] = UPLOADS #guardamos la ruta como un valor de la app

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

# Configurar la ruta para servir archivos estáticos
#@app.route('/src/uploads/<filename>')
#def uploaded_file(filename):
 #   return send_from_directory('src/uploads', filename)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store',methods=['POST'])
def store():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    
   # Suponiendo que _foto es una instancia de werkzeug.datastructures.FileStorage
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Crear el directorio 'uploads' si no existe
    upload_dir = 'src/uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    if _foto.filename != '':
        nuevoNombreFoto= f"{timestamp}_{_foto.filename}"
         # Guardar la foto en el sistema de archivos
        _foto.save(os.path.join(upload_dir, nuevoNombreFoto))

    sql="INSERT INTO empleados (nombre, correo, foto) VALUES (%s,%s,%s);"

    datos=(_nombre, _correo, nuevoNombreFoto)
    conn = mysql.connect()  # Llama a la función connect()
    cursor = conn.cursor()  # Obtiene el cursor de la conexión

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')    

@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "DELETE FROM empleados WHERE id=%s;"
   
    nombreFoto=cursor.fetchone()[0]
    try:
        os.remove(os.path.join(app.config['UPLOADS'],nombreFoto))
    except:
        pass
    cursor.execute(sql, (id,))
    conn.commit()
    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql=f'SELECT * FROM empleados WHERE id="{id}"'
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute(sql)

    empleado=cursor.fetchone()
    return render_template('empleados/edit.html', empleado=empleado)

@app.route('/update',methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
   
    id=request.form['txtId']
    #datos=(_nombre,_correo,id)

    conn=mysql.connect()
    cursor=conn.cursor()
    
    # Suponiendo que _foto es una instancia de werkzeug.datastructures.FileStorage
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Crear el directorio 'uploads' si no existe
    upload_dir = 'src/uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    if _foto.filename != '':
        nuevoNombreFoto= f"{timestamp}_{_foto.filename}"
         # Guardar la foto en el sistema de archivos
        _foto.save(os.path.join(upload_dir, nuevoNombreFoto))

        sql=f'SELECT foto FROM empleados WHERE id="{id}"'
        cursor.execute(sql)
        conn.commit()

        nombreFoto=cursor.fetchone()[0]
        borrarEstaFoto=os.path.join(app.config['UPLOADS'],nombreFoto)

        try:
            os.remove(os.path.join(app.config['UPLOADS'],nombreFoto))
        except:
            pass

        sql=f'UPDATE empleados SET foto="{nuevoNombreFoto}" WHERE id="{id}";'
        
        cursor.execute(sql)
        conn.commit()
    sql=f'UPDATE empleados SET nombre= "{_nombre}", correo="{_correo}" WHERE id="{id}"'
    
   # datos=(_nombre, _correo, nuevoNombreFoto)
    cursor.execute(sql)
  
    #cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')  



if __name__ == "__main__":
    app.run(debug=True)
