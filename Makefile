M3UFILE=examples/TVPACKET2.m3u
OUTDIR=tvheadend

.PHONY: import clean

import: clean
	mkdir -p $(OUTDIR)
	./tvheadend.py $(M3UFILE) $(OUTDIR)

clean:
	rm -fr $(OUTDIR)

# vim: set noexpandtab
