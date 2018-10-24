#!/usr/bin/env python

import logging
import zipfile

from pyclowder.extractors import Extractor
from pyclowder.utils import CheckMessage
from pyclowder.files import upload_to_dataset


class ZipContentsExtractor(Extractor):
    def __init__(self):
        Extractor.__init__(self)

        # add any additional arguments to parser
        # self.parser.add_argument('--max', '-m', type=int, nargs='?', default=-1,
        #                          help='maximum number (default=-1)')

        # parse command line and load default logging configuration
        self.setup()

        # setup logging for the exctractor
        logging.getLogger('pyclowder').setLevel(logging.DEBUG)
        logging.getLogger('__main__').setLevel(logging.DEBUG)

    def check_message(self, connector, host, secret_key, resource, parameters):
        return CheckMessage.bypass

    def process_message(self, connector, host, secret_key, resource, parameters):
        zip = resource['local_paths'][0]
        zipname = resource['name'].replace(".zip", "")

        # Create folder with name of zipfile
        url = '%sapi/datasets/%s/newFolder?key=%s' % (host, resource["parent"]["id"], secret_key)
        folderid = connector.post(url, data={"name": zipname}, verify=connector.ssl_verify if connector else True)

        # Extract files into new folder
        zf = zipfile.ZipFile(zip)
        contents = zf.namelist()
        for filename in contents:
            zf.extract(filename)
            if not filename.endswith("/"):
                fileid = upload_to_dataset(connector, host, secret_key, resource["parent"]["id"], filename)
                url = '%sapi/datasets/%s/movefolder/%s/%s?key=%s' % (host, resource["parent"]["id"], folderid, fileid, secret_key)
                connector.post(url)

if __name__ == "__main__":
    extractor = ZipContentsExtractor()
    extractor.start()
