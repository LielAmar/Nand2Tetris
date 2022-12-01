PROJNUM=10
PROJFILES=README Makefile *.rb JackAnalyzer

all:
	@echo Done

clean:
	$(RM) *~ proj${PROJNUM}.tar

.PHONY: test
test:
	./test_all

.PHONY: tar
tar:
	tar -b1 -cf proj$(PROJNUM).tar $(PROJFILES)

