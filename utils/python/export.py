#!/usr/bin/env python

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.export

import os
import logging

if __name__ == "__main__":

    import optparse
    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-r', '--root', dest='root', action='store', default='.', help='...')        

    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')
    options, args = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    root = os.path.abspath(options.root)
    data = os.path.join(root, "data")

    exporter = mapzen.whosonfirst.export.flatfile(data)

    crawl = mapzen.whosonfirst.utils.crawl(data, inflate=True)

    for feature in crawl:
        
        feature["properties"]["edtf:inception"] = "uuuu"
        feature["properties"]["edtf:cessation"] = "uuuu"

        date = feature["properties"]["flysfo:date"]
        ymd = date.split("-")
        
        if feature["properties"]["flysfo:event"] == "departure":
            feature["properties"]["edtf:inception"] = date
        else:
            feature["properties"]["edtf:cessation"] = date
            
        feature["properties"]["wof:repo"] = "sfomuseum-data-flight-%s-%s" % (ymd[0], ymd[1])
        exporter.export_feature(feature)
