CURR_DATETIME=$(shell date)

gen_res:
	python3 parse_xml.py > res.txt
	cat res.txt 

test:
	$(MAKE) gen_res && \
	git add res.txt && \
	git commit -m "Update res.txt as of $(CURR_DATETIME)" && \
	git push origin master