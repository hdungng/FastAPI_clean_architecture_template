class PaginationUtil:
    MAX_PAGE_SIZE = 100

    @staticmethod
    def Normalize(page: int, page_size: int) -> tuple[int, int, int]:
        page = max(page, 1)
        page_size = min(max(page_size, 1), PaginationUtil.MAX_PAGE_SIZE)
        return page, page_size, (page - 1) * page_size

    @staticmethod
    def GetOffset(page: int, page_size: int) -> int:
        _, _, offset = PaginationUtil.Normalize(page, page_size)
        return offset
