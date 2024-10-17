from flask import render_template, request, redirect, session, url_for

class AuthController:

    @staticmethod
    def login():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']  # Validar contraseña aquí
            session['username'] = username
            session['email'] = email
            return redirect(url_for('usuario'))
        return render_template('login.html')

    @staticmethod
    def registro():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']  # Validar contraseña aquí
            session['username'] = username
            session['email'] = email
            return redirect(url_for('login'))
        return render_template('registro.html')
