M3UFILE=examples/TVPACKET2.m3u
XMLTV_MATCH=tvguide.json
OUTDIR=/tmp/tvheadend

.PHONY: import clean

import: clean
	mkdir -p $(OUTDIR)
	./tvheadend.py $(M3UFILE) $(XMLTV_MATCH) $(OUTDIR)

clean:
	rm -fr $(OUTDIR)

# vim: set noexpandtab
