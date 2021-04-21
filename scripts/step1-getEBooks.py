#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import glob, os, re, sys, time, requests, shutil


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

# pip3 install selenium
# install "geckodriver" from https://github.com/mozilla/geckodriver/releases
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile



# Get the current folder
# The downloaded books will be placed in a folder named corpus inside this folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))


# Load a profile to automatically accept ePub downloads
profile = FirefoxProfile()
profile.set_preference("browser.download.panel.shown", False)
#profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/epub+zip")
profile.set_preference("browser.download.folderList", 2);
# Download files in the corpus folder
profile.set_preference("browser.download.dir", os.path.join(folder,"corpus"))
try:
   # May not work for MacOS but required to automatically download Wikisource files on Windows
   driver = webdriver.Firefox(firefox_profile=profile)
except:
   # Should work for MacOS
   driver = webdriver.Firefox()
   pass

# Specify a 15 second timeout to avoid getting stuck after each download
driver.set_page_load_timeout(15)


# An example of how the variable alreadyDownload can be used
alreadyDownloaded=["https://beq.ebooksgratuits.com/vents-epub/Sand_Indiana.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Valentine.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Lelia.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Le_secretaire_intime.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-Andre.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Leone_Leoni.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Simon.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Mauprat.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_La_derniere_Aldini.epub",
"https://beq.ebooksgratuits.com/vents-epub/sand-mosaiste.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Horace.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-Consuelo-1.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-Consuelo-2.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-Consuelo-3.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-comtesse-1.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-comtesse-2.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-Jeanne.epub",]



# An example of the variable booksToDownload without renaming
booksToDownload=[
"https://beq.ebooksgratuits.com/vents-epub/Sand-Kourroglou.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Le_meunier_dAngibault.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_La_Mare_au_Diable.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Teverino.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Lucrezia_Floriani.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Le_peche_de_M._Antoine.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_La_petite_Fadette.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Francois_le_champi.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Le_chateau_des_Desertes.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Les_maitres_sonneurs.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_La_derniere_Aldini.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Elle_et_lui.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-dernier_amour.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Francia.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand_Nanon.epub",
"https://beq.ebooksgratuits.com/vents-epub/Sand-Marianne.epub",
]

# An example of the variable booksToDownload with renaming
booksToDownload=[["http://beq.ebooksgratuits.com/vents-epub/Verne-Chanteleine.epub","1862_Le_comte_de_Chanteleine"],
["https://beq.ebooksgratuits.com/vents-epub/Verne_Cinq_semaines_en_ballon.epub","1863_Cinq_Semaines_en_ballon"],
["https://beq.ebooksgratuits.com/vents-epub/Verne_Voyage_au_centre_de_la_terre.epub","1864_Voyage_au_centre_de_la_Terre"],
["https://beq.ebooksgratuits.com/vents-epub/Verne_De_la_terre_a_la_lune.epub","1865_De_la_Terre_a_la_Lune"],
["http://beq.ebooksgratuits.com/vents-epub/Verne_Voyages_et_aventures_du_capitaine_Hatteras.epub","1866_Les_Aventures_du_capitaine_Hatteras"],
["https://beq.ebooksgratuits.com/vents-epub/Verne_Les_enfants_du_capitaine_Grant.epub","1868_Les_Enfants_du_capitaine_Grant"],
["https://beq.ebooksgratuits.com/vents-epub/Verne_Autour_de_la_lune.epub","1870_Autour_de_la_Lune"],
["https://beq.ebooksgratuits.com/vents-epub/Verne_Vingt_mille_lieues_sous_les_mers.epub","1870_Vingt_mille_lieues_sous_les_mers"],
["https://wsexport.wmflabs.org/?lang=fr&format=epub&page=Les+Forceurs+de+blocus","1871_Les_Forceurs_de_blocus"],
["https://beq.ebooksgratuits.com/vents-epub/Verne_Une_ville_flottante.epub","1871_Une_ville_flottante"],
["https://beq.ebooksgratuits.com/vents-epub/Verne-Afrique.epub","1872_Aventures_de_trois_Russes_et_de_trois_Anglais"],
["https://beq.ebooksgratuits.com/vents-epub/Verne_Le_tour_du_monde_en_80_jours.epub","1873_Le_Tour_du_monde_en_quatre-vingts_jours"],
["https://beq.ebooksgratuits.com/vents-epub/Verne-ile.epub","1874_L_Ile_mysterieuse"],]

