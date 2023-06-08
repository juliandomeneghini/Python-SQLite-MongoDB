from sqlalchemy import Column, create_engine, inspect, ForeignKey, Integer, select, String, func, DECIMAL
from sqlalchemy.orm import declarative_base, relationship, Session

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


print(Cliente.__tablename__)

# conexão com o banco de dados
engine = create_engine('sqlite:///database.db', echo=True)

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# investiga o esquema de banco de dados
inspector = inspect(engine)
print(inspector.get_table_names())
print(inspector.default_schema_name)

with Session(engine) as session:
    julian = Cliente(
        nome='julian',
        cpf='362689450',
        endereco='Rua Tiradentes'
    )

    Janaina = Cliente(
        nome='janaina',
        cpf='567890987',
        endereco='Rua Oswald Aranha'
    )

    Pietro = Cliente(
        nome='pietro',
        cpf='874567890',
        endereco='Rua Noes'
    )

    # enviando para o BD (persistência de dados)
    session.add_all([julian, Janaina, Pietro])
    session.commit()

    stmt = select(Cliente).where(Cliente.nome.in_(['julian', 'sandy']))
    print('Recuperando clientes a partir de condição de filtragem')
    for cliente in session.scalars(stmt):
        print(cliente)

    stmt_address = select(Cliente).where(Cliente.id == 2)
    print('\nRecuperando o cliente com ID igual a 2')
    cliente = session.scalars(stmt_address).one()
    print(cliente)

    stmt_order = select(Cliente).order_by(Cliente.nome.desc())
    print('\n')
    for result in session.scalars(stmt_order):
        print(result)

    stmt_join = select(Cliente.nome, Conta.saldo).join_from(Conta, Cliente)
    print('\n')
    for result in session.scalars(stmt_join):
        print(result)

    connection = engine.connect()
    results = connection.execute(stmt_join).fetchall()
    print('\nExecutando statement a partir da connection')
    for result in results:
        print(result)

    stmt_count = select(func.count('*')).select_from(Cliente)
    print('Total de instâncias em Cliente')
    for result in session.scalars(stmt_count):
        print(result)
