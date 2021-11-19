from glob import glob
from string import capwords
from datetime import date, datetime
from collections import defaultdict
import time
import os
import re

import pdb

kHTML = re.compile(r'<.*?>')
kBRACKET = re.compile(r'\[.*?\]')
kHTML_CHARS = {"&eacute;": "e", "\%": "%"}

global_replace = defaultdict(str)

def remove_html_chars(text):
    for ii in kHTML_CHARS:
      if ii in text:
        text = text.replace(ii, kHTML_CHARS[ii])
    return text

def bibtex_last(name):
  """
  Extract last name from bibtex field, dealing with pesky Alvin and Hal
  """

  name = name.replace("\\'{e}", 'e')

  if "{" in name:
    last_name = name.split("{")[1]
    last_name = last_name.rsplit("}")[0]
    return last_name.replace(" ", "-")
  else:
    return name.split()[-1]

class Student:
  def __init__(self, name, start, end, webpage = None, kind="PHD",
               job=None, thesis='', thesis_url=''):
    self._name = name
    self._start = start
    self._end = end
    self._web = webpage
    self._job = job
    self._kind = kind
    self._thesis = thesis
    self._thesis_url = thesis_url

  def latex(self):
      val = self._name
      return val

  def html(self):
      val = self._name

      if not self._web is None:
          val = '<A HREF="%s">%s</a>' % (self._web, val)

      if not self._job is None:
          val = "%s (Student %i&#8211;%i: Now at %s)" % (val, self._start, self._end, self._job)

      if self._thesis:
        if self._thesis_url:
          val += ' [<a href="%s">%s</a>]' % (self._thesis_url, self._thesis)
        else:
          val += ' [%s]' % self._thesis

      return val

UMD_MAPPING = {"Chapter": "\\ifumd II.B.1. \else \\fi Chapters in Books",
               "Book": "\\ifumd II.A.1. Books Authored \\else Books \\fi ",
               "Refereed Conference": "\\ifumd II.D.1. \\fi Refereed Conference Proceedings",
               "Preprint": "\\ifumd II.F.2  \\fi Preprints / Working Papers",
               "Workshop": "\\ifumd II.E.4. \\fi Refereed Workshops",
               "Journal": "\\ifumd II.C.1 \\fi Refereed Journal Articles"}

