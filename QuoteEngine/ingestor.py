from abc import ABC, abstractmethod
from quote import QuoteModel

# TODO: docstring, pep8 pep 257
# TODO: __str__
# TODO: __repr__
class IngestorInterface(ABC):
    """A general interface for an ingestor."""

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
                        quote = line.split("-")
                        body = quote[0].strip()
                        author = quote[1].strip()
                        quote_model = QuoteModel(body, author)
                        quote_models.append(quote_model)

            except FileNotFoundError as e:
                print(e)
                return []
            return quote_models
        print(f"{self.__class__.__name__} object can't ingest {path}")
        return []


if __name__ == "__main__":
    test = TextIngestor()
    print(test.can_ingest("grger.txt"))
    print(test.can_ingest("_data/DogQuotesTXT.few"))
    quote_models = test.parse("_data/DogQuotes/DogQuotesTXT.txt")
    pass
