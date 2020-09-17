# This script does not require anything special, but it runs fairly slow. To increase speed you can change id and change rate of id
# and run this script multiple times
# ex: id_min += id_min + 2 and in the first one id_min = 1023342 in the second one id_min = 1023343

"""Important note, if you use windows you may not have permission to download and store the files with python, I recommend using
linux but if you cannot please check internet for permission solutions"""

import requests

id_min = 1023342
id_max = 1063421
url = 'http://transcript.unec.edu.az/transkript/rs?action=studentsReport&studID='

for a in range(id_max - id_min):
    # This part gets the urls for every Student ID
    response = requests.get(url + str(id_min))

    #This part creates a new file and writes content to that file
    open('your path location'+str(id_min), 'wb').write(response.content)
    # This part is for knowing the progress is going
    print(response, id_min)
    if id_min == id_max:
        break
    id_min += 1

"""Important note 2, after all the files are downloaded be sure to open the file location and delete non-pdf files"""
