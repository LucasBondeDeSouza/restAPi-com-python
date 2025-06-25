from fastapi import FastAPI # Importa a classe FastAPI para criar a aplicação web
from passlib.context import CryptContext # Importa o gerenciador de contexto de criptografia de senhas (aqui será usado o bcrypt)
from fastapi.security import OAuth2PasswordBearer # Importa o esquema OAuth2 para autenticação com tokens (Bearer Token)
from dotenv import load_dotenv # Importa o dotenv para carregar variáveis de ambiente de um arquivo .env
import os # Importa a biblioteca os para acessar variáveis de ambiente do sistema

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Lê as variáveis de ambiente necessárias para autenticação
SECRET_KEY = os.getenv("SECRET_KEY") # Chave secreta usada para gerar e verificar tokens JWT
ALGORITHM = os.getenv("ALGORITHM") # Algoritmo usado para criptografia dos tokens (ex: HS256)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # Tempo de expiração do token em minutos

# Cria a aplicação FastAPI
app = FastAPI()

# Define o contexto de criptografia usando bcrypt (para armazenar/verificar senhas com segurança)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define o esquema de autenticação usando OAuth2, onde o token será enviado no header da requisição
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form") # URL onde será feito o login para obter o token

# Importa os roteadores (rotas separadas em arquivos diferentes)
from auth_routes import auth_router  # Rotas relacionadas à autenticação
from order_routes import order_router  # Rotas relacionadas a pedidos (orders)

# Adiciona as rotas de autenticação à aplicação
app.include_router(auth_router)

# Adiciona as rotas de pedidos à aplicação
app.include_router(order_router)

# Para rodar o nosso código, executar no terminal: uvicorn main:app --reload