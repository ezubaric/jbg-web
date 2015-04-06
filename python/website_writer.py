
from glob import glob
from string import capwords
from datetime import date, datetime
import time
import os
import re

kHTML = re.compile(r'<.*?>')
kBRACKET = re.compile(r'\[.*?\]')
kHTML_CHARS = {"&eacute;": "e", "\%": "%"}

class Student:
  def __init__(self, name, start, end, webpage = None):
    self._name = name
    self._start = start
    self._end = end
    self._web = webpage

UMD_MAPPING = {"Chapter": "\\ifumd 2.A.iii. \else \\fi Chapters in Books",
               "Refereed Conference": "\\ifumd 2.E.ii. \\fi Refereed Conferences",
               "Workshop": "\\ifumd 2.E.ii. \\fi Refereed Workshops",
               "Journal": "\\ifumd 2.B. \\fi Articles in Refereed Journals"}

STUDENTS = {"Ke Zhai": Student("Ke Zhai", 2010, 2015, "http://www.umiacs.umd.edu/~zhaike/"),
            "Yuening Hu": Student("Yuening Hu", 2010, 2015, "http://www.cs.umd.edu/~ynhu/"),
            "Kimberly Glasgow": Student("Kimberly Glasgow", 2010, 2015),
            "Brianna Satinoff": Student("Brianna Satinoff", 2010, 2012),
            "Viet-An Nguyen": Student("Viet-An Nguyen", 2011, 2016, "http://www.cs.umd.edu/~vietan/index.htm"),
            "Mohamad Alkhouja": Student("Mohamad Alkhouja", 2011, 2013),
            "Thang Nguyen": Student("Thang Nguyen", 2014, 2019, "http://www.umiacs.umd.edu/~daithang/"),
            "Mohit Iyyer": Student("Mohit Iyyer", 2014, 2019, "http://cs.umd.edu/~miyyer/"),
            "Alvin {Grissom II}": Student("Alvin Grissom II", 2013, 2017, "http://www.umiacs.umd.edu/~alvin/"),
            "Eric Hardisty": Student("Eric Hardisty", 2010, 2011)}

def format_name(students, name, year, latex):
  if name in students:

    try:
      year = int(year)
    except ValueError:
      year = datetime.now().year

    s = students[name]
    if year >= s._start and year <= s._end:
      if latex:
        if s._web:
            return "\\underline{\\href{%s}{%s}}" % (s._web, s._name)
        else:
            return "\\underline{%s}" % (s._name)
      elif s._web:
        return '<a href="%s">%s</a>' % (s._web, s._name)
      else:
        return "<u>%s</u>" % s._name

  if name == "Jordan Boyd-Graber":
    if latex:
      return "{\\bf Jordan Boyd-Graber}"
    else:
      return "<b>Jordan Boyd-Graber</b>"

  if not latex:
    name = name.replace("\\'{e}", "&eacute;")
    name = name.replace("\\'e", "&eacute;")
    name = name.replace("{", "")
    name = name.replace("}", "")

  return name

