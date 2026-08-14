# -*- coding: utf-8 -*-
# Extractor for CET-4/6 word list
# 5418 + 2551 = 7969

import re

class Ex_CET:

    cet_6_line_prefix = '★'
    words_split = ' '

    cet_4_word_list = []
    cet_6_word_list = []

    def __init__(self, path, cet_4_filename, cet_6_filename):
        lines = self.read(path)
        self.classify(lines)
        
        self.write(sorted(list(set(self.cet_4_word_list))), cet_4_filename)
        self.write(sorted(list(set(self.cet_6_word_list))), cet_6_filename)

    def read(self, path):
        lines = []
        with open(path, 'r') as file:
            for line in file.readlines():
                if self.is_meaningful_string(line.strip()):
                    lines.append(line.strip())
        return lines

    def write(self, content, filename):
        with open(filename, 'w') as file:
            for cnt in content:
                file.write(cnt + '\n')

    def classify(self, lines):
        word_regex = '[a-zA-Z]+'

        for line in lines:
            if self.cet_6_line_prefix in line:
                word = re.findall(word_regex, line)
                if len(word) > 0:
                    self.cet_6_word_list += word
            else:
                word = re.findall(word_regex, line)
                if len(word) > 0:
                    self.cet_4_word_list += word

    def is_meaningful_string(self, string):
        return string != '' and string != '\n' and string != '\r'

if __name__ == '__main__':
    extractor = Ex_CET('source_file.txt', 'cet4_wl.md', 'cet6_wl.md')