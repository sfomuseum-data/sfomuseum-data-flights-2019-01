OS := $(shell uname -s | tr '[:upper:]' '[:lower:]')

# metafiles:
# 	utils/$(OS)/wof-build-metafiles -out meta .

export:
	python utils/python/export.py -r .

prune:
	git gc --aggressive --prune

rm-empty:
	find data -type d -empty -print -delete

scrub: rm-empty prune

count:
	find data -name '*.geojson' -print | wc -l

stats:
	if test ! -d docs/stats; then mkdir -p docs/stats; fi
	utils/$(OS)/wof-stats-counts -pretty -custom 'properties.sfomuseum:placetype' -out docs/stats/counts.json ./
	utils/$(OS)/wof-stats-du -pretty > docs/stats/diskusage.json ./