class IndexElement:
  def __init__(self, file_contents):
    self.fields = {"Authors": [], "Link": [], "Category": [], "Venue": []}
    for ii in [x for x in file_contents.split("~~") if x != ""]:
      key = capwords(ii.split("|")[0].strip())
      val = ii.split("|")[1].strip()
      if key == "Author":
        for jj in val.split(" and "):
          print "Author: ", jj
          self.fields["Authors"].append(jj)
      if not key in self.fields:
        self.fields[key] = []
      self.fields[key].append(val)

  def author_string(self, latex):
    s = ""
    if "Authors" in self.fields:
      assert "Year" in self.fields
      authors = [format_name(STUDENTS, x, self.fields["Year"][0], latex) \
                   for x in self.fields["Authors"]]
      if len(authors) > 2:
        s += ", ".join(authors[:-1]) + ", and " + authors[-1]
      elif len(authors) == 2:
        s += " and ".join(authors)
      else:
        s += authors[0]
      s += ".  "
    return s

  def wrapper_document(self):
    s = """
    \\documentclass[a4paper]{article}
    \\usepackage{savetrees}
    \\usepackage{hyperref}
    \\usepackage{pdfpages}

    \\begin{document}

    ~~~citation~~~

    \\vspace{5cm}

    \\begin{verbatim}
    ~~~bibtex~~~
    \\end{verbatim}

    \\includepdf[pages={-}]{src_~~~filename~~~}

    \\end{document}
    """

    s = s.replace("~~~citation~~~", self.latex(url="", acceptance = False))
    s = s.replace("~~~filename~~~", self.fields["Url"][0])
    s = s.replace("~~~bibtex~~~", self.bibtex())

    return s

  def txt(self, acceptance=True, url=''):
    text = kHTML.sub('', self.html(False, url, ""))
    text = kBRACKET.sub('', text)
    if "Acceptance" in self.fields and acceptance:
      text += " (" + self.fields["Acceptance"][0] + "\% Acceptance Rate)"
    text += "\n"
    if "Url" in self.fields and url:
      if url.endswith("/"):
        url = "%s%s\n" % (url, self.fields["Url"][0])
      else:
        url = "%s/%s\n" % (url, self.fields["Url"][0])
      text += url
    text += "\n"

    for ii in kHTML_CHARS:
      if ii in text:
        text = text.replace(ii, kHTML_CHARS[ii])

    return text

  def latex(self, url="", acceptance=True):
    s = self.author_string(True)
    if "Title" in self.fields:
      if "Url" in self.fields and url:
          s += '{\\bf \href{%s/%s}{%s}}.  ' % (url, self.fields["Url"][0], self.fields["Title"][0])
      else:
          s += '{\\bf %s}.  ' % (self.fields["Title"][0])
    if "Booktitle" in self.fields:
      s += "\\emph{%s}, " % self.fields["Booktitle"][0]
    if "Journal" in self.fields:
      s += "\\emph{%s}, " % self.fields["Journal"][0]
    if "Year" in self.fields:
      s += self.fields["Year"][0]
    if "Acceptance" in self.fields and acceptance:
      s += " (" + self.fields["Acceptance"][0] + "\% Acceptance Rate)"

    s += ".\n\n"
    return s

  def html(self, bibtex, url, section):
    s = self.author_string(False)

    formatted_title = self.fields["Title"][0].replace("``", "&quot;").replace("\dots", "&hellip;").replace("~", "&nbsp;")
    if "Title" in self.fields and "Url" in self.fields:
      s += "<b><a href=\"../%s\"  onClick=\"javascript: pageTracker._trackPageview('%s'); \">%s</a></b>.  " % (self.fields["Url"][0], self.fields["Url"][0], formatted_title)
    elif "Title" in self.fields:
      s += '<b>%s</b>.  ' % formatted_title

    if "Booktitle" in self.fields:
      s += "<i>%s</i>, " % self.fields["Booktitle"][0]

    if "School" in self.fields:
      s += "<i>Ph.D. thesis, %s</i>, " % self.fields["School"][0]

    if "Journal" in self.fields:
      s += "<i>%s</i>, " % self.fields["Journal"][0]
    if "Year" in self.fields:
      s += self.fields["Year"][0]
      s += "."

    s = s.replace("{", "")
    s = s.replace("}", "")

    for ii in self.fields["Link"]:
      text, url = ii.split("*")
      if url.startswith("http://"):
        s += ' [<a href="%s">%s</a>]' % (url, text)
      else:
        s += ' [<a href="../%s">%s</a>]' % (url, text)

		# print self.fields["Title"], len(self.fields["Bibtex"]), len(self.fields["Authors"]), len(self.fields["Year"])
    div_name = str(hash("".join("".join(x) for x in self.fields.values()) + section))
    if bibtex and len(self.fields["Bibtex"]) > 0:
      s += ' [<a href="javascript:unhide('
      s += "'%s'" % div_name
      s += ');">BIBTEX</a>]\n'
      s += '<div id="'
      s += "%s" % div_name
      s += '" class="hidden">\n'
      s += "<br><PRE>\n" + self.bibtex() + "</PRE>\n"
      s += '</div>'

    if "Note" in self.fields:
      s += "<B>%s</B>\n" % "".join(self.fields["Note"])


    return s

  def bibtex(self):
    s = "@%s{%s,\n" % (self.fields["Bibtex"][0], ":".join(x.split()[-1] for x in self.fields["Authors"]) + "-" + self.fields["Year"][0])
    for ii in self.fields:
      if ii in ["Author", "School", "Journal", "Pages", "Volume", "Year", "Number", "ISSN", "Abstract", "Location", "Title", "Booktitle", "Isbn", "Publisher", "Address", "Editor", "Series"]:
        s += "\t%s = {%s},\n" % (ii, self.fields[ii][0])
    s += "}\n"
    return s

  def keys(self, name, criteria):
    """
    Create keys that can be sorted
    """
    # print "Values:", criteria, self.fields[criteria]

    try:
      year = -int(self.fields["Year"][0])
    except ValueError:
      year = float("-inf")

    return [(x, year, self.fields["Title"][0], name) for \
              x in self.fields[criteria]]

