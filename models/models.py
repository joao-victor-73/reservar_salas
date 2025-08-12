from . import db


class Salas(db.Model):
    __tablename__ = 'salas'
    id_sala = db.Column(db.Integer, primary_key=True)
    nome_sala = db.Column(db.String(100), nullable=False)
    cap_pessoas = db.Column(db.Integer, nullable=True)
    status_disp = db.Column(db.String(50), nullable=True)

    reservas = db.relationship('Reservas', backref='sala', lazy=True)


class Reservas(db.Model):
    __tablename__ = 'reservas'
    id_reserva = db.Column(db.Integer, primary_key=True)
    nome_responsavel = db.Column(db.String(100), nullable=False)
    nome_grupo = db.Column(db.String(100), nullable=False)
    tel1 = db.Column(db.String(20), nullable=False)
    data_reserva = db.Column(db.Date, nullable=False)
    hora_inicial = db.Column(db.Time, nullable=False)
    hora_final = db.Column(db.Time, nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    status_fixo = db.Column(db.String(20), nullable=False, default='Pendente')

    # Foreign Key (Relacionamento: salas (1) - reservas (N) )
    sala_desejada = db.Column(db.Integer, db.ForeignKey(
        'salas.id_sala'), nullable=False)
