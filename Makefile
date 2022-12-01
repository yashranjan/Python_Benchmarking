CURR_DATETIME ?= $(shell date)

loop ?= 4
repeat ?= 3

gen_res:
	python3 parse_xml.py loop=$(loop) repeat=$(repeat) > res.txt
	cat res.txt 

test:
	$(MAKE) gen_res && \
	git add res.txt && \
	git commit -m "Update res.txt as of $(CURR_DATETIME)" && \
	git push origin master