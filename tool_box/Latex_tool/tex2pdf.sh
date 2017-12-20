#!/bin/tcsh -f

if( $#argv == 1 ) then
	if( $1 =~ *.tex ) then
		platex $1
		set dviName = `echo $1 | sed -e "s/\.tex/\.dvi/"`
		dvips $dviName
		# xdvi $dviName &
		# dvipdfmx -l $dviName
		# xdvi -paper a4r $dviName &
	else
		echo "input file is not tex file."
	endif
else
	echo "number of arguments is not single."
endif