kSTUDENTS = {"Ke Zhai": Student("Ke Zhai", 2010, 2014, "https://kzhai.github.io/",
                                job="Microsoft, Senior Research Scientist"),
             "Weiwei Yang": Student("Weiwei Yang", 2014, 2019, "http://www.cs.umd.edu/~wwyang/", job="Facebook"),
             "Yoo Yeon Sung": Student("Yoo Yeon Sung", 2019, 2024, "https://www.linkedin.com/in/yooyeon-sung-a81a0b131"),
             "Yuening Hu": Student("Yuening Hu", 2010, 2014, "https://scholar.google.com/citations?user=mO_62fQAAAAJ&hl=en",
                                   job="Google", thesis_url="https://drum.lib.umd.edu/bitstream/handle/1903/15763/Hu_umd_0117E_15485.pdf", thesis='Expressive Knowledge Resources in Probabilistic Models'),
             "Kimberly Glasgow": Student("Kimberly Glasgow", 2010, 2014, job="Johns Hopkins Applied Physics Laboratory, Senior Research Scientist"),
             "Davis Yoshida": Student("Davis Yoshida", 2015, 2016, kind="UG"),
             "Davis Yoshida": Student("Davis Yoshida", 2016, 2017, kind="MS", job="TTIC, PhD Candidate"),
             "Forough Poursabzi-Sangdeh": Student("Forough Poursabzi-Sangdeh", 2014, 2018, "https://www.microsoft.com/en-us/research/people/fopoursa/", job="MSR, Postdoc"),
             "Brianna Satinoff": Student("Brianna Satinoff", 2010, 2012, kind="MS"),
             "Yoshinari Fujinuma": Student("Yoshinari Fujinuma", 2015, 2021, "http://akkikiki.github.io/about/"),
             "He He": Student("He He", 2012, 2016, "https://hhexiy.github.io/",
                              job="NYU, Assistant Professor"),
             "Shudong Hao": Student("Shudong Hao", 2015, 2017, "http://shudong-hao.com/", job="Bard College, Assistant Professor"),
             "Mozhi Zhang": Student("Mozhi Zhang", 2016, 2021, "http://www.mozhi.umiacs.io"),
             "Jo Shoemaker": Student("Jo Shoemaker", 2017, 2020),
             "Michelle Yuan": Student("Michelle Yuan", 2017, 2022, "http://www.cs.umd.edu/~myuan/"),
             "Denis Peskov": Student("Denis Peskov", 2016, 2021,
                                        "http://denispeskov.github.io/"),
             "Naveen Raman": Student("Naveen Raman", 2019, 2021, "http://naveenraman.com/"),
             "Viet-An Nguyen": Student("Viet-An Nguyen", 2011, 2015,
                                       "http://www.cs.umd.edu/~vietan/index.htm",
                                       job="Facebook"),
             "Pedro Rodriguez": Student("Pedro Rodriguez", 2015, 2021, "https://www.pedro.ai/", job="Facebook, Research Scientist", thesis_url="https://www.pedro.ai/static/publications/pedro_rodriguez_phd_thesis.pdf", thesis="Evaluating Machine Intelligence with Question Answering"),
             "Fenfei Guo": Student("Fenfei Guo", 2015, 2022, "https://csel.cs.colorado.edu/~fegu1724/"),
             "Mohamad Alkhouja": Student("Mohamad Alkhouja", 2011, 2013, kind="MS"),
             "Wenyan Li": Student("Wenyan Li", 2017, 2018, kind="MS"),
             "Thang Nguyen": Student("Thang Nguyen", 2014, 2019, "http://www.umiacs.umd.edu/~daithang/", job="CGI Federal, Data Scientist"),
             "Mohit Iyyer": Student("Mohit Iyyer", 2014, 2017, "https://people.cs.umass.edu/~miyyer/", job="UMass, Assistant Professor"),
             "Manjhunath Ravi": Student("Manjhunath Ravi", 2015, 2016, kind="MS"),
             "Alvin {Grissom II}": Student("Alvin Grissom II", 2013, 2017, "https://www.ursinus.edu/live/profiles/3125-alvin-grissom-ii",
                                           job="Haverford College, Assistant Professor"),
             "Eric Wallace": Student("Eric Wallace", 2018, 2019, "http://www.ericswallace.com/", kind="UG", job="UC Berkeley, PhD Student"),
             "Emily Gong": Student("Emily Gong", 2020, 2021, kind="MS"),
             "Matthew Shu": Student("Matthew Shu", 2019, 2021, kind="UG"),
             "Andrew Mao": Student("Andrew Mao", 2020, 2022, kind="MS"),
             "Sander Schulhoff": Student("Sander Schulhoff", 2019, 2022, kind="UG"),
             "Chenglei Si": Student("Chenglei Si", 2020, 2023, "https://noviscl.github.io", kind="UG"),
             "Arjun Akkiraju": Student("Arjun Akkiraju", 2020, 2022, kind="UG"),
             "Shravan Sanjiv": Student("Shravan Sanjiv", 2017, 2018, kind="UG"),
             "Danny Bouman": Student("Danny Bouman", 2013, 2014, kind="UG"),
             "Stephanie Hwa": Student("Stephanie Hwa", 2013, 2014, kind="UG"),
             "Alison Smith": Student("Alison Smith", 2012, 2020, "http://alisonmsmith.github.io/"),
             "Henrik Larsen": Student("Henrik Larson", 2016, 2017, kind="UG"),
             "Shi Feng": Student("Shi Feng", 2017, 2021, "http://www.shifeng.umiacs.io"),
             "Chen Zhao": Student("Chen Zhao", 2018, 2022, "http://www.chenz.umiacs.io"),
             "Ahmed Elgohary": Student("Ahmed Elgohary Ghoneim", 2018, 2021, "http://www.cs.umd.edu/~elgohary/"),
             "Eric Hardisty": Student("Eric Hardisty", 2010, 2011, kind="MS")}