class WebsiteWriter:
  def __init__(self, source, output, header_file, footer_file, site_title, url):
    self.STATIC_DIR = "static"
    self.DYNAMIC_DIR = "dyn-"

    self._source = source
    self._output = output
    self._header = open(header_file).read()
    self._header = self._header.replace("~~SITETITLE~~", site_title)

    d = date.fromtimestamp(time.time()).isoformat()
    print d
    self._footer = open(footer_file).read().replace("~~TIMESTAMP~~", d)
    self._url = url

    self._files = {}
    self._indexed = {}
    self._criteria = {}

    for ii in glob(source + "*.html"):
      print("Adding file %s" % ii)
      name = capwords(ii.split("/")[-1].replace(".html", "").replace("_", " "))
      self._files[name] = ii

  def navigation(self, prefix):
    s = "<ul>"
    keys = [x for x in self._files.keys() if x != "Home"]
    keys += self._indexed.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    print(keys)

    for ii in keys:
      if ii in self._files:
        s += ('\t<li><a href="%s' + self.STATIC_DIR + '/%s">%s</a>\n') % \
            (prefix, self._files[ii].split("/")[-1], ii)
      else:
        s += ('\t<li><a href="%s' + self.DYNAMIC_DIR + '%s/year.html">%s</a>\n') % \
            (prefix, ii, ii.title())
    s += "</ul>\n"
    return s


  def add_index(self, path, name = "Documents", criteria=[("Year", 0, [])]):
    index = {}
    print "Searching:", path + "*"
    for ii in glob(path + "*"):
      # Don't go through backup files
      if "~" in ii or "#" in ii or "." in ii:
        continue
      print "Indexing", ii
      item = IndexElement(open(ii).read())
      print item.fields
      if "Nopub" in item.fields:
		  print("Skipping %s" % ii)
		  continue
      else:
		  index[ii] = item

      if "Url" in index[ii].fields and index[ii].fields["Url"]:
        resource = index[ii].fields["Url"][0].split("/")[1].split(".")[0]
        o = open("pubs/%s.tex" % resource, 'w')
        o.write(index[ii].wrapper_document())

    self._indexed[name.lower()] = index
    self._criteria[name.lower()] = criteria
    print("Criteria now %s" % str(self._criteria.keys()))

  def write_index(self, index, bibtex=True):
    print("Creating index for %s from %s" % (index, str(self._criteria.keys())))
    for ii in self._criteria[index.lower()]:
      print "Criteria: ", ii
      sort_by, min_count, exclude = ii
      o = open(self._output + "/" + self.DYNAMIC_DIR +
               "%s/%s.html" % (index.lower(), sort_by.lower()), 'w')
      latex_out = open(self._output + "/" + self.DYNAMIC_DIR +
                       "%s/%s.txt" % (index.lower(), sort_by.lower()), 'w')
      bibtex_out = open(self._output + "/" + self.DYNAMIC_DIR +
                        "%s/%s.bib" % (index.lower(), sort_by.lower()), 'w')
      text_out = open(self._output + "/" + self.DYNAMIC_DIR +
                      "%s/%s_raw.txt" % (index.lower(), sort_by.lower()), 'w')

      latex_out.write("\\vspace{.1cm}\nStudents directly advised or co-advised \\underline{in underline}.\n\\vspace{.4cm}")

      keys = []
      lookup = {}
      for jj in self._indexed[index.lower()]:
        contrib = self._indexed[index.lower()][jj].keys(jj, sort_by)
        # print "Contrib: ", jj, contrib
        keys += contrib
        for kk in contrib:
          assert not kk in lookup, "%s already found as %s" % (str(kk), lookup[kk].txt())
          lookup[kk] = self._indexed[index.lower()][jj]

      primary = [x[0] for x in keys]
      primary = [x for x in primary if \
                   len([y for y in primary if y==x]) > min_count and \
                   not x in exclude]
      keys = [x for x in keys if x[0] in primary]
      keys.sort()
      if sort_by == "Year":
        keys.reverse()

      o.write(self._header.replace("~~PAGETITLE~~", \
                                     '%s (%s)' % (index, sort_by))
              .replace("~~NAVIGATION~~", self.navigation("../"))
              .replace("~~PATHPREFIX~~", "../"))
      old = None
      o.write('<div id="content">\n')
      o.write('<h1 id="header"> %s (%s) </h1>\n' % (index, sort_by))

      o.write("<center>Sort by:")
      for jj in self._criteria[index.lower()]:
        o.write(' <a href="%s.html">%s</a>' % (jj[0].lower(), jj[0]))
      o.write("</center>\n")
      for jj in keys:
        if old != jj[0]:
          if old:
            latex_out.write("\n\\end{enumerate}\n}")
            o.write("\t</ul>")
          old = jj[0]
          o.write("\t<h2>%s</h2>\n\t<ul>\n" % format_name([], old, -1, False))
          text_out.write(format_name([], old, -1, False))
          text_out.write("\n-------------------------\n\n")
          out_string = old
          latex_out.write("\n\\headedsection{{\\bf %s}}{}{\n\n" % out_string)

          latex_out.write("\n\\begin{enumerate}\n")

        latex_out.write("\t \item " + lookup[jj].latex(self._url))
        bibtex_out.write(lookup[jj].bibtex())
        text_out.write(lookup[jj].txt(url=self._url))

        o.write("\t\t<li>" + lookup[jj].html(bibtex, self._url, old))

      latex_out.write("\n\\end{enumerate}")
      latex_out.write("\n}")
      o.write("\t</ul>\n")
      o.write("<p>&nbsp;</p>\n")
      o.write('<center><a href="%s.txt">LaTeX Version</a>&nbsp;' % sort_by.lower())
      o.write('<a href="%s.bib">BibTex Version</a>&nbsp;' % sort_by.lower())
      o.write('<a href="%s_raw.txt">Text Version</a></center>' % sort_by.lower())

      o.write("<p>&nbsp;</p>\n")
      o.write("</div>")
      o.write(self._footer)
      o.close()

  def unindexed_directory(self, source_path, target_path):
    final_directory = self._output + self.STATIC_DIR + "/" + target_path
    try:
      os.mkdir(final_directory)
    except OSError:
      print "Dir couldn't be made:", final_directory

    for ii in glob(source_path + "/*.html"):
      filename = final_directory + "/" + ii.split("/")[-1]
      print "Writing non-indexed file", filename
      self.write_file(filename, ii.split("/")[-1].replace(".html", ""), ii,
                      "../../")

  def write_file(self, filename, title, raw, prefix="../"):
    contents = self._header.replace("~~PAGETITLE~~", title)
    contents = contents.replace("~~NAVIGATION~~", self.navigation(prefix))
    contents += open(raw).read()
    contents = contents.replace("~~PATHPREFIX~~", prefix).replace("~~PAGETITLE~~", title)
    contents += self._footer

    o = open(filename, 'w')
    o.write(contents)
    o.close()

  def write(self):
    try:
      os.mkdir(self._output + self.STATIC_DIR)
    except OSError:
      print "Couldn't make " + self._output + self.STATIC_DIR
    # Write the static files
    for ii in self._files:
      self.write_file(self._output + self.STATIC_DIR + "/%s.html" % ii.lower().replace(" ", "_"), ii, self._files[ii])

      # Put the main file one directory up
      if ii.lower() == "home":
        self.write_file(self._output + "/index.html", ii, self._files[ii], "")

    for ii in self._indexed:
      path = self._output + "/" + self.DYNAMIC_DIR + "%s" % ii
      try:
        os.mkdir(path)
      except OSError:
        print "Cannot make directory: ", path
