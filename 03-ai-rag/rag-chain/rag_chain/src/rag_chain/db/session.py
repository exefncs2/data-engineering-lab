from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rag_chain.core.config import settings
from .models import Vector  # 假設你的模型名爲 Vector

engine = create_engine(settings.database_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_vector_by_id(vector_id: int):
    """
    根據提供的向量 ID 從資料庫檢索向量。
    
    參數:
    - vector_id (int): 要檢索的向量的 ID。
    
    回傳:
    - VectorModel 實例，如果找到對應的向量；否則回傳 None。
    """
    db: Session = SessionLocal()
    try:
        return db.query(Vector).filter(Vector.id == vector_id).first()
    finally:
        db.close()

def create_vector(vector_data: dict):
    """
    建立一個新的向量並存儲在資料庫中。
    
    參數:
    - vector_data (dict): 包含向量描述和值的字典。
    
    回傳:
    - 建立的 VectorModel 實例。
    """
    db = SessionLocal()
    try:
        # 建立一個新的 Vector 實例
        vector = Vector(**vector_data)
        db.add(vector)
        db.commit()
        db.refresh(vector)  # 重新載入實例以取得分配的 ID 等
        return vector
    finally:
        db.close()

def update_vector(vector_id: int, vector_data: dict):
    """
    更新資料庫中的特定向量。
    
    參數:
    - vector_id (int): 要更新的向量的 ID。
    - vector_data (dict): 包含更新資料的字典。
    
    回傳:
    - 更新後的 VectorModel 實例，如果找到併成功更新；否則回傳 None。
    """
    db = SessionLocal()
    try:
        vector = db.query(Vector).filter(Vector.id == vector_id).first()
        if vector:
            for key, value in vector_data.items():
                setattr(vector, key, value)
            db.commit()
            db.refresh(vector)
            return vector
        return None
    finally:
        db.close()

