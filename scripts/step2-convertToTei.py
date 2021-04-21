#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import glob, os, re, sys, time, requests, subprocess
from xml.dom import minidom


"""
    GetCorpus, a script to automatically download and clean ePub ebooks
    from projects such as Gutenberg, Wikisource, BeQ or Gallica digital libraries
    Copyright (C) 2020-2021 Philippe Gambette, Olga Seminck

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
"""

documentNb = 0

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

def containsText(node,string):
   found = False;
   if node.childNodes.length == 0:
      data = ""
      try:
         data = node.data
      except:
         pass
      if string in data:
         found = True
   else:
      for child in node.childNodes:
         found = found or containsText(child,string)
   return found

# get the text inside the XML node
def displayNodeText(node,output):
   if node.childNodes.length == 0:
      data = ""
      if output:
         try:
            data = node.data
         except:
            pass
      if node.nodeName.lower()=="lb":
         if node.getAttribute("rend")=="hyphen":
            data = "<hyphen>"
         else :
            data = "\n"
      return data
   else:
      text = ""
      displayByDefault = True

      # Do not display the content of ref tags (footnotes, in Gutenberg eBooks)
      if node.nodeName.lower() == "ref":
         displayByDefault = False

      # Special cases for p tags
      if node.nodeName.lower() == "p":
         # Remove header of Project Gutenberg eBooks
         if containsText(node,"The Project Gutenberg EBook of") or containsText(node,"and the Online Distributed") or containsText(node,"This file was produced") or containsText(node,"from images generously") or containsText(node,"START OF THE PROJECT GUTENBERG EBOOK"):
            displayByDefault = False
            text = "<DeleteEverythingBeforeThis>"
         # Remove footer of Project Gutenberg eBooks
         if containsText(node,"End of the Project Gutenberg") or containsText(node,"END OF THIS PROJECT GUTENBERG EBOOK") or containsText(node,"End of Project Gutenberg") or containsText(node,"END OF THE PROJECT GUTENBERG EBOOK"):
            displayByDefault = False
            text = "<DeleteEverythingAfterThis>"
         # Remove header of BeQ eBooks
         if containsText(node,"Collection À tous les vents"):
            displayByDefault = False
            text = "<DeleteEverythingBeforeThis>"
         # Remove footer of BeQ eBooks
         if containsText(node,"Cet ouvrage est le ") and containsText(node,"e publié"):
            displayByDefault = False
            text = "<DeleteEverythingAfterThis>"
         # Remove tag p containing "image pas disponible" for Project Gutenberg eBooks
         try:
            if node.childNodes[0].data == "image pas disponible":
               displayByDefault = False
         except:
            pass
         # Remove tag p containing a footnote (for Wikisource or for Project Gutenberg eBooks)
         try:
            if node.childNodes[0].nodeName.lower() == "ref" or node.childNodes[1].nodeName.lower() == "ref" or node.childNodes[2].nodeName.lower() == "ref":
               displayByDefault = False
         except:
            pass
         # Remove tag p containing a tag figure child (useful for Wikisource and for Gallica eBooks)
         if node.childNodes[0].nodeName.lower() == "figure":
            displayByDefault = False
         # Remove tag p containing "..................................................................." for BEQ eBooks (Zevaco for example).
         try:
            if node.childNodes[0].data == "...................................................................":
               displayByDefault = False
         except:
            pass
        # Sometimes there are more points...
         try:
            if node.childNodes[0].data == ".......................................................................":
               displayByDefault = False
         except:
            pass
        # Remove paragraph separations in BeQ marqued by *
         try:
            if node.childNodes[0].data == "*":
               displayByDefault = False
         except:
            pass

      # Special cases for head tags
      if node.nodeName.lower() == "head":
         # Remove head tag starting with PAG_ or ending with .jpg for Gallica Ebooks
         if containsText(node,"PAG_") or containsText(node,".jpg"):
            displayByDefault = False
         # Remove everything before head tag containing "Exporté de Wikisource" for Wikisource Ebooks
         if containsText(node,"Exporté de Wikisource"):
            displayByDefault = False
            text = "<DeleteEverythingBeforeThis>"
         # Remove everything after head tag containing "À propos de cette édition électronique" for Wikisource Ebooks
         if containsText(node,"À propos de cette édition électronique"):
            displayByDefault = False
            text = "<DeleteEverythingAfterThis>"
         
      if node.nodeName.lower() == "l":
         text = " \n"
      if node.nodeName.lower() == "choice":
         text = "<c>"
      for child in node.childNodes:
         if child.nodeName.lower() == "text":
            text += displayNodeText(child,True and displayByDefault)
         else :
            # ignore the content of these tags
            if child.nodeName.lower() == "orig" or child.nodeName.lower() == "fw" or child.nodeName.lower() == "abbr" or child.nodeName.lower() == "sic":
               text += displayNodeText(child,False and displayByDefault)
            else:
               text += displayNodeText(child,output and displayByDefault)
               
      if node.nodeName.lower() == "choice":
         text += "<c>"
      
      if node.nodeName.lower() == "placename":
         nodeType = ""
         if node.hasAttribute("type"):
            nodeType = ' type="'+node.getAttribute("type")+'"'
         return "<placename"+nodeType+">"+text+"</placename>"
      else :
         return text

# get the text without sequences of whitespaces
def cleanText(text):
   table = text.split("\n")
   result = ""
   regex = "(.*) [ ]+(.*)"
   for line in table:
      line = line.replace("	"," ")
      res = re.search(regex,line)
      while res:
         line = res.group(1)+" "+res.group(2)
         res = re.search(regex, line)
      result += line
   result = result.replace("- <hyphen>","")
   result = result.replace(" <hyphen>","")
   result = result.replace("<hyphen>","")   
   result = result.replace("<c>"," ")   
   res = re.search(regex,result)
   while res:
     result = res.group(1)+" "+res.group(2)
     res = re.search(regex, result)
   return result

#extension = "txt"
extension = "tei"

# Consider all epub files in the corpus folder
for file in glob.glob(os.path.join(os.path.join(folder, "corpus"), "*.epub")):
   print("Converting " + file + " to " + extension)
   # Convert to XML-TEI or TXT with pandoc
   try:
      print("pandoc -s \"" + file + "\" -o \"" + file + "." + extension + "\"")
      result = subprocess.check_output("pandoc -s \"" + file + "\" -o \"" + file + "." + extension + "\"", shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
      if extension == "tei":
         mydoc = minidom.parse(file + ".tei")
         # Get the cleaned text of the XML-TEI file 
         book = displayNodeText(mydoc.getElementsByTagName('text')[0],True)
         endOfBook = book.find("<DeleteEverythingAfterThis>")
         if endOfBook >= 0:
            book = book[0:endOfBook]
         startOfBook = 0
         while startOfBook >= 0:
            startOfBook = book.find("<DeleteEverythingBeforeThis>")
            if startOfBook >= 0:
               book = book[startOfBook+28:len(book)]
         # Write the clean text into a text file
         outputFile = open(os.path.join(file + ".txt"),"w",encoding="utf-8")
         outputFile.writelines(book)
         outputFile.close()
   except subprocess.CalledProcessError as e:
      raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
      pass
