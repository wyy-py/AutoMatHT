Query data from OQMD database: 

(1)
```
OQMD-getdata.py
```
create a .json file containing all the carbon materials in OQMD database, and processing all the necessary revelant information you query into the .json file. 

(2)
```
OQMD-poscar.py
```
convert structure data in .json file to files named [POSCAR_' + str(d['entry_id'])] . 

(3)
```
OQMD-rename.py
```
convert [POSCAR_' + str(d['entry_id'])] files to poscar files, and store each poscar to its corrsponding directory named 'entry_id'. 
