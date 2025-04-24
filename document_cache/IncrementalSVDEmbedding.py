import numpy as np
from scipy.linalg import svd
from scipy import sparse
from typing import Optional, Union

class IncrementalSVDEmbedding:
    def __init__(
        self,
        num_nodes: int,
        embedding_dim: int = 32,
        *, 
        recon_error_threshold: float = 0.1,  # 触发重计算的累计误差阈值
        max_updates_before_recompute: int = 50,  # 最大增量更新次数后强制重计算
        sparse_mode: bool = False  # 是否使用稀疏矩阵优化
    ):
        """
        改进版增量SVD嵌入器（带周期性精确重计算）
        
        参数:
            num_nodes: 节点总数
            embedding_dim: 嵌入维度
            recon_error_threshold: 重构误差累计阈值，超过则触发重计算
            max_updates_before_recompute: 最大增量更新次数后强制重计算
            sparse_mode: 使用稀疏矩阵存储变化（适合delta_C稀疏场景）
        """
        self.n = num_nodes
        self.d = embedding_dim
        self.error_threshold = recon_error_threshold
        self.max_updates = max_updates_before_recompute
        
        # 状态跟踪
        self._update_count = 0
        self._accumulated_error = 0.0
        self._delta_norm_history = []
        
        # 核心参数
        self.U: Optional[np.ndarray] = None      # 左奇异向量 (n x d)
        self.s: Optional[np.ndarray] = None      # 奇异值 (d,)
        self.VT: Optional[np.ndarray] = None    # 右奇异向量转置 (d x n)
        self.C_approx: Optional[np.ndarray] = None  # 当前近似矩阵（用于误差计算）
        self.is_trained = False
        
        # 稀疏模式设置
        self.sparse_mode = sparse_mode
        if sparse_mode:

            self.sparse = sparse
            self.dtype = np.float32
        else:
            self.dtype = np.float64

    def init_svd(self, C: Union[np.ndarray]):
        """初始精确SVD分解"""
        assert C.shape == (self.n, self.n), f"共现矩阵应为 {self.n}x{self.n}"
        
        if self.sparse_mode and not isinstance(C, self.sparse.csr_matrix):
            C = self.sparse.csr_matrix(C, dtype=self.dtype)
        
        # 精确计算初始SVD
        if self.sparse_mode:
            U, s, VT = self.sparse.linalg.svds(C, k=self.d)
            # 确保奇异值降序排列
            idx = np.argsort(s)[::-1]
            self.U, self.s, self.VT = U[:, idx], s[idx], VT[idx, :]
        else:
            U, s, VT = svd(C, full_matrices=False)
            self.U, self.s, self.VT = U[:, :self.d], s[:self.d], VT[:self.d, :]
        
        self.C_approx = self.U @ np.diag(self.s) @ self.VT
        self.is_trained = True
        self._reset_tracking()

    def _reset_tracking(self):
        """重置误差统计和更新计数"""
        self._update_count = 0
        self._accumulated_error = 0.0
        self._delta_norm_history = []

    def _needs_recompute(self, delta_norm: float) -> bool:
        """
        判断是否需要触发精确重计算
        基于：1) 更新次数阈值 2) 累计误差阈值 3) 最近变化幅度
        """
        self._update_count += 1
        self._delta_norm_history.append(delta_norm)
        
        # 条件1: 达到最大更新次数
        if self._update_count >= self.max_updates:
            return True
        
        # 条件2: 累计误差超过阈值
        self._accumulated_error += delta_norm * 0.1  # 加权累计
        if self._accumulated_error > self.error_threshold:
            return True
        
        # 条件3: 检测到突变（最近3次变化幅度增大）
        if len(self._delta_norm_history) >= 3:
            recent_avg = np.mean(self._delta_norm_history[-3:])
            if recent_avg > 2 * np.mean(self._delta_norm_history[:-3]):
                return True
                
        return False

    def update(self, delta_C: Union[np.ndarray]):
        """
        增量更新SVD参数，自动触发重计算当满足条件时
        
        参数:
            delta_C: 共现矩阵的变化部分（支持稀疏矩阵）
        """
        assert delta_C.shape == (self.n, self.n), f"变化矩阵应为 {self.n}x{self.n}"
        
        if not self.is_trained:
            raise RuntimeError("请先调用init_svd初始化")
        
        # 转换为稀疏矩阵（如果启用稀疏模式）
        if self.sparse_mode and not isinstance(delta_C, self.sparse.csr_matrix):
            delta_C = self.sparse.csr_matrix(delta_C, dtype=self.dtype)
        
        # 计算当前变化幅度（用于误差判断）
        delta_norm = np.linalg.norm(delta_C) if not self.sparse_mode else self.sparse.linalg.norm(delta_C)
        
        # 判断是否需要精确重计算
        if self._needs_recompute(delta_norm):
            if self.sparse_mode:
                new_C = self.C_approx + delta_C
                self.init_svd(new_C)
            else:
                self.init_svd(self.C_approx + delta_C)
            return
        
        # --- 增量SVD核心步骤 ---
        # 计算残差（投影到正交补空间）
        if self.sparse_mode:
            U_deltaC = self.U.T @ delta_C  # (d x n)
            residual = delta_C - self.U @ U_deltaC
            residual -= (residual @ self.VT.T) @ self.VT
            Q, _ = np.linalg.qr(residual.toarray())  # 注意：此处稀疏转密集
        else:
            residual = delta_C - self.U @ (self.U.T @ delta_C)
            residual -= (residual @ self.VT.T) @ self.VT
            Q, _ = np.linalg.qr(residual)
        
        # 构造合并矩阵K
        U_deltaC_VT = self.U.T @ delta_C @ self.VT.T
        upper_block = np.diag(self.s) + U_deltaC_VT
        right_block = self.U.T @ delta_C @ Q.T
        lower_block = Q.T @ delta_C @ self.VT.T
        diag_block = Q.T @ delta_C @ Q
        
        K = np.block([
            [upper_block, right_block],
            [lower_block, diag_block]
        ])
        
        # 对K进行SVD
        UK, s_new, VTK = svd(K, full_matrices=False)
        
        # 更新参数
        self.U = np.hstack([self.U, Q]) @ UK[:, :self.d]
        self.s = s_new[:self.d]
        self.VT = (np.hstack([self.VT.T, Q])) @ VTK.T[:self.d, :].T
        
        # 更新近似矩阵（用于后续误差计算）
        self.C_approx = self.U @ np.diag(self.s) @ self.VT

    def get_embeddings(self, side: str = 'left') -> np.ndarray:
        """
        获取节点嵌入表示（自动归一化处理）
        
        参数:
            side: 'left'返回UΣ^(1/2)，'right'返回Σ^(1/2)VT (默认'left')
        返回:
            (n x d)的嵌入矩阵（已做L2归一化）
        """
        if not self.is_trained:
            raise RuntimeError("模型未训练")
            
        sqrt_s = np.sqrt(self.s)
        if side == 'left':
            emb = self.U * sqrt_s.reshape(1, -1)
        elif side == 'right':
            emb = (sqrt_s.reshape(-1, 1) * self.VT).T
        else:
            raise ValueError("side必须是'left'或'right'")
        
        # 行归一化（可选）
        return emb / np.linalg.norm(emb, axis=1, keepdims=True)

    def get_reconstruction_error(self) -> float:
        """计算当前近似矩阵与真实矩阵的Frobenius范数误差"""
        if not hasattr(self, 'C_true'):
            raise RuntimeError("需要先设置真实矩阵C_true")
        return np.linalg.norm(self.C_true - self.C_approx, 'fro')