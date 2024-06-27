
import os
import sys
from website_writer import WebsiteWriter, global_replace

home = os.environ.get('HOME')
print("Home: " + home)

if __name__ == "__main__":
    writer = WebsiteWriter("src/", home + "/public_html/", "resources/_header.html", "resources/_footer.html",
                           "Jordan Boyd-Graber", "http://umiacs.umd.edu/~jbg/", sys.argv[1])
    writer.add_index("pubs/", "Pubs", [("Year", 0, []), ("Category", 0, []), ("Authors", 1, ["Jordan Boyd-Graber"]), ("Venue", 0, []), ("Project", 0, [])], "Year")
    writer.add_index("media/", "Media", [("Year", 0, []), ("Category", 0, []), ("Project", 0, [])], "Category")
    writer.add_teaching("teaching/*/index.json")

    
    writer.write_index("Pubs", True)
    writer.write_index("Media", True)

    writer.write()
    teach = writer.add_raw("teaching/*/index.html", "../../")
    proj = writer.add_raw("projects/*.html", "../")
    print("----------------------")
    print(global_replace.keys())
    print(global_replace["Pubs:Preprint"])
