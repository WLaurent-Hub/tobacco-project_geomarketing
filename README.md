# automatisation-tabac-arcpy

## Presentation

This simple script automates the procedure for a **geomarketing study on the location of tobacconists** according to the legislative framework.

It uses the `arcpy library` to perform these processes.

Four main aspects of the methodology are automatic:
  - Address geocoding 
  - Service area calculation
  - Distance calculation 
  - Gathering of all .xls data in a single Excel table

Process source code is available in the module folder

<pre>
📦tobacco-project_geomarketing
 ┣ 📂module
 ┃ ┣ 📜dataconvert.py
 ┃ ┣ 📜geocoder.py
 ┃ ┣ 📜geodatabase.py
 ┃ ┣ 📜geoprocessing.py
 ┃ ┗ 📜__init__.py
</pre>

## Data

The data are located in the directory data :

<pre>
📦tobacco-project_geomarketing
 ┣ 📂data
 ┃ ┣ 📂adresse
 ┃ ┃ ┣ 📜implantation.xls
 ┃ ┃ ┗ 📜tabac.xls
 ┃ ┗ 📂communes
 ┃ ┃ ┣ 📜communes.cpg
 ┃ ┃ ┣ 📜communes.dbf
 ┃ ┃ ┣ 📜communes.prj
 ┃ ┃ ┣ 📜communes.shp
 ┃ ┃ ┗ 📜communes.shx
</pre>

- **implantation.xls** : address of a possible tobacco plant
- **tabac.xls** : nearby tobacco addresses
- **communes.shp** : Island of France commune

## Settings

### Runtime

The project is based on the python version : **v3.9.10**

### Dependencies 

The project is based on the packages:
- Arcpy **v3.0.2**
- pandas **v1.5.2**

Available in `requirements.txt`

## Run

For the script to work properly, two xls files are required: "implantation.xls" and "tabac.xls" :
  - The **implantation.xls** file represents the tobacco location.
  - The **tabac.xls** file represents existing tobacconists in the département wher
  
1. enter your addresses in the "address" fields (in both excel files) as required.

2. find the municipal contours in shapefile format and insert them in the "communes" directory
(default : Island of France commune in `/data/comunes`)

3. configure your username and password in **config.py**.

