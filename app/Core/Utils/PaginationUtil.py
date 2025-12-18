class PaginationUtil:

    @staticmethod
    def GetOffset(page: int, page_size: int) -> int:
        page = max(page, 1)
        page_size = min(max(page_size, 1), 100)
        return (page - 1) * page_size
