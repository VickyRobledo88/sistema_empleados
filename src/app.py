from flask import Flask
from flask import render_template
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
    sql = "INSERT INTO empleados (nombre, correo, foto) VALUES('Juan', 'juan@email.com', 'fotodejuan.jpg');"
    conn = mysql.connect()  # Llama a la función connect()
    cursor = conn.cursor()  # Obtiene el cursor de la conexión
    cursor.execute(sql)  
    conn.commit()
    cursor.close()  # Cierra el cursor
    conn.close()  # Cierra la conexión
    return render_template('empleados/index.html')

if __name__ == "__main__":
    app.run(debug=True)
