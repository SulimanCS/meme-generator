"""Represent different ingestors for different file types."""
from abc import ABC, abstractmethod

# for some reason from quote import QuoteModel does not work
# in meme.py, this is why the conditional is needed
# and `from QuoteEngine.quote import QuoteModel` does not work
# when executing this file alone.
# any help with understanding why is this the case would be
# appreciated
if __name__ == "__main__":
    from quote import QuoteModel
else:
    from QuoteEngine.quote import QuoteModel
import pandas as pd
import subprocess
import docx
import os.path


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
        return os.path.isfile(path) and cls.ingestor_type == file_type

    @abstractmethod
    def parse(cls, path: str) -> list:
        """Parse a txt file to get a list of quote models.

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
        """Parse a docx file to get a list of quote models.

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


class PDFIngestor(IngestorInterface):
    """A pdf file type ingestor.

    Pdf ingestor implements a parser to extract quotes from .pdf files
    """

    ingestor_type = "pdf"

    def parse(self, path: str) -> list[QuoteModel]:
        """Parse a pdf file to get a list of quote models.

        :param path: a path for the file to be ingested.
        :return: a list of `quotemodels`.
        """
        quote_models = []
        if self.can_ingest(path):
            try:
                # the '-' flag outputs the text of a pdf file
                # to stdout, this way I don't have to handle removing
                # temp files since none were created
                p = subprocess.run(
                    ["./pdftotext.exe", "-layout", path, "-"], stdout=subprocess.PIPE
                )
                output = p.stdout.decode("utf-8")
                output_lines = output.split("\n")[:-1]
                for line in output_lines:
                    quote_models.append(self.ingest_line(line))
            except FileNotFoundError as e:
                print(e)
                return []
            return quote_models
        return []


class CSVIngestor(IngestorInterface):
    """A csv file type ingestor.

    csv ingestor implements a parser to extract quotes from .csv files
    """

    ingestor_type = "csv"

    def parse(self, path: str) -> list[QuoteModel]:
        """Parse a pdf file to get a list of quote models.

        :param path: a path for the file to be ingested.
        :return: a list of `quotemodels`.
        """
        quote_models = []
        if self.can_ingest(path):
            try:
                df = pd.read_csv(path)
                for row in df.itertuples():
                    quote_models.append(QuoteModel(row.body, row.author))
            except FileNotFoundError as e:
                print(e)
                return []
            return quote_models
        return []


class Ingestor(IngestorInterface):
    """A general ingestor.

    ingestor encapsulates all kinds of ingestors and selects the
    appropriate one based on the file type
    """

    def __init__(self):
        """Create a new `Ingestor`.

        initializes a single instance of all different kind of ingestors
        and saves them into an ingestors list
        """
        pass

    @staticmethod
    def parse(path: str) -> list[QuoteModel]:
        """Parse a pdf file to get a list of quote models.

        :param path: a path for the file to be ingested.
        :return: a list of `quotemodels`.
        """
        ingestors = [TextIngestor(), DocxIngestor(), PDFIngestor(), CSVIngestor()]
        for ingestor in ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
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

    # manual testing for PDFIngestor
    test = PDFIngestor()
    quote_models = test.parse("_data/DogQuotes/DogQuotesPDFho.pdf")
    quote_models = test.parse("_data/DogQuotes/DogQuotesDOCX.docx")
    quote_models = test.parse("_data/DogQuotes/DogQuotesPDF.pdf")
    print(quote_models)

    # manual testing for CSVIngestor
    test = CSVIngestor()
    quote_models = test.parse("_data/DogQuotes/DogQuotesPDFho.pdf")
    quote_models = test.parse("_data/DogQuotes/DogQuotesDOCX.docx")
    quote_models = test.parse("_data/DogQuotes/DogQuotesCSV.csv")
    print(quote_models)

    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]
    test = Ingestor()
    all_quotes = []
    for quote_file in quote_files:
        all_quotes.extend(test.parse(quote_file))
    print(all_quotes)
    print(len(all_quotes))
