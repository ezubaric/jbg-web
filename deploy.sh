#!/bin/bash

# Restore deleted files
git checkout $(git ls-files -d)

CHANGES=`git whatchanged --since="3 days ago" -p pubs/ src_docs/ media/ resume_src/`

rm -f python/*.pyc
rm -f pubs/*.tex

mkdir -p ~/public_html/dyn-media
mkdir -p ~/public_html/dyn-pubs

rm -rf ~/public_html/teaching/*
for CLASS in LBSC_690_2012 INFM_718_2011 COS_280_2008 CMSC_773_2012 DATA_DIGGING CMSC_723 DEEP CSCI_5622 CSCI_3022 CSCI_7000 CMSC_726 INST_414 INST_808 CMSC_470 CMSC_848
        do
           mkdir -p ~/public_html/teaching/$CLASS
           cp teaching/$CLASS/*.* ~/public_html/teaching/$CLASS
	   for SUBDIR in slides reading
	   do
               if [ -d teaching/$CLASS/$SUBDIR ]
                   then
                     mkdir -p ~/public_html/teaching/$CLASS/$SUBDIR
	             cp teaching/$CLASS/$SUBDIR/*.* ~/public_html/teaching/$CLASS/$SUBDIR
               fi
	   done
done

for SUBDIR in docs images downloads style projects sound
        do
            mkdir -p ~/public_html/$SUBDIR
            cp $SUBDIR/*.* ~/public_html/$SUBDIR
done

rm -rf ~/public_html/qb
cp -r qb ~/public_html/

if hash python3 2>log.txt; then
        PYCOMMAND=python3
else
        PYCOMMAND=python
fi

echo "USING $PYCOMMAND"

$PYCOMMAND python/site.py `git show -s --format=%ci`

if [ ${#CHANGES} -gt 0 ]
   then
        echo "CHANGES DETECTED!"
        cp ~/public_html/dyn-pubs/venue.txt resume_src/pubs_by_venue.tex
        $PYCOMMAND python/extract_media_coverage.py ~/public_html/dyn-media/category.txt resume_src/media.tex
	echo "Done media"
        for FILE in teaching research
	do
		    pdflatex resume_src/$FILE > log.txt
		    bibtex $FILE
	done
	# echo "Done rsearch"
        for FILE in public umd short_cv teaching service diversity research german funding_wrapper publications_wrapper funding_wrapper
        do
            echo $FILE
	    echo "---------------------------"
            pdflatex resume_src/$FILE > log.txt
            mv $FILE.pdf ~/public_html/docs
        done
	cp resume_src/letter.html ~/public_html/docs
        for FILE in `ls -r pubs/*.tex`
        do
	    echo $FILE
	    echo "---------------------------"
            pdflatex $FILE > ${FILE/.tex/.log}
            PDFFILE="${FILE/.tex/.pdf}"
            ls -lh "${PDFFILE/pubs/.}"
            mv "${PDFFILE/pubs/.}" ~/public_html/docs
        done
fi

grep "pdfpages Error" pubs/*.log

rm *.aux *.log *.out;
rm pubs/#*#
rm pubs/*~

# Clean up cruft
rm */*~
rm *~
rm */*/*~
rm pubs/*.log
rm docs/*.pdf
git checkout $(git ls-files -d)
