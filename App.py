from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL #pip install flask-mysqldb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '5@L4QVrtUUMIHzP'
app.config['MYSQL_DB'] = 'biblioteca'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return render_template('home.html')

@app.route('/users')
def Indexusers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('users/index.html', users = data)

@app.route('/users/add-user')
def add_user_view():
    return render_template('users/add-user.html')

@app.route('/users/add_user', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, email, phone) VALUES (%s, %s ,%s)', (fullname, email, phone))
        mysql.connection.commit()
        flash('Contacto agregado correctamente')
        return redirect(url_for('Index'))

@app.route('/users/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s',(id))
    data = cur.fetchall()
    return render_template('users/edit-user.html', contact = data[0])

@app.route('/users/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s 
            WHERE id = %s
        """,(fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contacto actualizado')
        return redirect(url_for('Index'))

@app.route('/users/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}' .format(id))
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('Index'))

#Aca empiezan los books


@app.route('/books')
def Indexbooks():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libros')
    data = cur.fetchall()
    return render_template('books/index.html', books = data)

@app.route('/book/add-book')
def add_book_view():
    return render_template('books/add-book.html')


@app.route('/book/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        nombre = request.form['nombre']
        autor = request.form['autor']
        editorial = request.form['editorial']
        genero = request.form['genero']
        idioma = request.form['idioma']
        codigoISN = request.form['codigoISN']
        categoria = request.form['categoria']
        ubicacion = request.form['ubicacion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO libros (nombre, autor, editorial, genero, idioma, codigoISN, categoria, ubicacion) VALUES (%s, %s ,%s, %s, %s ,%s, %s, %s)', (nombre, autor, editorial, genero, idioma, codigoISN, categoria, ubicacion))
        mysql.connection.commit()
        flash('Libro agregado correctamente')
        return redirect(url_for('Indexbooks'))

@app.route('/book/edit/<id>')
def edit_book(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libros WHERE id = %s',(id))
    data = cur.fetchall()
    return render_template('books/edit.html', book = data[0])

@app.route('/book/update/<id>', methods = ['POST'])
def update_book(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        autor = request.form['autor']
        editorial = request.form['editorial']
        genero = request.form['genero']
        idioma = request.form['idioma']
        codigoISN = request.form['codigoISN']
        categoria = request.form['categoria']
        ubicacion = request.form['ubicacion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE libros
            SET nombre = %s,
                autor = %s,
                editorial = %s 
                genero = %s 
                idioma = %s 
                codigoISN = %s 
                categoria = %s 
                ubicacion = %s 
            WHERE id = %s
        """,(nombre,autor,editorial,genero,idioma,codigoISN,categoria,ubicacion, id))
        mysql.connection.commit()
        flash('Libro actualizado')
        return redirect(url_for('Index'))

@app.route("/book/search", methods=["GET"])
def search_book():
    nombre = request.args.get("titulo", "").strip().lower()
    cur = mysql.connection.cursor()
    #Aca no anda la busqueda
    consulta = """SELECT * FROM libros WHERE LOWER(nombre) LIKE %s"""
    patron = f"%{nombre}%"
    cur.execute(consulta, (patron,))
    data = cur.fetchall()
    return render_template("books/index.html", books= data)

#Aqui empiezan los estudiantes
@app.route('/students')
def Indexstudents():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')
    data = cur.fetchall()
    return render_template('students/index.html', students = data)









if __name__ == '__main__':
    app.run(port = 3000, debug = True)