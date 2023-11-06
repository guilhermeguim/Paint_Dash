from flask import Flask, render_template, jsonify, request, url_for, send_file, redirect
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import sqlite3
import os
import plotly.graph_objects as go
import pandas as pd
import json

from datetime import datetime
from manager import db_manager
from get_functions import get_path,get_curr_path
from get_graphs import get_graph

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('TYT85F46S_442D')
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

socketio = SocketIO(app)

class User(UserMixin):
    def __init__(self, id, hmc, password):
        self.id = id
        self.username = hmc
        self.password = password

    @staticmethod
    def get(user_id):
        user_record = db_manager.query_user_by_id(user_id)
        if user_record:
            return User(user_record[0], user_record[1], user_record[2])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    return render_template("login.html",error=0)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hmc = request.form['hmc']
        password = request.form['password']
        user_record = db_manager.query_user_by_hmc(hmc)

        if user_record and bcrypt.check_password_hash(user_record[2], password):
            user = User(user_record[0], user_record[1], user_record[2])
            login_user(user)
            return redirect(url_for('externo'))
        else:
            if user_record == None:
                error_type = 1
            else:
                error_type = 2
            return render_template('login.html',error=error_type)
    return render_template('login.html')

@app.route("/rst")
def rst():
    return render_template("rst.html",error=0)

@app.route("/rst_user", methods=['GET', 'POST'])
def rst_user():
    if request.method == 'POST':
        hmc = request.form['hmc']
        master_key = request.form['master']
        
        user_record = db_manager.query_user_by_hmc(hmc)

        if not user_record:
            #hmc not exists
            return render_template("rst.html", error=1)
        elif master_key != os.getenv('D8HS7T_232'):
            return render_template("rst.html", error=2)
        
        else:
            password = bcrypt.generate_password_hash('HMC1234').decode('utf-8')
            dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_manager.rst_pwd_operator(hmc,dt_string,password)

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html',error=0)

@app.route("/register")
def register():
    return render_template("register.html", error=0)

