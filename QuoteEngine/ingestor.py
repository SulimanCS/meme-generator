from abc import ABC, abstractmethod

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

