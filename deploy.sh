#!/bin/sh

# Restore deleted files
git checkout $(git ls-files -d)

CHANGES=`git whatchanged --since="3 days ago" -p pubs/ src_docs/ media/ resume_src/`

rm python/*.pyc

rm -rf ~/public_html/teaching/*
for CLASS in LBSC_690_2012 INFM_718_2011 COS_280_2008 CMSC_773_2012 DATA_DIGGING CMSC_723_2013 CSCI_5832 DEEP CSCI_5622 CSCI_3022
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

python python/site.py `git show -s --format=%ci`

if [ ${#CHANGES} -gt 0 ]
   then
        echo "CHANGES DETECTED!"
        cp ~/public_html/dyn-pubs/venue.txt resume_src/pubs_by_venue.tex
        python python/extract_media_coverage.py ~/public_html/dyn-media/category.txt resume_src/media.tex
        pdflatex resume_src/research &> /dev/null
        bibtex research
        for FILE in resume short_cv teaching service research
        do
            echo $FILE
            pdflatex resume_src/$FILE &> /dev/null
        done
        mv resume.pdf short_cv.pdf teaching.pdf service.pdf research.pdf ~/public_html/docs
        for FILE in `ls pubs/*.tex`
        do
            pdflatex $FILE &> /dev/null
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