documentNb = 0
placeNameNb = 0
source = ""

old_file_names = []
new_file_names = []

for doc in booksToDownload:
   # if the input list contains not only the URL but also the filename, use this filename
   if len(doc)==2:
      file = doc[1]
      doc = doc[0]
   documentNb += 1
   if not(doc in alreadyDownloaded):
      url = doc
      fileName = "file.epub"
      source = ""

      res = re.search("https://fr.wikisource.org/wiki/(.+)$",doc)
      if res:
         url = "https://tools.wmflabs.org/wsexport/tool/book.php?lang=fr&format=epub&page=" + res.group(1)
         fileName = res.group(1)+".epub"
         source = "wikisource"
               
      res = re.search("http://www.gutenberg.org/ebooks/([0-9]+)",doc)
      if res:
         url = "https://www.gutenberg.org/ebooks/" + res.group(1) + ".epub.noimages"
         fileName = res.group(1)+".epub"
         source = "gutenberg"
         
      res = re.search("http://www.gutenberg.org/files/([0-9]+)/",doc)
      if res:
         url = "https://www.gutenberg.org/ebooks/" + res.group(1) + ".epub.noimages"
         fileName = res.group(1)+".epub"
         source = "gutenberg"
         
      res = re.search("http://www.gutenberg.org/cache/epub/([0-9]+)/",doc)
      if res:
         url = "https://www.gutenberg.org/ebooks/" + res.group(1) + ".epub.noimages"
         fileName = res.group(1)+".epub"
         source = "gutenberg"
      
      res = re.search("https://gallica.bnf.fr/ark:/12148/([^/]*)",doc)
      if res:
         url = "https://gallica.bnf.fr/ark:/12148/" + res.group(1) + "/f1.epub"
         fileName = res.group(1)+".epub"
         source = "gallica"
      
      res = re.search("https?://beq.ebooksgratuits.com/vents-epub/(.*).epub",doc)
      if res:
         url = "https://beq.ebooksgratuits.com/vents-epub/" + res.group(1) + ".epub"
         fileName = res.group(1)+".epub"
         source = "beq"

      res = re.search("https?://beq.ebooksgratuits.com/auteurs/[^/]*/(.*).epub",doc)
      if res:
         url = doc
         fileName = res.group(1)+".epub"
         source = "beq"
         
      res = re.search("https://www.daniel-lesueur.com",url)
      if res:
         url = url
         fileName = file+".epub"
         source = "lesueur"

      if file != "":
         # if the input list contains not only the URL but also the filename, use this filename
         fileName = file + ".epub"
      if source == "gutenberg" or source == "gallica" or source == "beq" or source == "lesueur":
         print("Downloading "+url)
         response = requests.get(url)
         open(os.path.join(os.path.join(folder,"corpus"),fileName), 'wb').write(response.content)
         time.sleep(5)
      else:
         try:
            print("Downloading "+url)
            driver.get(url)
         except:
            time.sleep(10)
            old_file_names.append(max([os.path.join(folder,"corpus") + "/" + f for f in os.listdir(os.path.join(folder,"corpus"))],key=os.path.getctime))
            new_file_names.append(os.path.join(os.path.join(folder,"corpus"), fileName))        

   else:
      print("File "+str(doc)+" already downloaded")
      
for (old, new) in zip(old_file_names, new_file_names):
    os.rename(old,new)
