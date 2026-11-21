"""輕量單檔實驗腳本：Pinecone 稠密＋稀疏（Hybrid）混合向量檢索與 CRUD 示範。"""

from __future__ import annotations

import logging
import os
import random
from typing import Dict, List, Tuple

import pinecone

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger(__name__)

DENSE_DIMENSION = 16
SPARSE_VOCAB_SIZE = 100
DEFAULT_HYBRID_ALPHA = 0.75
DEFAULT_NAMESPACE = "example-namespace"


def hybrid_score_norm(
    dense: List[float],
    sparse: Dict[str, List],
    alpha: float,
) -> Tuple[List[float], Dict[str, List]]:
    """依凸組合公式（alpha * dense + (1 - alpha) * sparse）縮放混合檢索權重。"""
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("權重參數 alpha 必須介於 0.0 與 1.0 之間")
    scaled_sparse = {
        "indices": sparse["indices"],
        "values": [value * (1.0 - alpha) for value in sparse["values"]],
    }
    scaled_dense = [value * alpha for value in dense]
    return scaled_dense, scaled_sparse


def generate_random_sparse_vector(
    vocab_size: int,
    min_value: float = 0.0,
    max_value: float = 1.0,
) -> Dict[str, List]:
    """產生索引不重複且已排序的隨機稀疏向量。"""
    sample_size = random.randint(1, min(10, vocab_size))
    indices = sorted(random.sample(range(vocab_size), sample_size))
    values = [random.uniform(min_value, max_value) for _ in indices]
    return {"indices": indices, "values": values}


def generate_random_dense_vector(
    dimension: int,
    min_value: float = 0.0,
    max_value: float = 1.0,
) -> List[float]:
    """產生指定維度的隨機稠密向量。"""
    return [random.uniform(min_value, max_value) for _ in range(dimension)]


def main() -> None:
    """執行 Pinecone 索引寫入、混合檢索、更新與刪除示範。"""
    api_key = os.getenv("PINECONE_API_KEY", "").strip()
    if not api_key:
        raise ValueError("請先設定環境變數 PINECONE_API_KEY 再執行示範腳本")

    environment = os.getenv("PINECONE_ENVIRONMENT", "us-west4-gcp-free")
    index_name = os.getenv("PINECONE_INDEX", "test")

    pinecone.init(api_key=api_key, environment=environment)
    logger.info("目前可用索引：%s", pinecone.list_indexes())

    index = pinecone.Index(index_name)
    logger.info("索引統計資訊：%s", index.describe_index_stats())

    dense_1 = generate_random_dense_vector(DENSE_DIMENSION)
    dense_2 = generate_random_dense_vector(DENSE_DIMENSION)
    sparse_1 = generate_random_sparse_vector(SPARSE_VOCAB_SIZE)
    sparse_2 = generate_random_sparse_vector(SPARSE_VOCAB_SIZE)

    index.upsert(
        vectors=[
            {"id": "vec1", "values": dense_1, "metadata": {"genre": "drama"}, "sparse_values": sparse_1},
            {"id": "vec2", "values": dense_2, "metadata": {"genre": "action"}, "sparse_values": sparse_2},
        ],
        namespace=DEFAULT_NAMESPACE,
    )

    q_dense, q_sparse = hybrid_score_norm(
        generate_random_dense_vector(DENSE_DIMENSION),
        generate_random_sparse_vector(SPARSE_VOCAB_SIZE),
        alpha=DEFAULT_HYBRID_ALPHA,
    )
    query_res = index.query(
        namespace=DEFAULT_NAMESPACE,
        top_k=10,
        vector=q_dense,
        sparse_vector=q_sparse,
    )
    logger.info("混合檢索結果：%s", query_res)

    logger.info("查詢 vec1：%s", index.fetch(["vec1"], namespace=DEFAULT_NAMESPACE))
    index.update(id="vec1", values=dense_2, set_metadata={"type": "webdoc"}, namespace=DEFAULT_NAMESPACE)
    logger.info("更新後 vec1：%s", index.fetch(["vec1"], namespace=DEFAULT_NAMESPACE))
    index.delete(ids=["vec2"], namespace=DEFAULT_NAMESPACE)
    logger.info("已刪除示範向量 vec2")


if __name__ == "__main__":
    main()
