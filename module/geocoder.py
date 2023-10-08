import os
import arcpy
from config import ROOT_DIR

class Geocoder : 
    
    """
    Cette classe permet de géocoder des adresses à partir des fichiers excels tabac.xls et implantation.xls:
    
    📂data
    ┃ ┣ 📂adresse
    ┃ ┃ ┣ 📜tabac.xls
    ┃ ┃ ┗ 📜implantation.xls
    
    Utilisation :
    1. Ouvrir les deux fichiers excels : tabac.xls et implantation.xls
    2. Ajouter l'adresse dans le champs "adresse" avec son ID dans "OBJECTID
    3. Initialisez la classe avec les paramètres nécessaires.
    4. Appelez la méthode `geocoding_adress()` pour géocoder les adresses.
    
    Exemple d'utilisation :
    
    from module.geocoder import Geocoder
    
    gc = Geocoder(
        tabac_excel_path = "le chemin vers le fichier tabac.xls" (ex: src/data/tabac.xls/Feuil1$), 
        standard_geocod = "le service de géocodage", 
        tabac_gdb_path = "le chemin vers la geodatabase (ex : src/geodatabase.gdb/tabac)
    )
    
    gc.geocoding_adress()
    
    Remarques :
    
    - Les adresses générées seront renvoyées sous forme de données géospatiales points.
    - Le système de coordonnées est en RGF 1993 Lambert-93.
    """
    
    field = "\'Address or Place\' adresse"
    
    def __init__(self, path_database : str, standard_geocod : str, geocoding_output : str):
        self.path_database = os.path.join(ROOT_DIR, path_database)
        self.standard_geocod = standard_geocod
        self.geocoding_output = geocoding_output
        
    def geocoding_adress(self) -> str:
        
        """
        Effectue le géocodage des adresses.
        
        Returns:
            str: Un message indiquant si le géocodage a réussi ou a échoué.
        """
        
        try:
            arcpy.geocoding.GeocodeAddresses(self.path_database, self.standard_geocod, Geocoder.field, self.geocoding_output)
            return "Géocodage réussi"
        except Exception as e:
            return f"Échec du géocodage : {str(e)}"
    