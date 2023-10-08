# automatisation-tabac-arcpy

## Presentation

This simple script automates the procedure for a **geomarketing study on the location of tobacconists** according to the legislative framework.

It uses the `arcpy library` to perform these processes.

Four main aspects of the methodology are automatic:
  - Address geocoding 
  - Service area calculation
  - Distance calculation 
  - Gathering of all .xls data in a single Excel table

## Run

For the script to work properly, two xls files are required: "implantation.xls" and "tabac.xls" :
  - The "implantation.xls" file represents the tobacco location.
  - The "tabac.xls" file represents existing tobacconists in the département wher
  
1. enter your addresses in the "address" fields (in both excel files) as required.

2. find the municipal contours in shapefile format and insert them in the "communes" directory
(an example is available in the "communes" folder)

3. change the parameters of the "desserte_et_distance()" function in main.py to your arcgis IDs.

