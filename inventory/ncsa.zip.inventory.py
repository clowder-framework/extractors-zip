#!/usr/bin/env python

import logging
import zipfile

from pyclowder.extractors import Extractor
from pyclowder.utils import CheckMessage
from pyclowder.files import upload_metadata


class ZipInventory(Extractor):
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
        return CheckMessage.download

    def process_message(self, connector, host, secret_key, resource, parameters):
        zip = resource['local_paths'][0]

        zf = zipfile.ZipFile(zip)
        contents = zf.namelist()

        md = {
            "@context": ["https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld"],
            "content": {
                "inventory size": len(contents),
                "inventory": contents
            },
            "agent": {
                "@type": "cat:extractor",
                "extractor_id": host + ("" if host.endswith("/") else "/") + "api/extractors/"+ self.extractor_info['name']
            }
        }

        upload_metadata(connector, host, secret_key, resource['id'], md)

if __name__ == "__main__":
    extractor = ZipInventory()
    extractor.start()
