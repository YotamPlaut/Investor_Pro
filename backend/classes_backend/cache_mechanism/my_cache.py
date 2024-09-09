from datetime import datetime, timedelta
from backend.classes_backend.stock import Stock


class Node:
    def __init__(self, key, value: Stock):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Dictionary for O(1) lookups
        self.head = Node(0, 0)  # Dummy head
        self.tail = Node(0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node):
        first_node = self.head.next
        node.next = first_node
        node.prev = self.head
        self.head.next = node
        first_node.prev = node

    def _get_last_valid_date(self):
        today = datetime.today()
        return today

    def get(self, key: int):
        if key in self.cache:
            node = self.cache[key]
            last_access_date = node.value.last_access_date
            last_valid_date = self._get_last_valid_date()

            print(f"Checking stock with key {key}")
            print(f"Last date in data: {last_access_date.date()}")
            print(f"Last valid date: {last_valid_date.date()}")

            # Validate if the last date is the correct one
            if last_access_date.date() == last_valid_date.date():
                self._remove(node)
                self._add_to_front(node)
                return node.value
        return -1

    def put(self, key: int, value):
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self._add_to_front(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


def print_cache_contents(cache):
    print("Cache contents:")
    current = cache.head.next
    while current != cache.tail:
        print(f"Key: {current.key}, Last Date in Data: {current.value.price_data[-1]['date']}")
        current = current.next


if __name__ == '__main__':
    # Test Data for Stocks
    stock_data_1 = {
        "Index_Symbol": 1,
        "Symbol_Name": "Stock_A",
        "description": "Description A",
        "num_days": 2,
        "price_data": [
            {"date": (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), "close_price": 100},
            {"date": datetime.today().strftime("%Y-%m-%d"), "close_price": 110}
        ]
    }

    stock_data_2 = {
        "Index_Symbol": 2,
        "Symbol_Name": "Stock_B",
        "description": "Description B",
        "num_days": 2,
        "price_data": [
            {"date": (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"), "close_price": 200},
            {"date": (datetime.today()).strftime("%Y-%m-%d"), "close_price": 210}
        ]
    }

    stock_data_3 = {
        "Index_Symbol": 3,
        "Symbol_Name": "Stock_C",
        "description": "Description C",
        "num_days": 2,
        "price_data": [
            {"date": (datetime.today() - timedelta(days=3)).strftime("%Y-%m-%d"), "close_price": 300},
            {"date": (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"), "close_price": 310}
        ]
    }

    stock_data_4 = {
        "Index_Symbol": 4,
        "Symbol_Name": "Stock_D",
        "description": "Description D",
        "num_days": 2,
        "price_data": [
            {"date": (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d"), "close_price": 400},
            {"date": (datetime.today() - timedelta(days=6)).strftime("%Y-%m-%d"), "close_price": 410}
        ]
    }

    # Initialize LRUCache with capacity 3
    cache = LRUCache(3)

    # Add stocks to the cache
    cache.put(1, Stock(stock_data_1))
    cache.put(2, Stock(stock_data_2))
    cache.put(3, Stock(stock_data_3))

    print_cache_contents(cache)  # Print cache contents to verify

    # Test: Valid retrieval of stock 1 (should be a cache hit)
    assert cache.get(3) == -1, "Test failed: Stock 3 not updated."

    # Test: Invalid retrieval of stock with outdated data (simulate older date)

    cache.put(4, Stock(stock_data_4, 0))
    print_cache_contents(cache)
    assert cache.get(1) == -1, "Test failed: Stock 1 should not be in cache."
    # Test: Stock with outdated data should not be retrieved
    assert cache.get(4) != -1, "Test failed: Stock 4 should be in cache."

    # Test: Validate LRU eviction (stock 2 should be evicted since cache capacity is 3)
    cache.put(1, Stock(stock_data_1, 0))  # This will cause an eviction
    assert cache.get(2) == -1, "Test failed: Stock 2 should have been evicted."

    print("All tests passed!")
