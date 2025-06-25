# Importa as classes necessárias do SQLAlchemy para criar a estrutura do banco de dados
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Cria a conexão com o banco de dados SQLite chamado "banco.db"
db = create_engine("sqlite:///banco.db")

# Cria a base para declarar as classes do banco de dados (modelo ORM)
Base = declarative_base()

# ===============================
# MODELO DA TABELA DE USUÁRIOS
# ===============================
class Usuario(Base):
    __tablename__ = "usuarios" # Nome da tabela no banco

    # Colunas da tabela
    id = Column("id", Integer, primary_key=True, autoincrement=True)  # ID auto incremental (chave primária)
    nome = Column("nome", String)  # Nome do usuário
    email = Column("email", String, nullable=False)  # Email do usuário (obrigatório)
    senha = Column("senha", String)  # Senha criptografada
    ativo = Column("ativo", Boolean)  # Indica se o usuário está ativo
    admin = Column("admin", Boolean, default=False)  # Se é um usuário administrador (padrão: não)

    # Construtor da classe
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# ===============================
# MODELO DA TABELA DE PEDIDOS
# ===============================
class Pedido(Base):
    __tablename__ = "pedidos" # Nome da tabela no banco

    # STATUS_PEDIDOS = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)  # ID do pedido
    status = Column("status", String)  # Status do pedido (ex: PENDENTE, FINALIZADO)
    usuario = Column("usuario", ForeignKey("usuarios.id"))  # Chave estrangeira referenciando o ID do usuário
    preco = Column("preco", Float)  # Preço total do pedido
    itens = relationship("ItemPedido", cascade="all, delete")  # Relacionamento com os itens do pedido

    # Construtor da classe
    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

    # Método que calcula o preço total do pedido com base nos itens
    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


# ===========================================
# MODELO DA TABELA DE ITENS DO PEDIDO
# ===========================================
class ItemPedido(Base):
    __tablename__ = "itens_pedido" # Nome da tabela no banco

    id = Column("id", Integer, primary_key=True, autoincrement=True)  # ID do item
    quantidade = Column("quantidade", Integer)  # Quantidade do item
    sabor = Column("sabor", String)  # Sabor do item (ex: pizza de calabresa, etc.)
    tamanho = Column("tamanho", String)  # Tamanho do item (ex: pequeno, médio, grande)
    preco_unitario = Column("preco_unitario", Float)  # Preço de uma unidade
    pedido = Column("pedido", ForeignKey("pedidos.id"))  # Chave estrangeira referenciando o pedido

    # Construtor da classe
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

# Executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)

# Migrar o banco de dados

# Criar a migração: alembic revision --autogenerate -m "mensagem"
# Executar a migração: alembic upgrade head