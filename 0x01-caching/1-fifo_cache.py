#!/usr/bin/python3
"""a class BasicCache that inherits from BaseCaching and is a caching system"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """a class that inherits from BaseCaching and is a caching system """
    def __init__(self):
        """ Initiliaze"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Assign value to the cache dictionary if both key,item are not None.
        Args:
            key (str): The key for the item to be cached.
            item (str): The value to be cached.
        If key or item is None, do nothing.
        """
        if key is None and item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                first_key = self.order.pop(0)
                del self.cache_data[first_key]
                print(f"DISCARD: {first_key}")
            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """Retrieve the value from the cache dictionary.
        Args:
            key (str): The key of the item to retrieve.
        Returns:
            str: cached value of the key, or None if key is None or not found.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