@app.route("/register_user", methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        print('entrei')
        hmc = request.form['hmc']
        password = request.form['password']
        name = request.form['name']
        confirm_password2 = request.form['confirm_password']
        master_key = request.form['master']

        user_record = db_manager.query_user_by_hmc(hmc)

        if user_record:
            #hmc exists
            return render_template("register.html", error=1)
        elif password == '':
            return render_template("register.html", error=2)
        elif password != confirm_password2:
            return render_template("register.html", error=3)
        elif master_key != os.getenv('D8HS7T_232'):
            return render_template("register.html", error=4)
        else:
            password = bcrypt.generate_password_hash(os.getenv('82DAaf9525Far')).decode('utf-8')
            dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_manager.add_operator(hmc,dt_string,name,password)
            
            return render_template('login.html',error=0)

    return render_template('login.html',error=0)

@app.route("/externo")
@login_required
def externo():
    test_connect()
    return render_template("externo.html")

@app.route("/interno")
@login_required
def interno():
    return render_template("interno.html")

@app.route("/dashboard")
@login_required
def dashboard():
    
    size = 1
    # Vamos criar um exemplo de DataFrame para demonstração
    df = db_manager.get_graph_data()
    # Converta a coluna DATE_TIME para o tipo datetime
    fig1, total_events_today, shift1, shift2, shift3, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9 = get_graph(df,size)

    graph_json1 = fig1.to_json()
    graph_json2 = fig2.to_json()
    graph_json3 = fig3.to_json()
    graph_json4 = fig4.to_json()
    graph_json5 = fig5.to_json()
    graph_json6 = fig6.to_json()
    graph_json7 = fig7.to_json()
    graph_json8 = fig8.to_json()
    graph_json9 = fig9.to_json()
    
    # Renderize o gráfico usando a função render_template
    return render_template('dashboard.html', 
                           graph_json1=graph_json1,
                           total_events_today=total_events_today, 
                           shift1=shift1, 
                           shift2=shift2, 
                           shift3=shift3,
                           graph_json2=graph_json2,
                           graph_json3=graph_json3,
                           graph_json4=graph_json4,
                           graph_json5=graph_json5,
                           graph_json6=graph_json6,
                           graph_json7=graph_json7,
                           graph_json8=graph_json8,
                           graph_json9=graph_json9,
                           )

@app.route("/update_dash", methods=['GET'])
@login_required
def update_dash():
    size = int(request.args.get('screenSize'))
    # Vamos criar um exemplo de DataFrame para demonstração
    df = db_manager.get_graph_data()
    # Converta a coluna DATE_TIME para o tipo datetime
    fig1, total_events_today, shift1, shift2, shift3, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9 = get_graph(df,size)

    graph_json1 = fig1.to_json()
    graph_json2 = fig2.to_json()
    graph_json3 = fig3.to_json()
    graph_json4 = fig4.to_json()
    graph_json5 = fig5.to_json()
    graph_json6 = fig6.to_json()
    graph_json7 = fig7.to_json()
    graph_json8 = fig8.to_json()
    graph_json9 = fig9.to_json()
    
    # Criar um dicionário com todas as variáveis
    response_data = {
        "graph_json1": graph_json1,
        "graph_json2": graph_json2,
        "graph_json3": graph_json3,
        "graph_json4": graph_json4,
        "graph_json5": graph_json5,
        "graph_json6": graph_json6,
        "graph_json7": graph_json7,
        "graph_json8": graph_json8,
        "graph_json9": graph_json9,
        "total_events_today": total_events_today,
        "shift1": shift1,
        "shift2": shift2,
        "shift3": shift3
    }

    # Passando o dicionário para o jsonify do Flask
    return jsonify(response_data)

@app.route("/ext_map")
@login_required
def ext_map():
    return render_template('ext_map.html')

@app.route("/int_map")
@login_required
def int_map():
    return render_template('int_map.html')

@app.route("/heatmap", methods=['GET'])
@login_required
def heatmap():
    local_type = request.args.get('namePage')
    time = request.args.get('filterTime')
    df, max_value = db_manager.calculate_sums(local_type, time)
    
    # Convertendo o DataFrame para JSON usando o método 'to_json' do pandas
    json_data = df.to_json(orient='records')

    # Criando um dicionário para armazenar o JSON e o valor de 'max'
    response_data = {
        'data': json_data,
        'max_value': max_value
    }

    # Passando o dicionário para o jsonify do Flask
    return jsonify(response_data)

@app.route("/profile")
@login_required
def profile():
    data = db_manager.get_all_data_from_user(current_user.username)
    return render_template("profile.html",data=data)

@app.route("/edit_profile")
@login_required
def edit_profile():
    data = db_manager.get_all_data_from_user(current_user.username)
    return render_template("edit_profile.html",data=data)

@app.route("/edit_route", methods=['POST'])
@login_required
def edit_route():
    old_hmc = current_user.username
    if request.method == 'POST':
        hmc = request.form['hmc']
        name = request.form['name']
        dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db_manager.edit_operator(hmc, name, dt_string, old_hmc)
        
        return redirect(url_for('logout'))

@app.route("/edit_pwd")
@login_required
def edit_pwd():
    return render_template("edit_pwd.html",error=0)

@app.route("/edit_pwd_route", methods=['POST'])
@login_required
def edit_pwd_route():
    if request.method == 'POST':
        old_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_new_password']
        user_record = db_manager.query_user_by_hmc(current_user.username)
        
        if new_password != confirm_password:
            return render_template("edit_pwd.html",error=1)
        elif bcrypt.check_password_hash(user_record[2], old_password):
            hmc = current_user.username
            password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_manager.rst_pwd_operator(hmc,dt_string,password)
            return redirect(url_for('logout'))
        else:
            return render_template("edit_pwd.html",error=2)

@app.route("/history")
@login_required
def history():
    # Render the template with the rows
    data = db_manager.get_history('all','all','all','all','all')
    dates = db_manager.get_dates()
    return render_template("history.html", data=data, dates=dates)

@app.route('/input_data', methods=['POST'])
@login_required
def input_data():
    local_type = request.form.get('type')  # Obter o tipo de erro enviado pelo AJAX
    side = request.form.get('side')
    location = request.form.get('location')
    region = request.form.get('region')
    code = request.form.get('vinCode')
    operator = current_user.username
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = [local_type,side,location,region,code,dt_string,operator]
    db_manager.input_data(data)
    
    # Envia um sinal para atualizar a tabela nos clientes conectados
    socketio.emit('update_table', {'update': '1'})
    return 'Added'

@app.route('/delete_data', methods=['POST'])
@login_required
def delete_data():
    id_get = request.form.get('id')  # Obter o tipo de erro enviado pelo AJAX
    hmc = current_user.username
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db_manager.delete_data(id_get,dt_string,hmc)
    
    # Envia um sinal para atualizar a tabela nos clientes conectados
    socketio.emit('update_table', {'update': '1'})
    return 'Deleted'

# Rota para obter os dados atualizados da tabela
@app.route('/update_data', methods=['GET'])
@login_required
def update_data():
    
    d_type = request.args.get('filterType')
    side = request.args.get('filterSide')
    location = request.args.get('filterLocation')
    region = request.args.get('filterRegion')
    date = request.args.get('filterDate')
    # Use o método get_history(filter) do objeto db_manager para obter os dados atualizados
    data = db_manager.get_history(d_type, side, location, region, date)  # Substitua 'filter' pelo filtro adequado

    # Converta os dados para o formato JSON e retorne como resposta
    return jsonify({'data': data})

@app.route('/download', methods=['GET'])
@login_required
def download_file():
    # Caminho absoluto para o arquivo que você deseja fazer o download
    file_path = get_curr_path() + '/history.xlsx'
    db_manager.export_excel(file_path)
    # Verifique se o arquivo existe
    if os.path.exists(file_path):
        # Faça o download do arquivo
        return send_file(file_path, as_attachment=True)
    else:
        # Caso o arquivo não exista, retorne uma mensagem de erro
        return "Arquivo não encontrado"


@socketio.on('connect')
def test_connect():
    print("socket connected")

if __name__ == "__main__":
    db_path = get_path()
    db_manager = db_manager(db_path)

    socketio.run(app, host="0.0.0.0")
    

###HELPFULL
#https://stackoverflow.com/questions/18600031/changing-the-active-class-of-a-link-with-the-twitter-bootstrap-css-in-python-fla