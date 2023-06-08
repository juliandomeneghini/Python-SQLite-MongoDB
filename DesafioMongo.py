from pymongo import MongoClient
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///database.db', echo=True)


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String(9), unique=True, nullable=False)
    endereco = Column(String(9), unique=True, nullable=False)

    def __repr__(self):
        return f"Cliente(id={self.id}, nome='{self.nome}', cpf='{self.cpf}', endereco='{self.endereco}')"


class Conta(Base):
    __tablename__ = 'contas'

    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)
    agencia = Column(String, nullable=False)
    num = Column(Integer, unique=True, nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    saldo = Column(DECIMAL, nullable=False)

    cliente = relationship("Cliente", backref="contas")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo='{self.tipo}', agencia='{self.agencia}', num={self.num}, " \
               f"id_cliente={self.id_cliente}, saldo={self.saldo})"


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

cliente1 = Cliente(nome='João', cpf='362689455', endereco='Rua Tiradentes')
cliente2 = Cliente(nome='José', cpf='392355500', endereco='Rua Oswald Aranha')

conta1 = Conta(tipo='Tipo 1', agencia='Agencia 1', num=1, id_cliente=1, saldo=1000.0)
conta2 = Conta(tipo='Tipo 2', agencia='Agencia 2', num=2, id_cliente=2, saldo=2000.0)

session.add_all([cliente1, cliente2, conta1, conta2])
session.commit()

clientes = session.query(Cliente).all()
for cliente in clientes:
    print(cliente)

# Conectando ao MongoDB Atlas
client = MongoClient('mongodb+srv://juliandomeneghini:yHKT5BRQGj9BU2cU@cluster0.kxtnyi0.mongodb.net/?retryWrites=true'
                     '&w=majority')
database = client['mydatabase']

collection = database['bank']

cliente1 = {
    'id': 1,
    'nome': 'João',
    'cpf': '362689455',
    'endereco': 'Rua Tiradentes',
    'contas': [
        {
            'id': 1,
            'tipo': 'Tipo 1',
            'agencia': 'Agencia 1',
            'num': 1,
            'saldo': 1000.0
        }
    ]
}

cliente2 = {
    'id': 2,
    'nome': 'José',
    'cpf': '392355500',
    'endereco': 'Rua Oswald Aranha',
    'contas': [
        {
            'id': 2,
            'tipo': 'Tipo 2',
            'agencia': 'Agencia 2',
            'num': 2,
            'saldo': 2000.0
        }
    ]
}

collection.insert_many([cliente1, cliente2])

# Recuperando informações de um cliente com base no CPF
cliente = collection.find_one({'cpf': '123456789'})
print(cliente)

# Recuperando informações de todas as contas
contas = collection.find({}, {'contas': 1})
for cliente in contas:
    for conta in cliente['contas']:
        print(conta)
