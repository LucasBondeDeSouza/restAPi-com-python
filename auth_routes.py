from fastapi import APIRouter, Depends, HTTPException # Importa ferramentas do FastAPI para criar rotas, injetar dependências e lançar exceções HTTP
from models import Usuario # Importa o modelo de usuário do banco de dados
from dependencies import pegar_sessao, verificar_token # Importa funções auxiliares: uma para abrir a sessão do banco e outra para verificar o token JWT
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY # Importa variáveis de configuração definidas em main.py
from schemas import UsuarioSchema, LoginSchema # Importa schemas Pydantic para validar os dados de entrada
from sqlalchemy.orm import Session # Importa o tipo de sessão do SQLAlchemy
from jose import jwt, JWTError # Importa funções e exceções da biblioteca JOSE para lidar com JWT
from datetime import datetime, timedelta, timezone # Para manipular datas de expiração dos tokens
from fastapi.security import OAuth2PasswordRequestForm # Permite autenticar via formulário (usado pelo padrão OAuth2)

# Cria um roteador FastAPI com prefixo /auth e agrupa sob a tag "auth"
auth_router = APIRouter(prefix="/auth", tags=["auth"])

# ===========================================
# FUNÇÂO PARA CRIAR TOKENS JWT
# ===========================================
def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    # Define a data de expiração do token somando a duração atual
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    # Cria o payload com o ID do usuário (sub) e expiração (exp)
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    # Codifica o JWT com o payload, chave secreta e algoritmo
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


# ===========================================
# FUNÇÂO PARA AUTENTICAR USUÁRIOS
# ===========================================
def autenticar_usuario(email, senha, session):
    # Busca o usuário no banco de dados pelo e-mail
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    # Verifica se a senha informada bate com o hash no banco
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario # Retorna o objeto do usuário se autenticado com sucesso


# ===========================================
# ROTA GET
# ===========================================
@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}


# ===========================================
# ROTA PARA CRIAR CONTA (REGISTRO)
# ===========================================
@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    # Verifica se já existe um usuário com o mesmo e-mail
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        # Criptografa a senha do novo usuário
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        # Cria um novo objeto de usuário
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        # Adiciona e salva no banco
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso {usuario_schema.email}"}


# ===========================================
# ROTA DE LOGIN VIA JSON
# ===========================================
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    # Tenta autenticar o usuário com e-mail e senha
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        # Gera access token (curto prazo) e refresh token (mais longo)
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }


# ===========================================
# ROTA DE LOGIN VIA FORMULÁRIO (OAuth2)
# ===========================================
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    # O formulário envia username (email) e password
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        # Retorna apenas o access_token nesse endpoint
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }


# ===========================================
# ROTA DE REFRESH TOKEN
# ===========================================
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    # Cria um novo access token usando o usuário autenticado via refresh
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }