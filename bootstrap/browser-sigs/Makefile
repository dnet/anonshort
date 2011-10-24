all: $(shell ls *.bin | sed s/bin/tpl/)

%.tpl: %.bin
	sh firstblank.sh <$< | sed -f transform.sed >$@

clean:
	rm -f *.tpl

.PHONY: clean all
