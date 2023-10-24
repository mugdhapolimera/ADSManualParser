"""
example refwriter
"""
import os
import pdb
from glob import glob

from adsingestp.parsers.jats import JATSParser
from pyingest.serializers.classic import Tagged

#!/usr/bin/env python
from adsmanparse.refwriter import ReferenceWriter

outfile = "iop_test.tag"

"""
journal_ISSN = {
    '1538-3881': 'AJ',
    '0004-6256': 'AJ',
    '1475-7516': 'JCAP',
    '0004-637X': 'ApJ',
    '1538-4357': 'ApJ',
    '0067-0049': 'ApJS',
    '2041-8205': 'ApJ',
    '1538-4357': 'ApJL',
    '2041-8205': 'ApJL',
    '2515-5172': 'RNAAS'
}
"""
stacks_bibstems = ["AJ", "JCAP", "ApJ", "ApJS", "ApJL", "RNAAS"]

parser = JATSParser()

basedir = "./"  #'/proj/ads/articles/fulltext/sources/'

for bs in stacks_bibstems:
    b2 = basedir + bs
    vols = glob(b2 + "/*")
    i = -1
    pdb.set_trace()
    v = vols[i]
    while not os.path.isdir(v):
        i = i - 1
        v = vols[i]

    papers = glob(v + "/*.xml")
    print("VEE:", v)

    # Try the parser
    documents = []
    for p in papers:
        try:
            with open(p, "rU") as fp:
                doc = parser.parse(fp)
            documents.append(doc)
        except Exception as e:
            print("Error in IOP parser:", p, e)

    # Write everything out in Classic tagged format
    fo = open(outfile, "a")

    serializer = Tagged()
    refwriter = ReferenceWriter()
    refwriter.refsource = ".jats.iopft.xml"

    for d in documents:
        serializer.write(d, fo)
        try:
            refwriter.writeref(d)
        except Exception as err:
            print("Error in refwriter: %s" % err)
    fo.close()
