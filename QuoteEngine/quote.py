"""Represent models quotes."""


class QuoteModel:
    """A quote model that houses the body and author."""

    def __init__(self, body, author):
        """Create a new `QuoteModel`.

        :param body: The body of the quote model
        :param author: The author of the quote model
        """
        self.body = body
        self.author = author

    def __str__(self):
        """Return `str(self)`."""
        return f'"{self.body}" - {self.author}'

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"QuoteModel(body={self.body!r}, author={self.author!r})"


if __name__ == "__main__":
    body = "Chase the mailman"
    author = "Skittle"
    quote = QuoteModel(body, author)
