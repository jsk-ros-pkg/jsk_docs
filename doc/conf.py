# -*- coding: utf-8 -*-
#
import sys
import os
import glob
import shutil
import shlex
import subprocess
import yaml

from recommonmark.parser import CommonMarkParser


on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

extensions = [
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']

source_parsers = {
    '.md': CommonMarkParser,
}
source_suffix = ['.rst', '.md']

master_doc = 'index'
project = u'jsk_docs'
copyright = u'2015, JSK Lab'
author = u'Kei Okada'
version = '1.0'
release = '1.0'
language = 'en'

exclude_patterns = ['_build', 'venv', 'README.md']


index_text="""
==========
{local_name}
==========

{local_name} is common stacks used in JSK lab.

.. raw:: html

   <h2>
   Search docs!
   </h2>


.. raw:: html

  <script>
    (function() {{
      var cx = '004597581434396922146:u8zamng695e';
      var gcse = document.createElement('script');
      gcse.type = 'text/javascript';
      gcse.async = true;
      gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
          '//cse.google.com/cse.js?cx=' + cx;
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(gcse, s);
    }})();
  </script>
  <gcse:search></gcse:search>

.. raw:: html

   <h2>
   <a href="{uri}/issues">Ask question!</a>
   </h2>

The code is open source, and `available on github`_.

.. _available on github: {uri}
.. _github issue: {uri}/issues

:doc:`inverse_lookup` should be useful for you

This repository contains following ros packages:


.. toctree::
   :maxdepth: 2

"""

## get repositories and auto gen readme doc
try:
    filename = 'doc.rosinstall'
    stream = open(filename, 'r')
    repos = yaml.load(stream)
except:
    print >>sys.stderr, "Unexpected error:", sys.exc_info()[0]
    sys.exit(1)
with open("index.rst", "w") as f:
    f.write(index_text.format(local_name="jsk_docs", uri="https://github.com/jsk-ros-pkg/jsk_docs"))
for repo in repos:
    # setup repo
    local_name = repo['git']['local-name']
    uri = os.path.splitext(repo['git']['uri'])[0]
    version = repo['git']['version'] if repo['git'].has_key('version') else 'master'
    print("wrokin on name:{} uri:{} branch:{}".format(local_name, uri, version))
    if os.path.exists(local_name):
        subprocess.call(['git', 'fetch', '--all'], cwd=local_name)
    else:
        subprocess.call(['git', 'clone', '--depth=1', uri, local_name, '-b', version])
    subprocess.call(['git', 'clean', '-xfd'], cwd=local_name)
    subprocess.call(['git', 'reset', '--hard', 'origin/%s' % version], cwd=local_name)

    if "/" not in local_name:
        with open("index.rst", "a") as f:
            f.write("   %s/doc/index\n"%(local_name))
    # add index.rst if not exists
    index = os.path.join(local_name, "doc", "index.rst")
    if not os.path.exists(index):
        print("Add %s"%(index))
        if not os.path.exists(os.path.dirname(index)):
            os.mkdir(os.path.dirname(index))
        with open(index, "a") as f:
            f.write(index_text.format(local_name=local_name, uri=uri))

    # for each README.md
    for root, dirs, files in os.walk(local_name):
        for file in files:
            if file.endswith("README.md") and not root.startswith(os.path.join(local_name, "doc")):
                symlink_dir = os.path.join(local_name, "doc", root[len(local_name)+1:]) # repo/doc/pkg, not repo/doc/repo/pkg
                symlink_file = os.path.join(symlink_dir, file)
                target_file = os.path.join(root, file)
                print "-",target_file, symlink_file, root
                if os.path.exists(symlink_dir):
                    print("Skipping %s, which is already existing"%(symlink_dir))
                elif root == local_name and os.path.exists(target_file) and not os.path.exists(symlink_file):
                    print ("Creating symlink for %s"%symlink_file)
                    os.symlink(os.path.relpath(os.path.join(target_file),os.path.dirname(symlink_file)), symlink_file)
                    with open(index, "a") as f:
                        f.write("   %s\n"%("README.md"))
                else:
                    # copy directory
                    shutil.copytree(root, symlink_dir)
                    print ("Copying directries %s"%symlink_file)
                    with open(index, "a") as f:
                        f.write("   %s\n"%(os.path.join(root[len(local_name)+1:],file)))

    # hrpsys
    if local_name == "hrpsys-base":
        build_dir = os.path.join('_build', 'html', 'hrpsys-base-api')
        if not os.path.exists(build_dir):
            os.mkdir(build_dir)
        if not os.path.exists(build_dir):
            os.makedirs(os.path.dirname(build_dir))
            shutil.copytree('hrpsys', build_dir)
        with open(index, "a") as f:
            f.write("\n")
            f.write("`API Documents <../../hrpsys-base-api/html>`_\n")

    # euslisp
    if local_name == "jskeus":
        doc_dir=os.path.join('jskeus', 'doc');
        build_dir = os.path.join('_build', 'html', 'jskeus', 'doc', 'html')
        if not os.path.exists(build_dir):
            os.makedirs(os.path.dirname(build_dir))
            shutil.copytree('jskeus', build_dir)
        with open(index, "a") as f:
            f.write("\n")
            f.write("`API Documents <html>`_\n")

# Add image tables in index page for nodes
this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir)
import add_img_tables_to_index
if (not on_rtd) and subprocess.check_output(['git', 'diff']):
    print('skipping adding image tables because there is changes in VCS')
