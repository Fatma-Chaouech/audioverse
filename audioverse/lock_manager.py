import threading
import time


class GPTLockManager:
    gpt_lock = threading.Lock()

    @classmethod
    def __enter__(cls):
        cls.gpt_lock.acquire()

    @classmethod
    def __exit__(cls, exc_type, exc_val, exc_tb):
        print("Sleeping for 20 seconds in GPTLockManager")
        time.sleep(20)
        cls.gpt_lock.release()
        print("Lock released in GPTLockManager")

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
    def __exit__(cls, exc_type, exc_val, exc_tb):
        print("Sleeping for 20 seconds in EmbeddingLockManager")
        time.sleep(20)
        cls.emb_lock.release()
        print("Lock released in EmbeddingLockManager")

    @classmethod
    def force_release(cls):
        if cls.emb_lock.locked():
            cls.emb_lock.release()


gpt_lock_manager = GPTLockManager()
embedding_lock_manager = EmbeddingLockManager()
