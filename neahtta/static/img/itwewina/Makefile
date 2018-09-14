LOGO = itwew.png

all: optimize favicon.ico

optimize:
	optipng -o9 $(LOGO)

favicon.ico: $(LOGO)
	convert $< -define icon:auto-resize=32,16 $@

.PHONY: all optimize
