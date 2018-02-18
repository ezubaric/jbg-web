#!/bin/sh

# Restore deleted files
git checkout $(git ls-files -d)

CHANGES=`git whatchanged --since="3 days ago" -p pubs/ src_docs/ media/ resume_src/`

rm -f python/*.pyc
rm -f pubs/*.tex

rm -rf ~/public_html/teaching/*
for CLASS in LBSC_690_2012 INFM_718_2011 COS_280_2008 CMSC_773_2012 DATA_DIGGING CMSC_723_2013 CSCI_5832 DEEP CSCI_5622 CSCI_3022 CSCI_7000 CMSC_726 INST_414
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

for SUBDIR in docs images downloads style projects
        do
            mkdir -p ~/public_html/$SUBDIR
            cp $SUBDIR/*.* ~/public_html/$SUBDIR
done

rm -rf ~/public_html/$SUBDIR
cp -r qb ~/public_html/$SUBDIR

if hash python3 2>/dev/null; then
        PYCOMMAND=python3
else
        PYCOMMAND=python
fi

$PYCOMMAND python/site.py `git show -s --format=%ci`

if [ ${#CHANGES} -gt 0 ]
   then
        echo "CHANGES DETECTED!"
        cp ~/public_html/dyn-pubs/venue.txt resume_src/pubs_by_venue.tex
        $PYCOMMAND python/extract_media_coverage.py ~/public_html/dyn-media/category.txt resume_src/media.tex
        pdflatex resume_src/research
        bibtex research
        for FILE in public umd short_cv teaching service research
        do
            echo $FILE
            pdflatex resume_src/$FILE
            mv $FILE.pdf ~/public_html/docs
        done
	cp resume_src/letter.html ~/public_html/docs
        for FILE in `ls pubs/*.tex`
        do
            pdflatex $FILE 
            PDFFILE="${FILE/.tex/.pdf}"
            ls -lh "${PDFFILE/pubs/.}"
            mv "${PDFFILE/pubs/.}" ~/public_html/docs
        done
fi

rm *.aux *.log *.out;
rm pubs/#*#
rm pubs/*~

# Clean up cruft
rm */*~
rm *~
rm */*/*~
rm docs/*.pdf
git checkout $(git ls-files -d)
