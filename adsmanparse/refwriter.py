"""
reference writer
"""
import os

from adsputils import load_config

# import exceptions?

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
config = load_config(proj_home=proj_home)


class WriteErrorException(Exception):
    pass


class NoReferencesException(Exception):
    pass


class ReferenceWriter(object):
    def __init__(self):
        self.topdir = config.get("REFERENCE_TOPDIR", "")
        self.refsource = config.get("REFSOURCE_DICT", "")

    def writeref(self, output_metadata, source="iop"):
        if isinstance(output_metadata, dict):
            if output_metadata.get("bibcode", "") and output_metadata("volume", ""):
                bibcode = output_metadata["bibcode"]
                bibstem = bibcode[4:9].rstrip(".")
                volume = str(output_metadata["volume"]).rjust(4, "0")
                file_ext = self.refsource[source]
                reflist = output_metadata["references"]

                # TODO replace with os.join
                outdir = self.topdir + bibstem + "/" + volume
                outfile = outdir + "/" + bibcode + "." + file_ext

                if not os.path.isdir(outdir):
                    os.makedirs(outdir)
                with open(outfile, "w") as fw:
                    fw.write("<ADSBIBCODE>%s</ADSBIBCODE>\n" % bibcode)
                    for s in reflist:
                        fw.write(str(s) + "\n")
            # else:
            # raise bibcode not found error
        return
