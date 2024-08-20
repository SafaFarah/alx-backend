#!/usr/bin/python3
"""class that inherits from BaseCaching and implements LIFO caching."""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO caching system."""

    def __init__(self):
        """Initialize LIFOCache."""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Assign value to the cache dictionary using LIFO algorithm.
        Args:
            key (str): The key for the item to be cached.
            item (str): The value to be cached.
        If key or item is None, do nothing.
        If the items exceeds MAX_ITEMS, discard the most recently added item.
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                last_key = self.order.pop()
                del self.cache_data[last_key]
                print(f"DISCARD: {last_key}")
            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """Retrieve the value from the cache dictionary.
        Args:
            key (str): The key of the item to retrieve.
        Returns:
            str: cached value of key,None if key is None or not found.
        """
        if key is None or key not in self.cache_data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
