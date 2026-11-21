"""Pinecone hybrid (dense + sparse) vector search & CRUD experiment."""

from __future__ import annotations

import logging
import os
import random
from typing import Dict, List, Tuple

import pinecone

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger("pinecone_hybrid_demo")


def hybrid_score_norm(
    dense: List[float],
    sparse: Dict[str, List],
    alpha: float,
) -> Tuple[List[float], Dict[str, List]]:
    """Scale dense and sparse vectors for convex hybrid search (`alpha * dense + (1 - alpha) * sparse`)."""
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be between 0 and 1")
    scaled_sparse = {
        "indices": sparse["indices"],
        "values": [v * (1.0 - alpha) for v in sparse["values"]],
    }
    scaled_dense = [v * alpha for v in dense]
    return scaled_dense, scaled_sparse


def generate_random_sparse_vector(
    vocab_size: int,
    min_value: float = 0.0,
    max_value: float = 1.0,
) -> Dict[str, List]:
    """Generate a random sparse vector with unique sorted indices."""
    k = random.randint(1, min(10, vocab_size))
    indices = sorted(random.sample(range(vocab_size), k))
    values = [random.uniform(min_value, max_value) for _ in indices]
    return {"indices": indices, "values": values}


def generate_random_dense_vector(
    dimension: int,
    min_value: float = 0.0,
    max_value: float = 1.0,
) -> List[float]:
    """Generate a random dense vector of fixed `dimension`."""
    return [random.uniform(min_value, max_value) for _ in range(dimension)]


def main() -> None:
    api_key = os.getenv("PINECONE_API_KEY")
    environment = os.getenv("PINECONE_ENVIRONMENT", "us-west4-gcp-free")
    index_name = os.getenv("PINECONE_INDEX", "test")
    namespace = "example-namespace"

    if not api_key:
        raise RuntimeError("Please set PINECONE_API_KEY environment variable before running this demo.")

    pinecone.init(api_key=api_key, environment=environment)
    logger.info("Available indexes: %s", pinecone.list_indexes())

    index = pinecone.Index(index_name)
    logger.info("Index stats: %s", index.describe_index_stats())

    # 1. Upsert sample dense + sparse hybrid vectors
    dense_1 = generate_random_dense_vector(16)
    dense_2 = generate_random_dense_vector(16)
    sparse_1 = generate_random_sparse_vector(100)
    sparse_2 = generate_random_sparse_vector(100)

    index.upsert(
        vectors=[
            {"id": "vec1", "values": dense_1, "metadata": {"genre": "drama"}, "sparse_values": sparse_1},
            {"id": "vec2", "values": dense_2, "metadata": {"genre": "action"}, "sparse_values": sparse_2},
        ],
        namespace=namespace,
    )

    # 2. Hybrid query (alpha=0.75 favors dense semantic similarity)
    q_dense, q_sparse = hybrid_score_norm(
        generate_random_dense_vector(16),
        generate_random_sparse_vector(100),
        alpha=0.75,
    )
    query_res = index.query(namespace=namespace, top_k=10, vector=q_dense, sparse_vector=q_sparse)
    logger.info("Hybrid query response: %s", query_res)

    # 3. Fetch, update metadata, and delete sample record
    logger.info("Fetch vec1: %s", index.fetch(["vec1"], namespace=namespace))
    index.update(id="vec1", values=dense_2, set_metadata={"type": "webdoc"}, namespace=namespace)
    logger.info("Updated vec1: %s", index.fetch(["vec1"], namespace=namespace))
    index.delete(ids=["vec2"], namespace=namespace)
    logger.info("Deleted vec2 successfully.")


if __name__ == "__main__":
    main()
