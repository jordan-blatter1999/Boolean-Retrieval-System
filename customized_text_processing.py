from typing import Set, List
import re
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords


class CustomizedTextProcessing:
    def __init__(self, *args, **kwargs):
        """
        the default TextProcessing class uses Porter stemmer and stopwords list from nltk to process tokens.
        in the Python class, please include at least one other approach for each of the following:
        - to identify a list of terms that should also be ignored along with stopwords
        - to normalize tokens other than stemming and lemmatization

        Your implementation should be in this class. Create more helper functions as you needed. Your approaches could
        be based on heuristics, the usage of a tool from nltk or some new feature you implemented using Python. Be creative!

        # TODO:
        :param args:
        :param kwargs:
        """
        # use list of stop words in addition to converting basic digits to alphabetized versions
        self.STOP_WORDS = set(stopwords.words('english'))
        self.num_dict = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
                         '8': 'eight', '9': 'nine', '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen',
                         '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', '17': 'seventeen', '18': 'eighteen',
                         '19': 'nineteen', '20': 'twenty', '30': 'thirty', '40': 'forty', '50': 'fifty', '60': 'sixty',
                         '70': 'seventy', '80': 'eighty', '90': 'ninety', '100': 'hundred', '0': 'zero'}

    @classmethod
    def from_customized(cls, stop_words: List[str] = stopwords.words("english"), *args, **kwargs) \
            -> "CustomizedTextProcessing":
        """
        You don't necessarily need to implement a class method, but if you do, please use this boilerplate.
        :param stop_words:
        :param args:
        :param kwargs:
        :return:
        """
        return cls(set(stop_words))

    def normalize(self, token: str) -> str:
        """
        your approach to normalize a token. You can still adopt the criterion and methods from TextProcessing along with your own approaches
        :param token:
        :return:
        """
        # TODO:
        # remnove non alphanumeric chars
        token = token.lower()
        normal_token = re.sub(r'[^a-zA-Z0-9\-]', '', token)

        # normalize basic digits
        if normal_token in self.num_dict:
            normal_token = self.num_dict[normal_token]

        # remove stopwords and all prepositions (PP) and particles (RB)
        if normal_token in self.STOP_WORDS or len(normal_token) <= 1 or normal_token.endswith("RB") or \
                normal_token.endswith("PP"):
            return ""
        else:
            return normal_token

    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        :param title:
        :param content:
        :return:
        """
        # TODO:
        # the customized text processing class adds part of speech tags to the tokens using pos_tag()
        tags_and_pos = []
        if title is not None:
            tags_and_pos.extend(pos_tag(word_tokenize(title)))
        if content is not None:
            tags_and_pos.extend(pos_tag(word_tokenize(content)))

        token_tags = set()

        # concatenate POS tag to token
        for token_and_tag in tags_and_pos:
            normalized = self.normalize(token_and_tag[0])
            if normalized != "":
                concat = normalized + '_' + token_and_tag[1]
                token_tags.add(concat)

        return token_tags


if __name__ == "__main__":
    custom = CustomizedTextProcessing.from_customized()
    print(custom.get_normalized_tokens('As homicides fall in D.C., rise in Prince George’s, '
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
