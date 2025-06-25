from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema # Variáveis e esquema de autenticação definidos em main.py
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError # Biblioteca para codificar e decodificar tokens JWT

# ================================
# Dependência para obter uma sessão com o banco de dados
# ================================
def pegar_sessao():
    try:
        # Cria uma fábrica de sessões SQLAlchemy vinculada ao banco
        Session = sessionmaker(bind=db)
        session = Session() # Cria a sessão
        yield session # Retorna a sessão para uso (com 'yield', ela é usada como uma dependência injetável)
    finally:
        session.close() # Garante que a sessão será fechada após o uso


# ================================
# Dependência para verificar o token JWT de autenticação
# ================================
def verificar_token(
        token: str = Depends(oauth2_schema), # Obtém o token automaticamente do header Authorization
        session: Session = Depends(pegar_sessao) # Usa a sessão do banco via dependência
    ):
    try:
        # Decodifica o token usando a chave secreta e o algoritmo definidos
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub")) # Extrai o ID do usuário (sub = subject)
    except JWTError:
        # Caso o token esteja inválido ou expirado
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a válidade do token")
    # Busca o usuário no banco pelo ID extraído do token
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        # Caso o usuário não exista no banco
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario # Retorna o objeto usuário para uso nos endpoints protegidos