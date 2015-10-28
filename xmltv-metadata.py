# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import xml.etree.ElementTree as ET
import re
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', required = True)
    parser.add_argument('-o', '--outputfile', default='-')
    args = parser.parse_args()
    inputfilename = args.inputfile
    outputfilename = args.outputfile

    tree = ET.parse(inputfilename)
    root = tree.getroot()

    patterns = ['(?P<name>.+)\. Жанр: (?P<category>[^.]+)\. Рейтинг: (?P<rating>\d+)\. (?P<country>[^,]+), (?P<date>\d{4}-\d{4}|\d{4}-?)\. (?P<desc>.+)',
               '(?P<name>.+)\. Жанр: (?P<category>[^.]+)\. (?P<country>[^,]+), (?P<date>\d{4}-\d{4}|\d{4}-?)\. (?P<desc>.+)',
               '(?P<name>.+)\. Рейтинг: (?P<rating>\d+)\. (?P<country>[^,]+), (?P<date>\d{4}-\d{4}|\d{4}-?)\. (?P<desc>.+)',
               '(?P<name>.+)\. Жанр: (?P<category>[^.]+)\. (?P<country>[^,]+). (?P<desc>.+)',
               '(?P<name>.+)\. (?P<country>[^,]+), (?P<date>\d{4}-\d{4}|\d{4}-?)[.,] (?P<desc>.+)']

    for programme in root.iter('programme'):
        title = programme.find('title')
        title_value = title.text.encode('UTF-8')
        for i in range(0, len(patterns)):
            if re.match(patterns[i], title_value):
                m = re.match(patterns[i], title_value)
                name_value = m.group('name')

                description_value = m.group('desc')
                description = ET.SubElement(programme, 'desc')
                description.text = description_value.encode('UTF-8')

                country_value = m.group('country')
                country = ET.SubElement(programme, 'country')
                country.text = country_value.encode('UTF-8')

                try:
                    category_value = m.group('category')
                    category = ET.SubElement(programme, 'category')
                    category.text = category_value.encode('UTF-8')
                except:
                    pass

                try:
                    rating_value = m.group('rating')
                    rating = ET.SubElement(programme, 'rating')
                    rating.text = rating_value.encode('UTF-8')
                except:
                    pass

                title.text = name_value.encode('UTF-8')
                break

            # If title length larger than filesystem maximum file name size then tvheadend failed to record show
            if len(title.text) > 150:
                title.text = title.text[0:140]

    if outputfilename == "-":
        print ET.tostring(root, encoding="UTF-8", method="xml")
    else:
        tree.write(outputfilename, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()
