import faiss
import pickle
import json
import uuid
import shutil
from typing import List, Dict, Any
import os
import logging
import hashlib
import numpy as np

logger = logging.getLogger(__name__)

# 向量维度
EMBEDDING_DIM = 384


def compute_embedding(text: str) -> np.ndarray:
    """计算文本的embedding向量"""
    if not text or not isinstance(text, str):
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)
    
    # 使用SHA256哈希生成固定长度的向量
    hash_obj = hashlib.sha256(text.encode('utf-8'))
    hash_bytes = hash_obj.digest()
    
    # 将32字节的哈希转换为384维向量
    embedding = np.zeros(EMBEDDING_DIM, dtype=np.float32)
    for i in range(EMBEDDING_DIM):
        byte_val = hash_bytes[i % len(hash_bytes)]
        embedding[i] = float(byte_val) / 255.0
    
    return embedding


class VectorStore:
    def __init__(self):
        """初始化FAISS向量存储"""
        self.base_path = "./faiss_db"
        os.makedirs(self.base_path, exist_ok=True)
        logger.info("VectorStore初始化完成（使用FAISS）")
    
    def _get_collection_path(self, company_id: str) -> str:
        """获取集合的存储路径"""
        return os.path.join(self.base_path, f"company_{company_id}")
    
    def _load_collection(self, company_id: str) -> tuple:
        """
        加载集合数据
        返回: (index, documents, ids, metadatas) 或 None
        """
        collection_path = self._get_collection_path(company_id)
        
        index_path = os.path.join(collection_path, "index.faiss")
        data_path = os.path.join(collection_path, "data.pkl")
        
        if not os.path.exists(index_path) or not os.path.exists(data_path):
            return None
        
        try:
            # 加载FAISS索引
            index = faiss.read_index(index_path)
            
            # 加载文档数据
            with open(data_path, 'rb') as f:
                data = pickle.load(f)
                documents = data.get('documents', [])
                ids = data.get('ids', [])
                metadatas = data.get('metadatas', [])
            
            return (index, documents, ids, metadatas)
        except Exception as e:
            logger.error(f"加载集合失败: {e}", exc_info=True)
            return None
    
    def _save_collection(self, company_id: str, index: faiss.Index, 
                        documents: List[str], ids: List[str], 
                        metadatas: List[Dict[str, Any]]):
        """保存集合数据"""
        collection_path = self._get_collection_path(company_id)
        os.makedirs(collection_path, exist_ok=True)
        
        index_path = os.path.join(collection_path, "index.faiss")
        data_path = os.path.join(collection_path, "data.pkl")
        
        try:
            # 保存FAISS索引
            faiss.write_index(index, index_path)
            
            # 保存文档数据
            data = {
                'documents': documents,
                'ids': ids,
                'metadatas': metadatas
            }
            with open(data_path, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"集合保存成功: {collection_path}")
        except Exception as e:
            logger.error(f"保存集合失败: {e}", exc_info=True)
            raise
    
    async def add_documents(
        self,
        company_id: str,
        documents: List[str],
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        添加文档到向量数据库
        """
        logger.info(f"开始添加文档到 company_{company_id}，共 {len(documents)} 个文档块")
        
        # 生成文档ID
        file_id = str(uuid.uuid4())
        
        # 计算embeddings
        logger.info("开始计算embeddings...")
        embeddings = []
        ids = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            doc_id = f"{file_id}_{i}"
            ids.append(doc_id)
            
            # 计算embedding
            embedding = compute_embedding(doc)
            embeddings.append(embedding)
            
            # 创建元数据
            doc_metadata = {
                "file_id": file_id,
                "chunk_index": i,
                **(metadata or {})
            }
            metadatas.append(doc_metadata)
        
        logger.info(f"计算完成，共 {len(embeddings)} 个embeddings")
        
        # 加载现有集合或创建新集合
        collection_data = self._load_collection(company_id)
        
        if collection_data is None:
            # 创建新索引
            index = faiss.IndexFlatIP(EMBEDDING_DIM)  # 使用内积（点积）相似度
            existing_documents = []
            existing_ids = []
            existing_metadatas = []
        else:
            index, existing_documents, existing_ids, existing_metadatas = collection_data
            logger.info(f"加载现有集合，已有 {len(existing_documents)} 个文档")
        
        # 将embeddings转换为numpy数组
        embeddings_array = np.array(embeddings, dtype=np.float32)
        
        # 归一化向量（用于余弦相似度）
        faiss.normalize_L2(embeddings_array)
        
        # 添加到索引
        index.add(embeddings_array)
        logger.info(f"已添加 {len(embeddings)} 个向量到索引")
        
        # 合并文档数据
        all_documents = existing_documents + documents
        all_ids = existing_ids + ids
        all_metadatas = existing_metadatas + metadatas
        
        # 保存集合
        self._save_collection(company_id, index, all_documents, all_ids, all_metadatas)
        
        logger.info(f"成功添加 {len(documents)} 个文档块到集合")
        return file_id
    
    async def search(
        self,
        company_id: str,
        query: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        在向量数据库中搜索相关文档
        """
        # 加载集合
        collection_data = self._load_collection(company_id)
        
        if collection_data is None:
            logger.info(f"集合 company_{company_id} 不存在，返回空结果")
            return []
        
        index, documents, ids, metadatas = collection_data
        
        if len(documents) == 0:
            logger.info(f"集合 company_{company_id} 为空，返回空结果")
            return []
        
        # 计算查询向量
        query_embedding = compute_embedding(query)
        query_vector = query_embedding.reshape(1, -1).astype(np.float32)
        
        # 归一化查询向量
        faiss.normalize_L2(query_vector)
        
        # 搜索
        logger.info(f"开始搜索，查询向量维度: {query_vector.shape}")
        k = min(n_results, len(documents))
        distances, indices = index.search(query_vector, k)
        
        # 格式化结果
        formatted_results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(documents):
                formatted_results.append({
                    "content": documents[idx],
                    "metadata": metadatas[idx] if idx < len(metadatas) else {},
                    "distance": float(distances[0][i]) if distances[0][i] >= 0 else None
                })
        
        logger.info(f"搜索完成，找到 {len(formatted_results)} 个结果")
        return formatted_results
    
    async def get_documents(self, company_id: str) -> List[Dict[str, Any]]:
        """
        获取指定公司的所有文档
        """
        collection_data = self._load_collection(company_id)
        
        if collection_data is None:
            return []
        
        _, documents, ids, metadatas = collection_data
        
        # 按file_id分组
        files = {}
        for i, metadata in enumerate(metadatas):
            fid = metadata.get('file_id', 'unknown')
            if fid not in files:
                files[fid] = {
                    "file_id": fid,
                    "filename": metadata.get('filename', 'unknown'),
                    "chunks_count": 0
                }
            files[fid]["chunks_count"] += 1
        
        return list(files.values())
    
    async def delete_document(self, company_id: str, file_id: str):
        """
        删除指定文档的所有块
        """
        collection_data = self._load_collection(company_id)
        
        if collection_data is None:
            logger.warning(f"集合 company_{company_id} 不存在")
            return
        
        index, documents, ids, metadatas = collection_data
        
        # 找到要删除的索引
        indices_to_keep = []
        new_documents = []
        new_ids = []
        new_metadatas = []
        
        for i, metadata in enumerate(metadatas):
            if metadata.get('file_id') != file_id:
                indices_to_keep.append(i)
                new_documents.append(documents[i])
                new_ids.append(ids[i])
                new_metadatas.append(metadatas[i])
        
        if len(indices_to_keep) == len(documents):
            logger.info(f"未找到 file_id={file_id} 的文档")
            return
        
        # 重建索引
        if len(new_documents) == 0:
            # 删除整个集合
            collection_path = self._get_collection_path(company_id)
            if os.path.exists(collection_path):
                shutil.rmtree(collection_path)
                logger.info(f"已删除集合: {collection_path}")
        else:
            # 重新计算embeddings并重建索引
            logger.info(f"重建索引，保留 {len(new_documents)} 个文档")
            new_index = faiss.IndexFlatIP(EMBEDDING_DIM)
            new_embeddings = []
            
            for doc in new_documents:
                embedding = compute_embedding(doc)
                new_embeddings.append(embedding)
            
            embeddings_array = np.array(new_embeddings, dtype=np.float32)
            faiss.normalize_L2(embeddings_array)
            new_index.add(embeddings_array)
            
            # 保存更新后的集合
            self._save_collection(company_id, new_index, new_documents, new_ids, new_metadatas)
            logger.info(f"已删除 file_id={file_id} 的所有文档块")
