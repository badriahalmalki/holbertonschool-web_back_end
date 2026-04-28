#!/usr/bin/env python3 
def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
            Get the hyper index

            Args:
                index: Current page
                page_size: Total size of the page

            Return:
                Hyper index
        """
        assert index is not None and index >= 0

        indexed_data = self.indexed_dataset()
        max_index = max(indexed_data.keys())

        assert index <= max_index

        data = []
        current_index = index

        while len(data) < page_size and current_index <= max_index:
            if current_index in indexed_data:
                data.append(indexed_data[current_index])
            current_index += 1

        return {
            "index": index,
            "next_index": current_index,
            "page_size": len(data),
            "data": data
        }

#!/usr/bin/env python3
"""
This module provides a Server class that implements deletion-resilient
hypermedia pagination on a dataset of popular baby names.
"""

import csv
from typing import List, Dict


class Server:
    """
    Server class that loads, indexes, and paginates a dataset of baby names.

    It supports deletion-resilient pagination using an indexed dataset,
    ensuring stable pagination even when entries are removed.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self) -> None:
        """Initializes the Server with cached dataset attributes."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Loads and caches the dataset from a CSV file.

        Returns:
            List[List]: The dataset without the header row.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Creates and caches a dataset indexed by position.

        Returns:
            Dict[int, List]: A dictionary mapping index to dataset row.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: truncated_dataset[i]
                for i in range(len(truncated_dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(
        self, index: int = None, page_size: int = 10
    ) -> Dict:
        """
        Returns a deletion-resilient paginated response starting from a given index.

        This method retrieves a page of data of size `page_size` starting from
        `index`, skipping any missing entries in the indexed dataset to ensure
        consistency even if rows have been deleted between queries.

        Args:
            index (int): The starting index of the page.
            page_size (int): The number of items per page.

        Returns:
            Dict: A dictionary containing the current index, next index,
                  page size, and the page data.
        """
        assert isinstance(index, int) and index >= 0

        indexed_data = self.indexed_dataset()
        max_index = max(indexed_data.keys())

        assert index <= max_index

        data = []
        current_index = index

        while len(data) < page_size and current_index <= max_index:
            if current_index in indexed_data:
                data.append(indexed_data[current_index])
            current_index += 1

        return {
            "index": index,
            "next_index": current_index,
            "page_size": len(data),
            "data": data,
        }
