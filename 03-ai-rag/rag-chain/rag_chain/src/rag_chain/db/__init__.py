# rag_chain/db/__init__.py

from .session import SessionLocal
from .models import Vector  # 假設你有一個Vector模型

def get_all_vectors():
    """檢索資料庫中所有向量的簡化示例"""
    # 建立一個新的資料庫會話實例
    db = SessionLocal()
    try:
        # 查詢所有Vector記錄
        vectors = db.query(Vector).all()
        return vectors
    finally:
        # 關閉會話
        db.close()

