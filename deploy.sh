#!/bin/sh
python python/site.py

export UPDATEDDOCS="`find pubs/* src_docs/* -mtime -6  -type f`"
echo "UPDATE DOCS: $UPDATEDDOCS"
if [ ${#UPDATEDDOCS} -gt 0 ]
   then
        for FILE in `ls pubs/*.tex`
        do
            pdflatex $FILE
        done
fi

rm *.aux *.log
mv *.pdf docs

cp style.css ~/public_html
for SUBDIR in docs images downloads teaching qb
        do
            mkdir -p ~/public_html/$SUBDIR
            cp $SUBDIR/*.* ~/public_html/$SUBDIR
done

rm -rf ~/public_html/teaching/*
for CLASS in LBSC_690_2012 INFM_718_2011 COS_280_2008 CMSC_773_2012 DATA_DIGGING CMSC_723_2013
        do
           mkdir -p ~/public_html/teaching/$CLASS
           mv teaching/$CLASS/*.* ~/public_html/teaching/$CLASS
	   for SUBDIR in xml_demo javascript_demo sqllite_walkthrough slides reading
	   do
               if [ -d teaching/$CLASS/$SUBDIR ]
                   then
                     mkdir -p ~/public_html/teaching/$CLASS/$SUBDIR
	             mv teaching/$CLASS/$SUBDIR/*.* ~/public_html/teaching/$CLASS/$SUBDIR
               fi
	   done
done

rm pubs/*.*
