from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Salas, Reservas, db
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'  # Necessário para flash messages e sessão
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_dados.db'  # Caminho do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # Serve para manter o app e o db "CONECTADOS"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/salas')
def listar_salas():
    salas = Salas.query.all()
    return render_template('salas.html', salas=salas)


@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    if request.method == 'POST':

        data_str = request.form['data_reserva']  # por exemplo: '2025-08-12'
        data_reserva_formatada = datetime.strptime(data_str, "%Y-%m-%d").date()


        # Convertendo a hora inicial e final do template para algo aceitavel ao banco de dados
        hora_inicial_str = request.form.get('hora_inicial')  # "19:50"
        hora_final_str = request.form.get('hora_final')      # "20:10"

        hora_inicial_formatadada = datetime.strptime(hora_inicial_str, "%H:%M").time()
        hora_final_formatadada = datetime.strptime(hora_final_str, "%H:%M").time()
        
        nova_reserva = Reservas(
            nome_responsavel=request.form['nome_responsavel'],
            nome_grupo=request.form['nome_grupo'],
            tel1=request.form['tel1'],
            sala_desejada=request.form['sala_desejada'], 
            data_reserva=data_reserva_formatada,
            hora_inicial=hora_inicial_formatadada,
            hora_final=hora_final_formatadada,
            observacao=request.form['observacao'],
            status_fixo='Pendente'
        )
        db.session.add(nova_reserva)
        db.session.commit()
        flash("Reserva solicitada! Aguarde confirmação.")
        return redirect(url_for('listar_reservas'))

    salas = Salas.query.all()
    return render_template('reservar.html', salas=salas)



@app.route('/reservas/<int:id_reserva>/status/<string:novo_status>', methods=['POST'])
def alterar_status_reserva(id_reserva, novo_status):
    reserva = Reservas.query.get_or_404(id_reserva)
    reserva.status_fixo = novo_status.capitalize()
    db.session.commit()
    flash(f"Reserva {novo_status} com sucesso.")
    return redirect(url_for('listar_reservas'))



@app.route('/reservas')
def listar_reservas():
    status = request.args.get('status', None)
    if status:
        reservas = Reservas.query.filter_by(status_fixo=status.capitalize()).all()
    else:
        reservas = Reservas.query.all()
    return render_template('reservas.html', reservas=reservas)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no SQLite se não existirem
    app.run(debug=True)
