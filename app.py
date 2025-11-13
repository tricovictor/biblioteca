from flask import Flask, render_template, request, redirect, url_for, flash
#from flask_mysqldb import MySQL #pip install flask-mysqldb
import pymysql

app = Flask(__name__)

DB_HOST = 'localhost'
DB_USER = 'admin'
DB_PASS = '5@L4QVrtUUMIHzP'
#2DOems
DB_NAME = 'biblioteca'
app.secret_key = 'mysecretkey'

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def Index():
    return render_template('home.html')

@app.route('/users')
def Indexusers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    conn.close()
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
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO contacts (fullname, email, phone) VALUES (%s, %s ,%s)', (fullname, email, phone))
        conn.commit()
        flash('Contacto agregado correctamente')
        return redirect(url_for('Index'))

@app.route('/users/edit/<id>')
def edit_contact(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s',(id))
    data = cur.fetchall()
    return render_template('users/edit-user.html', contact = data[0])

@app.route('/users/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s 
            WHERE id = %s
        """,(fullname, email, phone, id))
        conn.commit()
        flash('Contacto actualizado')
        return redirect(url_for('Indexusers'))

@app.route('/users/delete/<string:id>')
def delete_contact(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}' .format(id))
    conn.commit()
    flash('Contacto eliminado')
    return redirect(url_for('Index'))

@app.route("/users/search", methods=["GET"])
def search_user():
    fullname = request.args.get("fullname", "").strip().lower()
    conn = get_db_connection()
    cur = conn.cursor()
    consulta = """SELECT * FROM contacts WHERE LOWER(fullname) LIKE %s"""
    patron = f"%{fullname}%"
    cur.execute(consulta, (patron,))
    data = cur.fetchall()
    return render_template("users/index.html", users= data)


#Aca empiezan los books


@app.route('/books')
def Indexbooks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT libros.* , categories.name AS categoria
        FROM libros
        JOIN categories ON libros.categoria_id = categories.id
    """)
    data = cur.fetchall()
    return render_template('books/index.html', books = data)

@app.route('/book/add-book')
def add_book_view():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM categories')
    categories = cur.fetchall()
    return render_template('books/add-book.html', categories = categories)

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
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO libros (nombre, autor, editorial, genero, idioma, codigoISN, categoria, ubicacion) VALUES (%s, %s ,%s, %s, %s ,%s, %s, %s)', (nombre, autor, editorial, genero, idioma, codigoISN, categoria, ubicacion))
        conn.commit()
        flash('Libro agregado correctamente')
        return redirect(url_for('Indexbooks'))

@app.route('/book/edit/<id>')
def edit_book(id):
    conn = get_db_connection()
    cur = conn.cursor()
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
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE libros
            SET nombre = %s,
                autor = %s,
                editorial = %s, 
                genero = %s, 
                idioma = %s, 
                codigoISN = %s, 
                categoria = %s, 
                ubicacion = %s 
            WHERE id = %s
        """,(nombre,autor,editorial,genero,idioma,codigoISN,categoria,ubicacion, id))
        conn.commit()
        flash('Libro actualizado')
        return redirect(url_for('Index'))

@app.route("/book/search", methods=["GET"])
def search_book():
    nombre = request.args.get("titulo", "").strip().lower()
    conn = get_db_connection()
    cur = conn.cursor()
    consulta = """SELECT * FROM libros WHERE LOWER(nombre) LIKE %s"""
    patron = f"%{nombre}%"
    cur.execute(consulta, (patron,))
    data = cur.fetchall()
    return render_template("books/index.html", books= data)

#Aqui empiezan los estudiantes

@app.route('/students')
def Indexstudents():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    data = cur.fetchall()
    return render_template('students/index.html', students = data)

@app.route("/student/search", methods=["GET"])
def search_student():
    nombre = request.args.get("lastname", "").strip().lower()
    conn = get_db_connection()
    cur = conn.cursor()
    consulta = """SELECT * FROM students WHERE LOWER(name) LIKE %s OR LOWER(lastname) LIKE %s"""
    patron = f"%{nombre}%"
    cur.execute(consulta, (patron,patron,))
    data = cur.fetchall()
    return render_template("students/index.html", students= data)


@app.route('/student/add-student')
def add_student_view():
    return render_template('students/add-student.html')

@app.route('/student/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        document = request.form['document']
        email = request.form['email']
        phone = request.form['phone']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO students (name, lastname, document, email, phone) VALUES (%s, %s ,%s, %s, %s )', (name, lastname, document, email, phone))
        conn.commit()
        flash('Estudiante agregado correctamente')
        return redirect(url_for('Indexstudents'))

@app.route('/student/edit/<id>')
def edit_student(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students WHERE id = %s',(id))
    data = cur.fetchall()
    return render_template('students/edit-student.html', student = data[0])

@app.route('/student/update/<id>', methods = ['POST'])
def update_student(id):
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        document = request.form['document']
        email = request.form['email']
        phone = request.form['phone']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE students
            SET name = %s,
                lastname = %s,
                document = %s, 
                email = %s,
                phone = %s 
            WHERE id = %s
        """,(name,lastname,document,email,phone, id))
        conn.commit()
        flash('Estudiante actualizado')
        return redirect(url_for('Indexstudents'))

#Aqui comienzan las categorias

@app.route('/categories')
def Indexcategories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM categories')
    data = cur.fetchall()
    return render_template('categories/index.html', categories = data)

@app.route('/categories/add-category')
def add_category_view():
    return render_template('categories/add-category.html')

@app.route('/categories/add_category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        nombre = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO categories (name) VALUES (%s)', (nombre,))
        conn.commit()
        flash('Categoria agregada correctamente')
        return redirect(url_for('Indexcategories'))

@app.route('/categories/edit/<id>')
def edit_category(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM categories WHERE id = %s',(id))
    data = cur.fetchall()
    return render_template('categories/edit.html', category = data[0])

@app.route('/categories/update/<id>', methods = ['POST'])
def update_category(id):
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE categories
            SET name = %s
            WHERE id = %s
        """,(name, id))
        conn.commit()
        flash('Categoria actualizada')
        return redirect(url_for('Indexcategories'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)