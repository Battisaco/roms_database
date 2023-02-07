# roms_database

Project in progress, it aims to get info of roms from diverse sites than compile to a database

Currently this project has the code for scrap from:
https://www.romsgames.net/
https://romsfun.com/

All the possible information about the game (name,region,genera,size...) was extracted according to the availability of the site. 

As the scrap process on these sites takes hours, the extracted data has already been saved and can be found inside the /providers folder 

To test by yourself it's needed to install the requirement.txt, however, the process can take hours, besides the code at the moment is experimental, so there is the possibility of failure.

If you want to test, I recommend you to take only a part or just one of the consoles on the site, to do this you need to change the code in the '(.*)_request.py' files, inside the request function you can limit 

It is worth remembering that the code has very few instructions because it is not ready for production, it can't even be considered an alpha state.