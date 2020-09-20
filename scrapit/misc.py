from bs4 import BeautifulSoup as OldBeautifulSoup


class BeautifulSoup(OldBeautifulSoup):
    def __getitem__(self, key):
        """
        Basically, text is thought of as an attribute.
        tag[text] -> tag.text.strip()
        """
        if key == 'text':
            return self.text.strip()

        return super().__getitem__(key)
