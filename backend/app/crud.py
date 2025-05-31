from sqlalchemy.orm import Session
from . import models, schemas, auth
from .models import InventoryItem

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    print(f"CRUD: Buscando usuário {email}") # DEBUG
    user = get_user_by_email(db, email)
    if user:
        print(f"CRUD: Usuário {email} encontrado. Verificando senha.") # DEBUG
        if auth.verify_password(password, user.hashed_password):
            print(f"CRUD: Senha verificada para {email}") # DEBUG
            return user
        else:
            print(f"CRUD: Senha incorreta para {email}") # DEBUG
    else:
        print(f"CRUD: Usuário {email} não encontrado") # DEBUG
    return None

def save_token(db: Session, token: str, token_type: str, user_id: int):
    db_token = models.TokenBlocklist(token=token, token_type=token_type, user_id=user_id, revoked=False)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def revoke_token(db: Session, token: str):
    token_db = db.query(models.TokenBlocklist).filter(models.TokenBlocklist.token == token).first()
    if token_db:
        token_db.revoked = True
        db.commit()
        return True
    return False

def is_token_revoked(db: Session, token: str):
    token_db = db.query(models.TokenBlocklist).filter(models.TokenBlocklist.token == token).first()
    return token_db is not None and token_db.revoked

def add_item(db: Session, name: str, quantity: int = 0):
    item = InventoryItem(name=name, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_item(db: Session, item_id: int):
    return db.query(InventoryItem).filter(InventoryItem.id == item_id).first()

def get_all_items(db: Session):
    return db.query(InventoryItem).all()

def update_item(db: Session, item_id: int, name: str = None, quantity: int = None):
    item = get_item(db, item_id)
    if item is None:
        return None
    if name is not None:
        item.name = name
    if quantity is not None:
        item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = get_item(db, item_id)
    if item:
        db.delete(item)
        db.commit()
        return True
    return False