"""
Snowflake ID 生成器
生成 64 位整形的唯一 ID
结构: 1位符号位 + 41位时间戳 + 5位数据中心ID + 5位工作节点ID + 12位序列号
"""
import time
from typing import Optional
from app.core.config import get_settings

settings = get_settings()


class SnowflakeIDGenerator:
    """Snowflake ID 生成器"""

    # 起始时间戳 (2024-01-01 00:00:00)
    TWITTER_EPOCH = 1704067200000

    # 各部分的位数
    WORKER_ID_BITS = 5
    DATACENTER_ID_BITS = 5
    SEQUENCE_BITS = 12

    # 各部分的最大值
    MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1
    MAX_DATACENTER_ID = (1 << DATACENTER_ID_BITS) - 1
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

    # 各部分的位移
    WORKER_ID_SHIFT = SEQUENCE_BITS
    DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    def __init__(self, datacenter_id: int = 1, worker_id: int = 1):
        """
        初始化 ID 生成器

        Args:
            datacenter_id: 数据中心 ID (0-31)
            worker_id: 工作节点 ID (0-31)
        """
        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError(f"Datacenter ID 必须在 0-{self.MAX_DATACENTER_ID} 之间")

        if worker_id > self.MAX_WORKER_ID or worker_id < 0:
            raise ValueError(f"Worker ID 必须在 0-{self.MAX_WORKER_ID} 之间")

        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1

    def _current_millis(self) -> int:
        """获取当前时间戳（毫秒）"""
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp: int) -> int:
        """等待下一毫秒"""
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            timestamp = self._current_millis()
        return timestamp

    def generate_id(self) -> int:
        """
        生成唯一的 Snowflake ID

        Returns:
            64 位整形的唯一 ID
        """
        timestamp = self._current_millis()

        # 如果当前时间小于上次生成ID的时间，说明时钟回拨，抛出异常
        if timestamp < self.last_timestamp:
            raise Exception(f"时钟回拨。拒绝生成 ID {self.last_timestamp - timestamp} 毫秒")

        # 如果是同一毫秒内生成的ID
        if timestamp == self.last_timestamp:
            # 序列号自增
            self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
            # 如果序列号溢出，等待下一毫秒
            if self.sequence == 0:
                timestamp = self._wait_next_millis(self.last_timestamp)
        else:
            # 不同毫秒，序列号重置
            self.sequence = 0

        self.last_timestamp = timestamp

        # 组合生成 ID
        snowflake_id = (
            ((timestamp - self.TWITTER_EPOCH) << self.TIMESTAMP_SHIFT)
            | (self.datacenter_id << self.DATACENTER_ID_SHIFT)
            | (self.worker_id << self.WORKER_ID_SHIFT)
            | self.sequence
        )

        return snowflake_id


# 创建全局 ID 生成器实例
_datacenter_id = getattr(settings, "DATACENTER_ID", 1)
_worker_id = getattr(settings, "WORKER_ID", 1)
_id_generator = SnowflakeIDGenerator(datacenter_id=_datacenter_id, worker_id=_worker_id)


def generate_snowflake_id() -> int:
    """
    生成 Snowflake ID 的便捷函数

    Returns:
        64 位整形的唯一 ID
    """
    return _id_generator.generate_id()
