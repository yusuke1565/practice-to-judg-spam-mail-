import sys
import MeCab

args = sys.argv
mecab = MeCab.Tagger("-Owakati")

class Mail:
    """
    Mail is label of mail and content.
    """
    def __init__(self, line):
        """
        Go to label and content.
        :param line: 1 line.
        """
        l, c = self.parse(line)
        self.label = l
        self.content = c
        self.words = None

    # ------------------------------------#
    def parse(self, line, delimiter = ','):
        """
        Parse mail to label and content.
        :param line: 1 line of mail.
        :param delimiter: Delimiter of label and content.
        :return: Label and content.
        """
        label, content = line.split(delimiter)
        return label, content

    def get_lable(self):
        return self.label

    def parse_content(self):
        self.words = mecab.parse(self.get_content())

    def get_content(self):
        return self.content

    def get_words(self):
        if self.words == None:
            self.parse_content()

        return self.words


class Dic_for_freq:
    """
    This class make dictionary for frequency and set data, and output it.
    """
    def __init__(self, list = []):
        """
        Define dictionary(key2frequency) and go 'set data'.
        :param list(list): Real or char.
        """
        self.k2f = {}
        self.set_data(list)

    # ---------------------------------#
    def set_data(self, list=[]):
        """
        Set data in k2f.
        :param list(list): Real or char.
        """
        for n in self.list:
            self.k2f[n] = self.k2f.get(n, 0) +1

    def get_dic(self):
        """
        Return k2f.
        :return: Dictionary for frequency.
        """
        return self.k2f


class Second_dimention_dic_for_freq:
    """
    This class make second dimention dictionary for frequency.
    """
    def __init__(self, closing = None, key2freq = {}):
        """
        Define dictionary(closing2key2frequency) and go 'set data'.
        :param closing(real or char): Close somethings.
                                      Example, label or category.
        :param key2freq(dictionary): Dictionary for frequency.
        """
        self.c2k2f = {}
        self.set_data(closing, key2freq)

    # -----------------------------------#
    def set_data(self, c=None, k2f={}):
        """
        Set data in c2k2f.
        :param c(real or char): Close something.
        :param k2f(dictionary): Key to frequency.
        """
        if c != None:
            self.c2k2f[c] = self.c2k2f.get(c, {})
            for k in k2f.keys():
                self.c2k2f[c][k] = self.c2k2f[c].get(k, 0) + k2f[k]

    def get_dic(self):
        """
        Return c2k2f.
        :return: Second dimention dictionary for frequency.
        """
        return self.c2k2f


class Dictionary_for_prob:
    """
    This class make dictionary for probability.
    """
    def __init__(self, key2freq = {}):
        """
        Define dictionary(key2probability) and go 'set data'.
        :param key2freq(dictionary): Key to frequency.
        """
        self.k2p = {}
        self.set_data(key2freq)

    # -------------------------------------#
    def set_data(self, k2f = {}):
        """
        Set data in k2p. (probability = frequency / all frequency)
        :param k2f(dictionary): Key to frequency.
        """
        n = 0
        for k in k2f.keys():
            n = n + k2f[k]
        for k in k2f.keys():
            self.k2p[k] = float(k2f[k]) / float(n)

    def get_dic(self):
        """
        Return k2p.
        :return: Dictionary for probability.
        """
        return self.k2p


class Two_dimentions_dic_for_prob:
    def __init__(self, closing2key2freq = {}):
        c2k2f = closing2key2freq
        self.c2k2p = {}
        self.set_data(c2k2f)

    # ----------------------------------------#
    def set_data(self, c2k2f = {}):
        for c in c2k2f.keys():
            self.c2k2p[c] = {}
            for k in c2k2f[c].keys():
                self.c2k2p[c][k] = float(c2k2f[c][k]) / float(len(c2k2f[c]))

    def get_dic(self):
        return self.c2k2p



file = args[1]
labels = []
i=0
with open(file, "r") as f:
    for line in f:
        i = i + 1
        line = line.rstrip()
        mail = Mail(line) #mail is instance of Mail class

        label = mail.get_lable()
        labels.append(label)

        words = mail.get_words()
        w2f = Dic_for_freq(words) #w2f is instance of Dictionary_of_freq class
        w2f = w2f.get_dic()
        del w2f["\n"]

        if i == 1:
            label2w2f = Second_dimention_dic_for_freq(label, w2f)
        else:
            label2w2f.set_data(label, w2f)
        del w2f

label2f = Dic_for_freq(labels)
label2f = label2f.get_dic()

label2w2f = label2w2f.get_dic()

label2p = Dic_for_prob(label2f)
label2p = label2p.get_dic()

label2w2p = Second_dimention_dic_for_prob(label2w2f)
label2w2p = label2w2p.get_dic()

with open("pLabel.txt", "w") as wf1:
    for l in label2p.keys():
        wf1.write(l + " " + str(label2p[l]) + "\n")

with open("pw_Label.txt", "w") as wf2:
    for l in label2w2p.keys():
        for w in label2w2p[l].keys():
            wf2.write(l + " " + w + " " + str(label2w2p[l][w]) + "\n")