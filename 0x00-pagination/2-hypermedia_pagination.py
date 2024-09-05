#!/usr/bin/env python3
"""Hypermedia pagination"""
import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    The function returns a tuple of size two containing a start index
    and an end index corresponding to the range of indexes
    """
    return ((page - 1) * page_size), (page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """get_page function"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        if start_index >= len(self.dataset()):
            return []

        return self.__dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Function that returns a dict containing some key-value pairs"""
        data = self.get_page(page, page_size)
        start_index, end_index = index_range(page, page_size)

        return {
            'page_size': page_size if len(data) != 0 else 0,
            'page': page,
            'data': data,
            'next_page': page + 1 if end_index < len(self.dataset()) else None,
            'prev_page': page - 1 if start_index > 0 else None,
            'total_pages': math.ceil(len(self.dataset()) / page_size)
        }
