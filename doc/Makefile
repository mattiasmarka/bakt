F=MARKA_2025_bakatoo

$F.pdf: $F.tex srcs.bib *.jpg
	-lualatex --interaction=nonstopmode $F.tex
	-biber $F.bcf
	-lualatex --interaction=nonstopmode $F.tex
	-bibib $F.bcf
	-lualatex --interaction=nonstopmode $F.tex

clean:
	-rm $F.aux $F.bbl $F.bcf $F.blg $F.log $F.out $F.pdf $F.run.xml $F.toc