for ii in set(x._kind for x in kSTUDENTS.values()):
    sorted_students = list(sorted(kSTUDENTS.values(), key=lambda x: x._start))
    global_replace["%s%s%sSTUDENTS" % ("LATEX", ii, "CUR")] = \
      "\\begin{itemize}\n %s \n\\end{itemize}" % \
      "\n".join("\item %s" % x.latex() for x in sorted_students
                if x._end >= datetime.now().year and x._kind == ii)

    global_replace["%s%s%sSTUDENTS" % ("LATEX", ii, "PAST")] = \
      "\\begin{itemize}\n %s \n\\end{itemize}" % \
      "\n".join("\item %s" % x.latex() for x in sorted_students
                if x._end < datetime.now().year and x._kind == ii)

    global_replace["%s%s%sSTUDENTS" % ("HTML", ii, "PAST")] = \
      "<UL>\n %s \n</UL>" % \
      "\n".join("<LI>%s</LI>" % x.html() for x in sorted_students
              if x._end < datetime.now().year and x._kind == ii)

    global_replace["%s%s%sSTUDENTS" % ("HTML", ii, "CUR")] = \
      "<UL>\n %s \n</UL>" % \
      "\n".join("<LI>%s</LI>" % x.html() for x in sorted_students
              if x._end >= datetime.now().year and x._kind == ii)


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
    name = name.replace('\\"{a}', "&auml;")
    name = name.replace('\\"a', "&auml;")
    name = name.replace('\\"{o}', "&ouml;")
    name = name.replace('\\"o', "&ouml;")
    name = name.replace('\\"{e}', "&euml;")
    name = name.replace('\\"e', "&euml;")
    name = name.replace("\\'{e}", "&eacute;")
    name = name.replace("\\'e", "&eacute;")
    name = name.replace("{", "")
    name = name.replace("}", "")

  return name

