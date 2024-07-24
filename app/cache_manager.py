class CacheManager:
    local_cache = []
    sales_cache = {}

    @classmethod
    def create_cache(cls):
        cls.local_cache = []
        cls.sales_cache = {}

    @classmethod
    def add_to_cache(cls, input_data, sales_checklist):
        if input_data:
            cls.local_cache.append(input_data)

        if sales_checklist:
            cls.sales_cache.update(sales_checklist)

    @classmethod
    def fetch_from_cache(cls):
        if cls.local_cache or cls.sales_cache:
            print("FOUND")
            if cls.local_cache:
                cls.local_cache.reverse()
            return {
                "recommendation": cls.local_cache,
                "sales_checklist": cls.sales_cache,
            }
        else:
            return None

    @classmethod
    def clear_from_cache(cls):
        cls.local_cache = []
        cls.sales_cache = {}
