
import os
import sys
from website_writer import WebsiteWriter, global_replace

home = os.environ.get('HOME')
print "Home: ", home

writer = WebsiteWriter("src/", home + "/public_html/", "resources/_header.html", "resources/_footer.html",
                       "Jordan Boyd-Graber", "http://cs.colorado.edu/~jbg/", sys.argv[1])
writer.add_index("pubs/", "Pubs", [("Year", 0, []), ("Category", 0, []), ("Authors", 1, ["Jordan Boyd-Graber"]), ("Venue", 0, []), ("Project", 0, [])], "Year")
writer.add_index("media/", "Media", [("Year", 0, []), ("Category", 0, []), ("Project", 0, [])], "Category")

writer.write()
writer.write_index("Pubs", True)
writer.write_index("Media", True)
print(global_replace.keys())
print("----------------------")
teach = writer.add_raw("teaching/*/index.html", "../../")
proj = writer.add_raw("projects/*.html", "../")
