#!/usr/bin/python3
"""a class MRUCache that inherits from BaseCaching and is a caching system"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """a class that inherits from BaseCaching and is a caching system"""
    def __init__(self):
        """Initialize the MRU cache"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Assign value to cache dictionary if both key and item are not None.
        Args:
            key (str): The key for the item to be cached.
            item (str): The value to be cached.
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            most_recent_key = self.order.pop()
            del self.cache_data[most_recent_key]
            print(f"DISCARD: {most_recent_key}")
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
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
