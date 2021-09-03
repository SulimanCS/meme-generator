from abc import ABC, abstractmethod
from quote import QuoteModel
import docx

class IngestorInterface(ABC):
    """A general interface for an ingestor."""

    @staticmethod
    def ingest_line(line) -> QuoteModel:
        """Make a QuoteModel out of a line in an external file.

        :param line: A line from an external file.
        :return: QuoteModel object.
        """
        quote = line.split("-")
        body = quote[0].strip()
        author = quote[1].strip()
        return QuoteModel(body, author)

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Get if a given file can be ingested by current instance.

        :param path: A path for the file to check if it can be ingested.
        :return: Whether if the file can by ingested or not by the passed in isntance.
        """
        file_type = path.split(".")[-1]
        return cls.ingestor_type == file_type

    @abstractmethod
    def parse(cls, path: str) -> list:
        """Parse a file to get a list of quote models.

        :param path: a path for the file to be ingested.
        :return: a list of `quotemodels`.
        """
        pass


class TextIngestor(IngestorInterface):
    """A text file type ingestor.

    Text ingestor implements a parser to extract quotes from .txt files
    """

    ingestor_type = "txt"

    def parse(self, path: str) -> list[QuoteModel]:
        """Parse a file to get a list of quote models.

        :param path: a path for the file to be ingested.
        :return: a list of `quotemodels`.
        """
        quote_models = []
        if self.can_ingest(path):
            try:
                # utf-8-sig encoding fixes a weird where
                # letters would be read as symbols
                with open(path, "r", encoding="utf-8-sig") as f:
                    lines = f.readlines()
                    for line in lines:
                        quote_models.append(self.ingest_line(line))
            except FileNotFoundError as e:
                print(e)
                return []
            return quote_models
        print(f"{self.__class__.__name__} object can't ingest {path}")
        return []

class DocxIngestor(IngestorInterface):
    """A docx file type ingestor.

    Docx ingestor implements a parser to extract quotes from .docx files
    """

    ingestor_type = "docx"

    def parse(self, path: str) -> list[QuoteModel]:
        """Parse a file to get a list of quote models.

        :param path: a path for the file to be ingested.
        :return: a list of `quotemodels`.
        """
        quote_models = []
        if self.can_ingest(path):
            try:
                doc = docx.Document(path)
                for line in doc.paragraphs:
                    if len(line.text) == 0:
                        continue
                    quote_models.append(self.ingest_line(line.text))
            except docx.opc.exceptions.PackageNotFoundError as e:
                print(e)
                return []
            return quote_models
        print(f"{self.__class__.__name__} object can't ingest {path}")
        return []

if __name__ == "__main__":
    # import os
    # print('\n\n')
    # print(os.getcwd())
    # manual testing for TextIngestor
    test = TextIngestor()
    print(test.can_ingest("grger.blah"))
    print(test.can_ingest("_data/DogQuotes/DogQuotesTXT.txt"))
    quote_models = test.parse("_data/DogQuotes/DogQuotesTXT.txt")
    print(quote_models)

    # manual testing for DocxIngestor
    test = DocxIngestor()
    print(test.can_ingest("grger.blah"))
    print(test.can_ingest("_data/DogQuotes/DogQuotesDOCX.docx"))
    quote_models = test.parse("_data/DogQuotes/DogQuotesDOCX.docx")
    print(quote_models)