class IndexElement:
  def __init__(self, file_contents):
    self.fields = defaultdict(list)
    for ii in [x for x in file_contents.split("~~") if x != ""]:
      key = capwords(ii.split("|")[0].strip())
      if not key in self.fields:
        self.fields[key] = []
      val = ii.split("|")[1].strip()
      if key == "Author":
        for jj in val.split(" and "):
          self.fields["Authors"].append(jj)
      self.fields[key].append(val)

  def author_string(self, latex):
    s = ""
    if "Authors" in self.fields and len(self.fields["Authors"]) > 0:
      assert "Year" in self.fields
      authors = [format_name(kSTUDENTS, x, self.fields["Year"][0], latex) \
                   for x in self.fields["Authors"]]
      if len(authors) > 2:
        s += ", ".join(authors[:-1]) + ", and " + authors[-1]
      elif len(authors) == 2:
        s += " and ".join(authors)
      elif len(authors) == 1:
        s += authors[0]
      s += ".  "
    return s

  def wrapper_document(self, url_prefix):
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

    ~~~public~~~

    ~~~note~~~

    ~~~links~~~

    \\vspace{3cm}
    Downloaded from ~~~url~~~  \\\\
      
    \\vspace{2cm}
    \\textit{Contact Jordan Boyd-Graber (jbg@boydgraber.org) for questions about this paper.}

    \\includepdf[pages={-}]{src_~~~filename~~~}

    \\end{document}
    """

    s = s.replace("~~~citation~~~", self.latex(url_prefix=url_prefix, acceptance = False))
    s = s.replace("~~~filename~~~", self.fields["Url"][0])
    s = s.replace("~~~bibtex~~~", self.bibtex(url_prefix))

    if "Public" in self.fields:
      s = s.replace("~~~public~~", "{\\bf Accessible Abstract:} %s\\\\" % "\n".join(self.fields["Public"]))
    else:
      s = s.replace("~~~public~~~", "")

    if "Note" in self.fields:
      s = s.replace("~~~note~~~", "{\\bf %s}\\\\"
                    % "".join(self.fields["Note"]))
    else:
      s = s.replace("~~~note~~~", "")

    if "Link" in self.fields and len(self.fields["Link"]) > 0:
      link_string = "\\noindent Links:\n\\begin{itemize}\n"
      for ii in self.fields["Link"]:
          title, location = ii.split("*")

          if not location.startswith("http"):
              location = "%s%s" % (url_prefix, location)
          link_string += "\\item \\href{%s}{%s} [\\url{%s}]\n" % \
            (location, title, location)
      link_string += "\n\\end{itemize}\\"
      s = s.replace("~~~links~~~", link_string)
    else:
      s = s.replace("~~~links~~~", "")

    if "Url" in self.fields:
      target = self.fields["Url"][0]
      if not target.startswith("http"):
          target = "%s%s" % (url_prefix, target)
      s = s.replace("~~~url~~~", "\\url{%s}" % target)
    else:
      s = s.replace("~~~links~~~", "")

    
    return s.encode("ascii", "ignore")

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

    return remove_html_chars(text)

  def latex(self, url_prefix="", acceptance=True):
    s = self.author_string(True)
    if "Title" in self.fields:
      if "Url" in self.fields and url_prefix:
          if self.fields["Url"][0].startswith("http"):
              s += '{\\bf \\href{%s}{%s}}.  ' % (self.fields["Url"][0], self.fields["Title"][0])
          else:
              s += '{\\bf \\href{%s/%s}{%s}}.  ' % (url_prefix, self.fields["Url"][0], self.fields["Title"][0])
      else:
          s += '{\\bf %s}.  ' % (self.fields["Title"][0])
    if "Booktitle" in self.fields:
      s += "\\emph{%s}, " % self.fields["Booktitle"][0]
    if "Journal" in self.fields:
      s += "\\emph{%s}, " % self.fields["Journal"][0]
    if "Year" in self.fields:
      s += self.fields["Year"][0]
    if "Numpages" in self.fields:
        s += ", %i pages" % int(self.fields["Numpages"][0])

    if "Acceptance" in self.fields and acceptance:
      s += " (" + self.fields["Acceptance"][0] + "\% Acceptance Rate)"

    s += "."
    s += "\n\n"
    return s

  def year(self):
    s = ""
    if "Year" in self.fields and self.fields["Year"][0].strip() != "":
      s += self.fields["Year"][0]
    return s

  def html(self, bibtex, url_prefix, section):
    s = self.author_string(False)

    formatted_title = self.fields["Title"][0].replace("``", "&quot;").replace("\dots", "&hellip;").replace("~", "&nbsp;").replace("\=o", "&omacr;")
    if "Title" in self.fields and "Url" in self.fields:
      url = self.fields["Url"][0]
      if url.startswith("http"):
          s += "<b><a href=\"%s\">%s</a></b>.  " % (url, formatted_title)
      else:
          url = "%s/%s" % (url_prefix, url)
          s += "<b><a href=\"%s\"  onClick=\"javascript: pageTracker._trackPageview('%s'); \">%s</a></b>.  " % \
            (url, url, formatted_title)
    elif "Title" in self.fields:
      s += '<b>%s</b>.  ' % formatted_title

    if "Booktitle" in self.fields:
      s += "<i>%s</i>, " % self.fields["Booktitle"][0]

    if "School" in self.fields:
      s += "<i>Ph.D. thesis, %s</i>, " % self.fields["School"][0]

    if "Journal" in self.fields:
      s += "<i>%s</i>, " % self.fields["Journal"][0]
    if "Year" in self.fields and self.fields["Year"][0].strip() != "":
      s += self.fields["Year"][0]
      s += "."

    s = s.replace("{", "")
    s = s.replace("}", "")

    for ii in self.fields["Link"]:
      text, url = ii.split("*")
      if url.startswith("http"):
        s += ' [<a href="%s">%s</a>]' % (url, text)
      else:
        s += ' [<a href="../%s">%s</a>]' % (url, text)

    div_name = str(hash("".join("".join(x) for x in self.fields.values()) + str(section)))
    if bibtex and len(self.fields["Bibtex"]) > 0:
      s += ' [<a href="javascript:unhide('
      s += "'%s'" % div_name
      s += ');">Bibtex</a>]\n'
      s += '<div id="'
      s += "%s" % div_name
      s += '" class="hidden">\n'
      s += "<br><PRE>\n" + self.bibtex(url_prefix) + "</PRE>\n"
      s += '</div>'

    if "Note" in self.fields:
      s += "<B>%s</B>\n" % "".join(self.fields["Note"])

    if "Embed" in self.fields:
        s += "\n<BR>" + "<CENTER>%s</CENTER>" % "".join(self.fields["Embed"])

    return s

  def bibtex(self, url_prefix):
    s = "@%s{%s,\n" % (self.fields["Bibtex"][0], ":".join(bibtex_last(x) for x in self.fields["Authors"]) + "-" + self.fields["Year"][0])
    for ii in self.fields:
      if ii in ["Author", "School", "Journal", "Pages", "Volume", "Year", "Number", "ISSN",
                "Abstract", "Location", "Title", "Series", "Booktitle", "Isbn", "Publisher",
                "Address", "Editor"]:
        s += "\t%s = {%s},\n" % (ii, self.fields[ii][0])
      if ii.lower() == "url":
          assert url_prefix != self.fields[ii][0], "Badly formed URL  %s/%s" % (url_prefix, self.fields[ii][0])
          if self.fields[ii][0].startswith("http"):
              s += "\t%s = {%s},\n" % (ii, self.fields[ii][0])
          else:
              s += "\t%s = {%s/%s},\n" % (ii, url_prefix, self.fields[ii][0])
    s += "}\n"
    return s

  def keys(self, name, criteria):
    """
    Create keys that can be sorted
    """

    try:
      year = -int(self.fields["Year"][0])
    except ValueError:
      year = float("-inf")

    if "Booktitle" in self.fields and len(self.fields["Booktitle"]) > 0:
        venue = self.fields["Booktitle"][0]
    else:
        venue = ""

    if "Journal" in self.fields and len(self.fields["Journal"]) > 0:
        venue += self.fields["Journal"][0]
    else:
        venue += ""

    keys = [(x, year, venue, self.fields["Title"][0], name) for \
              x in self.fields[criteria]]

    return keys

class WebsiteWriter:
  def __init__(self, source, output, header_file, footer_file, site_title, url, last_modified):
    self.STATIC_DIR = "static"
    self.DYNAMIC_DIR = "dyn-"

    # start populating the replacement dictionary
    global_replace["SITETITLE"] = site_title
    global_replace["TIMESTAMP"] = last_modified

    self._source = source
    self._output = output
    self._header = open(header_file).read()
    self._footer = open(footer_file).read()

    self._url = url

    self._files = {}
    self._indexed = {}
    self._criteria = {}
    self._default_sort = {}

    for ii in glob(source + "*.html"):
      print("Adding file %s" % ii)
      name = capwords(ii.split("/")[-1].replace(".html", "").replace("_", " "))
      self._files[name] = ii

  def footer(self):
    html_out = self._footer
    for variable in global_replace:
        html_out = html_out.replace("~~%s~~" % variable,
                                    global_replace[variable])
    return html_out

  def navigation(self, prefix):
    s = "<ul>"
    keys = [x for x in self._files.keys() if x != "Home"]
    keys += self._indexed.keys()
    keys = sorted(keys, key=lambda s: s.lower())

    for ii in keys:
      if ii in self._files:
        s += ('\t<li><a href="%s' + self.STATIC_DIR + '/%s">%s</a>\n') % \
            (prefix, self._files[ii].split("/")[-1], ii)
      else:
        s += ('\t<li><a href="%s' + self.DYNAMIC_DIR + '%s/%s.html">%s</a>\n') % \
            (prefix, ii, self._default_sort[ii], ii.title())
    s += "</ul>\n"
    return s

  def add_raw(self, path, prefix):
      contents = []
      for ii in glob(path):
          val = self.write_file(self._output + ii, "UNTITLED", ii, prefix,
                                use_header=False, use_footer=False)
          contents.append(val)
      return contents

  def add_index(self, path, name = "Documents", criteria=[("Year", 0, [])],
                default_sort="Year"):
    index = {}
    print("Searching: " + path + "*")
    for ii in glob(path + "*"):
      if "~" in ii or "#" in ii or "." in ii:
        # Don't go through backup files
        continue
      try:
        item = IndexElement(open(ii).read())
      except UnicodeDecodeError:
        print("Encode error on %s" % ii)
        try:
          item = IndexElement(open(ii, encoding="utf-8").read())
        except UnicodeDecodeError:
          print("Skipping unicode error %s" % ii)
          time.sleep(60)
          continue
      if "Nopub" in item.fields:
          print("Skipping %s" % ii)
          continue
      else:
          index[ii] = item

      if "Url" in index[ii].fields and index[ii].fields["Url"]:
        try:
          resource = index[ii].fields["Url"][0].split("/")[1].split(".")[0]
        except IndexError:
          print("Cannot parse: %s" % index[ii].fields["Url"][0])
        o = open("pubs/%s.tex" % resource, 'wb')
        print("pubs/%s.tex" % resource)
        o.write(index[ii].wrapper_document(self._url))

    self._indexed[name.lower()] = index
    self._criteria[name.lower()] = criteria
    self._default_sort[name.lower()] = default_sort.lower()

  def write_index(self, index, bibtex=True):
    print("Creating index for %s from %s" % (index, str(self._criteria.keys())))

    final_directory = (self._output + "/" + self.DYNAMIC_DIR +
                       index.lower())
    try:
      print("Making dir %s" % final_directory)                
      os.mkdir(final_directory)
    except OSError:
      print("Dir couldn't be made: " + final_directory)
    
    for sort_by, min_count, exclude in self._criteria[index.lower()]:
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
        keys += contrib
        for kk in contrib:
          assert not kk in lookup, "%s already found as %s.  Look for a repeated key in the pub file (e.g., year)" % (str(kk), lookup[kk].txt())
          lookup[kk] = self._indexed[index.lower()][jj]

      primary = [x[0] for x in keys]
      primary = [x for x in primary if \
                   len([y for y in primary if y==x]) > min_count and \
                   not x in exclude]
      keys = [x for x in keys if x[0] in primary]
      keys.sort()
      if sort_by == "Year":
        keys.reverse()

      html_out = self._header.replace("~~PAGETITLE~~", \
                                      '%s (%s)' % (index, sort_by))
      html_out = html_out.replace("~~NAVIGATION~~", self.navigation("../"))
      html_out = html_out.replace("~~PATHPREFIX~~", "../")
      html_out += '<div id="content">\n'
      html_out += '<h1 id="header"> %s (%s) </h1>\n' % (index, sort_by)

      html_out += "<center>Sort by:"
      for jj in self._criteria[index.lower()]:
        html_out += ' <a href="%s.html">%s</a>' % (jj[0].lower(), jj[0])
      html_out += "</center>\n"

      for variable in global_replace:
          html_out = html_out.replace("~~%s~~" % variable,
                                      global_replace[variable])
      o.write(html_out)
      html_out = ""

      old = None
      for jj in keys:
        year = lookup[jj].year()
        if old != jj[0]:
          if jj[0] == "":
              continue

          # We're starting a new section, flush the cache
          if jj != keys[0]:
            latex_out.write("\n\\end{enumerate}\n}")
            o.write(html_out)
            o.write("\t</ul> <!----- Ending section: %s ------>" % str(old))
            global_replace["%s:%s" % (index, txt_name)] = html_out

            html_out = ""

          # The asterisk if a field separator, so it has slightly different formatting
          if not "*" in jj[0]:
            latex_name = format_name([], jj[0], -1, True)
            txt_name = format_name([], jj[0], -1, False)
            o.write("\t<h2>%s</h2>\n\t<ul>\n" % txt_name)
          else:
            o.write('\t<h2><a href="%s">%s</a></h2>\n\t<ul>\n' % (jj[0].split("*")[1],
                                                                  jj[0].split("*")[0]))
            txt_name = format_name([], jj[0].split("*")[0], -1, False)
            latex_name = format_name([], jj[0].split("*")[0], -1, True)

          # Write out the headers
          bibtex_out.write("\n\n% ")
          bibtex_out.write(txt_name)
          bibtex_out.write("\n\n\n")
          text_out.write(remove_html_chars(txt_name))
          text_out.write("\n-------------------------\n\n")
          if latex_name in UMD_MAPPING:
              latex_out.write("\n\\headedsection{{\\bf %s}}{}{\n\n" % UMD_MAPPING[latex_name])
          else:
              latex_out.write("\n\\headedsection{{\\bf %s}}{}{\n\n" % latex_name)

          latex_out.write("\n\\begin{enumerate}\n")

        latex_out.write("\t \item " + lookup[jj].latex(self._url))
        bibtex_out.write(lookup[jj].bibtex(self._url))
        text_out.write(lookup[jj].txt(url=self._url))

        # Write comment string so we know original entry in DB
        this_html = "\n\t\t<!--- %s --->\n" % str(jj)
        this_html += "\t\t<li>%s</li>\n" % lookup[jj].html(bibtex, self._url, old)
        global_replace["%s:%s:%s" % (index, txt_name, year)] += this_html
        html_out += this_html
        old = jj[0]

      # For the last entry, we need to flush the cache
      global_replace["%s:%s" % (index, txt_name)] = html_out
      o.write(html_out)
      html_out = ""

      latex_out.write("\n\\end{enumerate}")
      latex_out.write("\n}")
      o.write("\t</ul>\n")
      o.write("<p>&nbsp;</p>\n")
      o.write('<center><a href="%s.txt">LaTeX Version</a>&nbsp;' % sort_by.lower())
      o.write('<a href="%s.bib">BibTex Version</a>&nbsp;' % sort_by.lower())
      o.write('<a href="%s_raw.txt">Text Version</a></center>' % sort_by.lower())

      o.write("<p>&nbsp;</p>\n")
      o.write("</div>")
      o.write(self.footer())
      o.close()

  def unindexed_directory(self, source_path, target_path):
    final_directory = self._output + self.STATIC_DIR + "/" + target_path
    try:
      os.mkdir(final_directory)
    except OSError:
      print("Dir couldn't be made: " + final_directory)

    for ii in glob(source_path + "/*.html"):
      filename = final_directory + "/" + ii.split("/")[-1]
      print("Writing non-indexed file: " + filename)
      self.write_file(filename, ii.split("/")[-1].replace(".html", ""), ii,
                      "../../")

  def write_file(self, filename, title, raw, prefix="../", use_header=True, use_footer=True):
    if use_header:
        contents = self._header
    else:
        contents = ""

    contents += open(raw, encoding='utf-8').read()

    for variable in global_replace:
      search = "~~%s~~" % variable

      if search in contents:
        print("Found %s in %s" % (search, filename))
        contents = contents.replace(search, global_replace[variable])

    if use_footer:
        contents += self.footer()

    contents = contents.replace("~~NAVIGATION~~", self.navigation(prefix))
    contents = contents.replace("~~PATHPREFIX~~", prefix).replace("~~PAGETITLE~~", title)

    print("Writing %s to %s" % (raw, filename))
    o = open(filename, 'w', encoding='utf-8')
    o.write(contents)
    o.close()

    return contents

  def write(self):
    try:
      os.mkdir(self._output + self.STATIC_DIR)
    except OSError:
      print("Couldn't make " + self._output + self.STATIC_DIR)

    # Write dynamic files (needs to happen first to build macros)
    for ii in self._indexed:
      path = self._output + "/" + self.DYNAMIC_DIR + "%s" % ii
      try:
        os.mkdir(path)
      except OSError:
        print("Cannot make directory: " + path)

    # Write the static files
    for ii in self._files:
      self.write_file(self._output + self.STATIC_DIR + "/%s.html" % ii.lower().replace(" ", "_"), ii, self._files[ii])

      # Put the main file one directory up
      if ii.lower() == "home":
        self.write_file(self._output + "/index.html", ii, self._files[ii], "")
