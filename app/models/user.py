from app import db
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'usuarios'  
    
    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nombre_usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido_usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    email_usuario: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_usuario: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    calificaciones: Mapped[List["Rating"]] = relationship(back_populates="usuario")
    biblioteca: Mapped[List["UserLibrary"]] = relationship(back_populates="usuario")
    
    def __init__(self, nombre_usuario: str, apellido_usuario: str, email_usuario: str, password_usuario: str):
        self.nombre_usuario = nombre_usuario
        self.apellido_usuario = apellido_usuario
        self.email_usuario = email_usuario
        self.password_usuario = generate_password_hash(password_usuario)
    
    def set_password(self, password: str) -> None:
        self.password_usuario = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_usuario, password)
    
    def serialize(self) -> Dict[str, Any]:
        return {
            "id_usuario": self.id_usuario,
            "nombre_usuario": self.nombre_usuario,
            "apellido_usuario": self.apellido_usuario,
            "email_usuario": self.email_usuario,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def serialize_public(self) -> Dict[str, Any]:
        return {
            "id_usuario": self.id_usuario,
            "nombre_usuario": self.nombre_usuario,
            "apellido_usuario": self.apellido_usuario,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }