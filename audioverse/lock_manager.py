import threading
import time

from audioverse.decorators import lock_release_decorator


class GPTLockManager:
    gpt_lock = threading.Lock()

    @classmethod
    def __enter__(cls):
        cls.gpt_lock.acquire()

    @classmethod
    @lock_release_decorator
    def __exit__(cls, exc_type, exc_val, exc_tb):
        cls.gpt_lock.release()

    @classmethod
    def force_release(cls):
        if cls.gpt_lock.locked():
            cls.gpt_lock.release()


class EmbeddingLockManager:
    emb_lock = threading.Lock()

    @classmethod
    def __enter__(cls):
        cls.emb_lock.acquire()

    @classmethod
    @lock_release_decorator
    def __exit__(cls, exc_type, exc_val, exc_tb):
        cls.emb_lock.release()

    @classmethod
    def force_release(cls):
        if cls.emb_lock.locked():
            cls.emb_lock.release()


gpt_lock_manager = GPTLockManager()
embedding_lock_manager = EmbeddingLockManager()
