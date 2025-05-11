from beanie import Document

from logmaster.server.core.models.dto import PageInput
from logmaster.server.core.models.page import Page
from logmaster.server.core.models.resource import Resource


async def paginate(page: PageInput, document_class: type[Document], page_class: type[Page], resource_class: type[Resource]) -> Page:
    search_criteria = page.get_filter().get_criteria() if page.get_filter() is not None else ()
    sort = page.get_sort().get_sort() if page.get_sort() is not None else ["-_id"]
    offset = page.get_offset()
    content: list = await document_class.find(*search_criteria).sort(*sort).skip(offset).limit(page.page_size).to_list()
    total_items: int = await document_class.find(*search_criteria).count()
    return page_class(
        content=[resource_class.from_model(document) for document in content],
        page_number=page.page_number,
        page_size=page.page_size,
        total_items=total_items,
        total_pages=total_items//page.page_size+1
    )
