# Instructions: 1) This script does most of the job, I don't have the resources to test if optional part works properly, therefore
# it's better to run this script multiple times by changing id values

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

import io
import re
import sqlite3


# This is the part where we open our database and create ourselves a tool to interact with database
conn = sqlite3.connect('transkript.sqlite')
cur = conn.cursor()

'''Run these 2 lines of code only if you stopped the script halfway through'''
#cur.execute('DROP TABLE IF EXISTS Transkript1')
#cur.execute('CREATE TABLE Transkript1 (id INTEGER, AdSoyadAta TEXT,Fakültə TEXT, Ixtisas TEXT, KreditGPA TEXT)')


# I don't know how this part works, but it was the only working example I found on the internet
resource_manager = PDFResourceManager()
fake_file_handle = io.StringIO()
converter = TextConverter(resource_manager, fake_file_handle)
page_interpreter = PDFPageInterpreter(resource_manager, converter)
id_min = 1035000
id_max = 1040000
print(id_max-id_min)
for i in range(id_max-id_min):
    try:
        # These 4 lines of code opens previously downloaded code and runs extracts the text from pdfs
        with open("your path name"+str(id_min), 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                            caching=True,
                                            check_extractable=True):
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
        # This part is where new value is assigned to id_min and keeps the script running
        id_min = id_min+1
        r = text
        '''stop = re.findall('UNEC Biznes məktəbi (MBA)', r) #optional may not work
        if not stop == None:
            continue'''
        # Next 2 lines finds necessary information and and parses it so that we can work with
        evilest = re.findall('.+Fakültə(.+)_(.+)Tələbə.+Soyad, ad və ata adı:(.+)Təhsil pilləsi.+(Ümumi.+)Fa', r)
        evil = evilest[0]

        # This is where the database comes into the play, we start writing to the database
        cur.execute('INSERT INTO Transkript (id, AdSoyadAta, Ixtisas, Faculty, KreditGPA) VALUES(?, ?, ?, ?, ?)',
            (id_min, evil[2], evil[1], evil[0], evil[3]))
        conn.commit()
        print(id_max-id_min)

# This part is for empty pdfs so the script doesn't crash and runs properly
    except:
        id_min = id_min +1
# This happens at the very end and when these 2 lines run the file handles close and our database becomes usable
converter.close()
fake_file_handle.close()
