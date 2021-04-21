The two scripts, step1-getEBooks.py and step2-convertToTei.py, were developed to collect the resource CIDRE. In the first step, books in epub format are downloaded, and during the second step these books are formatted into text files from which content which is not part of the novel itself, such as the preface, is removed. 

This software is distributed under a GNU General Public License (GPLv3). 

The developers of these scripts are Philippe Gambette and Olga Seminck. 


# step1-getEBooks.py

Download a list of eBooks from projects such as Gutenberg, Wikisource, BeQ or Gallica (only when the ePub format exists).

Requires to install selenium and the "gecko" driver:
* pip3 install selenium
* install "geckodriver" from https://github.com/mozilla/geckodriver/releases

To start downloading a list of eBooks:
* create a new directory at the same level as the scripts and call it 'corpus'. 
* empty the variable `alreadyDownloaded`: replace the current definition starting on line 61 by `alreadyDownloaded=[]`
* remplace the content of the variable `booksToDownload` by the list of URLs of books to download or by a list of lists with 2 elements: first the URL to download, then the file name to use to save the file. There are two examples of 'booksToDownload' provided in the two formats (line 82 and 102).
* Simply execute the following command: python step1-getEBooks.py 

Tested on Windows 10 and MacOs


# step2-convertToTei.py

Convert ePub e-books into XML-TEI using Pandoc and into TXT format, cleaning header and footer from the download source, image captions and footnotes

The books must be stored in a folder named `corpus` in the same folder as this script.

Requires to install pandoc from https://pandoc.org/installing.html

To clean the e-books:
* Simply execute the following command: python step2-convertToTei.py 

Tested on Windows 10 and MacOs
