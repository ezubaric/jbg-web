
import os
import sys
from website_writer import WebsiteWriter, global_replace

home = os.environ.get('HOME')
print "Home: ", home

writer = WebsiteWriter("src/", home + "/public_html/", "resources/_header.html", "resources/_footer.html",
                       "Jordan Boyd-Graber", "http://cs.colorado.edu/~jbg/", sys.argv[1])
writer.add_index("pubs/", "Pubs", [("Year", 0, []), ("Category", 0, []), ("Authors", 1, ["Jordan Boyd-Graber"]), ("Venue", 0, []), ("Project", 0, [])])
writer.write()
writer.write_index("Pubs", True)
print("----------------------")
writer.add_raw("teaching/*/index.html", "../../")
writer.add_raw("projects/*.html", "../")
