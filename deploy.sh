#!/bin/sh

# Restore deleted files
git checkout $(git ls-files -d)

CHANGES=`git whatchanged --since="3 days ago" -p pubs/ src_docs/ media/`

rm python/*.pyc

rm -rf ~/public_html/teaching/*
for CLASS in LBSC_690_2012 INFM_718_2011 COS_280_2008 CMSC_773_2012 DATA_DIGGING CMSC_723_2013 CSCI_5832 DEEP CSCI_5622
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

for SUBDIR in docs images downloads teaching qb projects style
        do
            mkdir -p ~/public_html/$SUBDIR
            cp $SUBDIR/*.* ~/public_html/$SUBDIR
done

python python/site.py `git show -s --format=%ci`

if [ ${#CHANGES} -gt 0 ]
   then
        echo "CHANGES DETECTED!"
        cp ~/public_html/dyn-pubs/year.txt resume_src/pubs_by_year.tex
        cp ~/public_html/dyn-media/category.txt resume_src/media_by_year.tex
        pdflatex resume_src/resume
        mv resume.pdf docs/resume.pdf
        for FILE in `ls pubs/*.tex`
        do
            pdflatex $FILE; rm $FILE
        done
fi
rm *.aux *.log *.out;
rm pubs/*.*
rm pubs/#*#
rm pubs/*~
mv *.pdf docs

# Clean up cruft
rm */*~
rm *~
rm */*/*~
rm docs/*.pdf
git checkout $(git ls-files -d)
