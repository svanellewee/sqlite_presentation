PACKAGE=sqlitetalk
PYTHON?=python3
D3_VERSION=v4.2.5
REVEAL_JS_VERSION=3.3.0
REVEAL_JS_TARBALL=$(REVEAL_JS_VERSION).tar.gz
DOOM_SHAREWARE=doom1.wad  # according to the fan-site https://doomwiki.org/wiki/DOOM1.WAD this is the Legit Shareware version

directories:
	mkdir -p depdir

./depdir/d3.zip: | directories
	wget https://github.com/d3/d3/releases/download/$(D3_VERSION)/d3.zip -P ./depdir/

./depdir/$(REVEAL_JS_TARBALL): | directories
	wget https://github.com/hakimel/reveal.js/archive/$(REVEAL_JS_TARBALL) -P ./depdir/


./depdir/$(DOOM_SHAREWARE): | directories
	wget http://distro.ibiblio.org/pub/linux/distributions/slitaz/sources/packages/d/doom1.wad -P ./depdir/


./depdir/$(FOSSIL_TARBALL): | directories
	wget https://www.fossil-scm.org/download/$(FOSSIL_TARBALL) -P ./depdir/

doomshareware: | ./depdir/$(DOOM_SHAREWARE)

revealjs: | ./depdir/$(REVEAL_JS_TARBALL)
	tar -xvzf ./depdir/$(REVEAL_JS_TARBALL)
	mv reveal.js-$(REVEAL_JS_VERSION) revealjs 

d3js: | ./depdir/d3.zip
	unzip ./depdir/d3.zip -d d3

deps:  directories revealjs d3js

clean: clean-dirs

clean-dirs:
	rm -fr depdir
	rm -fr revealjs
	rm -fr d3
	rm -fr *~
	rm -fr *gz

presentation:
	$(PYTHON) -m http.server
