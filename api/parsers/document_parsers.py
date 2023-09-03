from typing import Callable

from fastapi import UploadFile
from langchain.schema import Document
import fitz

from langchain.text_splitter import TokenTextSplitter


class Parser:
    @staticmethod
    def get_instance(file: UploadFile) -> "Parser":
        """
        get instance based on the file type.
        sometimes you need to do more than file type for the right
        kind of parser to be returned.
        """
        if file.content_type == "application/pdf":
            return PdfParser()
        elif "text" in file.content_type:
            return TextParser()
        else:
            raise ValueError("Unsupported file type")

    def __init__(self):
        self.splitter = TokenTextSplitter(chunk_size=3000, chunk_overlap=0)

    def _parse_text(self, supplier: Callable[[], bytes], name: str) -> list[Document]:
        content = supplier()
        pages = self.splitter.split_text(str(content))
        
        return [
            Document(page_content=page, metadata={"file": name, "page": i + 1})
            for i, page in enumerate(pages)
        ]

    async def parse(self, file: UploadFile, name: str) -> list[Document]:
        """
        parse and return a list of documents
        """
        content = await file.read()
        return self._parse_text(lambda: content, name)


class TextParser(Parser):
    pass

class PdfParser(Parser):
    async def parse(self, file: UploadFile, name: str) -> list[Document]:
        doc = fitz.open(stream = await file.read())
        return super()._parse_text(
            lambda: "".join([page.get_text() for page in doc]), name 
        )
