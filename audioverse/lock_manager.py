import threading


class GPTLockManager:
    lock = None

    @classmethod
    def __enter__(cls):
        if cls.lock is None:
            cls.lock = threading.Lock()
        cls.lock.acquire()

    @classmethod
    def __exit__(cls, exc_type, exc_val, exc_tb):
        cls.lock.release()
        cls.lock = None
