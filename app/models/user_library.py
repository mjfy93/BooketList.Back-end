from app import db
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserLibrary(db.Model):
    __tablename__ = 'biblioteca_usuario'
    
    id_biblioteca: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuarios.id_usuario'), nullable=False)
    id_libro: Mapped[int] = mapped_column(ForeignKey('libros.id_libro'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    usuario: Mapped["User"] = relationship(back_populates="biblioteca")
    libro: Mapped["Book"] = relationship(back_populates="biblioteca")
    
    def serialize(self) -> Dict[str, Any]:
        return {
            "id_biblioteca": self.id_biblioteca,
            "id_usuario": self.id_usuario,
            "id_libro": self.id_libro,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }