from pydantic import BaseModel  # Base para criar modelos de dados com validação automática
from typing import Optional, List  # Tipos opcionais e listas para usar nos campos dos schemas

# ================================
# Schema para criar ou representar um usuário
# ================================
class UsuarioSchema(BaseModel):
    nome: str               # Nome do usuário
    email: str              # Email do usuário
    senha: str              # Senha (normalmente criptografada antes de salvar)
    ativo: Optional[bool]   # Se o usuário está ativo (opcional)
    admin: Optional[bool]   # Se o usuário é admin (opcional)

    class Config:
        from_attributes = True # Permite converter automaticamente de um modelo SQLAlchemy para esse schema


# ================================
# Schema para criar um novo pedido
# ================================
class PedidoSchema(BaseModel):
    id_usuario: int # ID do usuário que está fazendo o pedido

    class Config:
        from_attributes = True


# ================================
# Schema para login do usuário
# ================================
class LoginSchema(BaseModel):
    email: str  # Email usado para login
    senha: str  # Senha usada para login

    class Config:
        from_attributes = True


# ================================
# Schema para representar um item do pedido
# ================================
class ItemPedidoSchema(BaseModel):
    quantidade: int        # Quantidade do item
    sabor: str             # Sabor (ex: calabresa, frango, etc.)
    tamanho: str           # Tamanho (ex: pequeno, médio, grande)
    preco_unitario: float  # Preço de cada unidade

    class Config:
        from_attributes = True


# ================================
# Schema de resposta para retornar um pedido completo
# ================================
class ResponsePedidoSchema(BaseModel):
    id: int                        # ID do pedido
    status: str                    # Status (ex: PENDENTE, FINALIZADO)
    preco: float                   # Preço total do pedido
    itens: List[ItemPedidoSchema]  # Lista de itens que fazem parte do pedido

    class Config:
        from_attributes = True