else:
    cwd = os.path.abspath(os.getcwd())
    for repo in os.listdir(this_dir):
        doc = os.path.join(cwd, repo, 'doc')
        if not os.path.exists(doc):
            continue
        print("adding image table for '{doc}'".format(doc=doc))
        os.chdir(doc)
        add_img_tables_to_index.main(exclude_patterns)
    os.chdir(cwd)

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'jsk_docsdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': "".join((
        '\usepackage[utf8]{inputenc}',
        # NO-BREAK SPACE
        '\DeclareUnicodeCharacter{00A0}{ }',
        # BOX DRAWINGS LIGHT VERTICAL AND RIGHT
        '\DeclareUnicodeCharacter{251C}{+}',
        # BOX DRAWINGS LIGHT UP AND RIGHT
        '\DeclareUnicodeCharacter{2514}{+}',
    )),

# Latex figure (float) alignment
#'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'jsk_docs.tex', u'jsk_docs Documentation',
   author, 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'jsk_docs', u'JSK Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'jsk_docs', u'JSK Documentation',
   author, 'jsk_docs', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The basename for the epub file. It defaults to the project name.
#epub_basename = project

# The HTML theme for the epub output. Since the default themes are not optimized
# for small screen space, using the same theme for HTML and epub output is
# usually not wise. This defaults to 'epub', a theme designed to save visual
# space.
#epub_theme = 'epub'

# The language of the text. It defaults to the language option
# or 'en' if the language is not set.
#epub_language = ''

# The scheme of the identifier. Typical schemes are ISBN or URL.
#epub_scheme = ''

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#epub_identifier = ''

# A unique identification for the text.
#epub_uid = ''

# A tuple containing the cover image and cover page html template filenames.
#epub_cover = ()

# A sequence of (type, uri, title) tuples for the guide element of content.opf.
#epub_guide = ()

# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_pre_files = []

# HTML files shat should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_post_files = []

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# The depth of the table of contents in toc.ncx.
#epub_tocdepth = 3

# Allow duplicate toc entries.
#epub_tocdup = True

# Choose between 'default' and 'includehidden'.
#epub_tocscope = 'default'

# Fix unsupported image types using the Pillow.
#epub_fix_images = False

# Scale large images.
#epub_max_image_width = 0

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#epub_show_urls = 'inline'

# If false, no index is generated.
#epub_use_index = True

def setup(app):
    app.add_stylesheet('search-button.css')
