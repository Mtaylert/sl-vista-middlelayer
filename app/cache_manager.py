class CacheManager:
    local_cache = []

    @classmethod
    def create_cache(cls):
        cls.local_cache = []

    @classmethod
    def add_to_cache(cls, input_data):
        cls.local_cache.append(input_data)

    @classmethod
    def fetch_from_cache(cls):
        if cls.local_cache:
            print("FOUND")
            return cls.local_cache
        else:
            return None

    @classmethod
    def clear_from_cache(cls):
        cls.local_cache = []
