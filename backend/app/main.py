from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app import models, schemas, database, crud, auth
from app.auth import get_current_user
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.models import InventoryItem
from fastapi import APIRouter




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 50
REFRESH_TOKEN_EXPIRE_DAYS = 7



origins = ["http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.create_user(db, user)

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_auth = crud.authenticate_user(db, user.email, user.password)
    if not user_auth:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(
        data={"sub": user_auth.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = auth.create_refresh_token(
        data={"sub": user_auth.email},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Salvar tokens no banco
    crud.save_token(db, access_token, "access", user_auth.id)
    crud.save_token(db, refresh_token, "refresh", user_auth.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.get("/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}

@app.post("/refresh", response_model=schemas.Token)
def refresh_token(token_refresh: schemas.TokenRefresh, db: Session = Depends(get_db)):
    refresh_token = token_refresh.refresh_token

    try:
        payload = jwt.decode(refresh_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # Verificar se o refresh token está no banco (não revogado)
        if crud.is_token_revoked(db, refresh_token):
            raise HTTPException(status_code=401, detail="Token revoked")

        user = crud.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Criar novos tokens
        access_token = auth.create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        new_refresh_token = auth.create_refresh_token(
            data={"sub": email},
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        # Revoke old refresh token e salvar os novos tokens
        crud.revoke_token(db, refresh_token)
        crud.save_token(db, access_token, "access", user.id)
        crud.save_token(db, new_refresh_token, "refresh", user.id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    revoked = crud.revoke_token(db, token)
    if revoked:
        return {"msg": "Logout successful"}
    raise HTTPException(status_code=400, detail="Invalid token or already logged out")

@app.post("/inventory", response_model=schemas.InventoryItemResponse)
def create_item(
    item: schemas.InventoryCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db_item = db.query(InventoryItem).filter(InventoryItem.name == item.name).first()
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    new_item = InventoryItem(name=item.name, quantity=item.quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.get("/inventory", response_model=list[schemas.InventoryItemResponse])
def list_items(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(InventoryItem).all()

@app.get("/inventory/{item_id}", response_model=schemas.InventoryItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/inventory/{item_id}", response_model=schemas.InventoryItemResponse)
def update_item(
    item_id: int,
    update: schemas.InventoryUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if update.name is not None:
        item.name = update.name
    if update.quantity is not None:
        item.quantity = update.quantity
    db.commit()
    db.refresh(item)
    return item

@app.delete("/inventory/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"ok": True}