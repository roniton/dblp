# -*- coding: utf-8 -*-
from lxml import etree
import os, sys
from unidecode import unidecode


def fastIter(context, func,*args, **kwargs):
    #xml categories
    #collaborations = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']
    collaborations = [u'article']
    
    #xml elements
    title = ''
    journal = ''
    year = ''

    # read chunk line by line
    # we focus title and journal and year
    for event, elem in context:
        if elem.tag == 'title':
            if elem.text:
                title = unidecode(elem.text)

        if elem.tag == 'journal':
            if elem.text:
                journal = unidecode(elem.text)

        if elem.tag == 'year':
            if elem.text:
                year = unidecode(elem.text)

        if elem.tag in collaborations:
            if title is not '':
                func('"'+title+'";"'+journal+'";"'+year+'"', *args, **kwargs)

            title = ''
            journal = ''
            year = ''
 
        elem.clear()
        while elem.getprevious() is not None:
            if elem.getparent() is not None:
                del elem.getparent()[0]
            else:
                break
    del context

def processElement(elem, fout):
    print(elem, end="\n", file=fout)

if __name__ == "__main__":
    fout = open('parsed_dblp.csv', 'w')
    context = etree.iterparse('dblp.xml', load_dtd=True,html=True)
    fastIter(context, processElement, fout)