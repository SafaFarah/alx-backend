#!/usr/bin/python3
"""a class BasicCache that inherits from BaseCaching and is a caching system"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Basic caching system with no limit on cache size.
    """
    def put(self, key, item):
        """Assign value to the cache dictionary if both key,item are not None.
        Args:
            key (str): The key for the item to be cached.
            item (str): The value to be cached.
        If key or item is None, do nothing.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

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
