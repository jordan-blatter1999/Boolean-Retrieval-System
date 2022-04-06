import re
from typing import Set, Any, List

from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem.porter import PorterStemmer  # type: ignore
from nltk.corpus import stopwords  # type: ignore


class TextProcessing:
    def __init__(self, stemmer, stop_words, *args):
        """
        class TextProcessing is used to tokenize and normalize tokens that will be further used to build inverted index.
        :param stemmer:
        :param stop_words:
        :param args:
        """
        self.stemmer = stemmer
        self.STOP_WORDS = stop_words

    @classmethod
    def from_nltk(
            cls,
            stemmer: Any = PorterStemmer().stem,
            stop_words: List[str] = stopwords.words("english"),
    ) -> "TextProcessing":
        """
        initialize from nltk
        :param stemmer:
        :param stop_words:
        :return:
        """
        return cls(stemmer, set(stop_words))

    def normalize(self, token: str) -> str:
        """
        normalize the token based on:
        1. make all characters in the token to lower case
        2. remove any characters from the token other than alphanumeric characters and dash ("-")
        3. after step 1, if the processed token appears in the stop words list or its length is 1, return an empty string
        4. after step 1, if the processed token is NOT in the stop words list and its length is greater than 1, return the stem of the token
        :param token:
        :return:
        """
        # TODO:
        # lower case, remove non alphanumeric, remove stopwords
        token = token.lower()
        normal_token = re.sub(r'[^a-zA-Z0-9\-]', '', token)
        if normal_token in self.STOP_WORDS or len(token) <= 1:
            return ""
        else:
            return TextProcessing.from_nltk().stemmer(normal_token)

    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        you may want to apply word_tokenize first to get un-normalized tokens first
        :param title:
        :param content:
        :return:
        """
        # TODO:
        token_set = set()
        # tokenize input strings and normalize tokens, make a set
        if title is not None:
            for token in word_tokenize(title):
                token_set.add(self.normalize(token))
        if content is not None:
            for token in word_tokenize(content):
                token_set.add(self.normalize(token))
        if "" in token_set:
            token_set.remove("")
        return token_set


if __name__ == "__main__":
    tp = TextProcessing.from_nltk()
    print(tp.get_normalized_tokens('As homicides fall in D.C., rise in Prince George’s, '
                                   'numbers meet in '
                                   'the middle', 'Correction: An earlier version of this article '
                                                 'misstated the Prince George’s County Police '
                                                 'Department’s homicide closure rate for 2011. The rate '
                                                 'was 66 percent, not 63\xa0percent. In addition, '
                                                 'because of incomplete information provided by Fairfax '
                                                 'County police, the article and an accompanying graphic '
                                                 'misstated the number of homicides in that county. There '
                                                 'were 11, not eight. The number for Prince William '
                                                 'County was also incorrect; it included two cases that '
                                                 'were ruled justified. That county had four criminal '
                                                 'homicides, according to police, not six. And D.C. '
                                                 'police say that one of the 109 homicides recorded in '
                                                 'the city in 2011 will be considered a 2012 case because '
                                                 'the medical examiner did not issue a ruling until Jan. '
                                                 '1. This version has been corrected. The District and '
                                                 'Prince George’s County had nearly the same number of '
                                                 'homicides in 2011, a major departure from a high 20 '
                                                 'years ago, when the city saw 325 more slayings than the '
                                                 'county. It is a shift that reflects a double-digit drop '
                                                 'in killings in the District from 2010 to 2011, '
                                                 'with an especially noticeable downward trend in the '
                                                 'most stubborn crime zones east of the Anacostia River. '
                                                 'Just across the border, though, the homicide count in '
                                                 'the neighboring communities in Prince George’s is '
                                                 'surging, and the county as a whole saw a slight '
                                                 'increase last year. There were 97 slayings in Prince '
                                                 'George’s in 2011, four more killings than in 2010. In '
                                                 'the District, the year saw 108 homicides, down from 132 '
                                                 'in 2010 and the lowest homicide total in the city since '
                                                 '1963. “We share many of the same issues,” said D.C. '
                                                 'Police Chief Cathy L. Lanier. “Quite a few of our '
                                                 'victims come from Prince George’s County.” The police '
                                                 'department’s 7th District east of the Anacostia River — '
                                                 'neighborhoods including Barry Farm and Congress Heights '
                                                 '— saw its annual homicide count drop'))
