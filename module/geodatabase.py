import arcpy

class Geodatabase:
    
    """
    Cette classe permet de créer une géodatabase ArcGis.
    
    Utilisation :
    1. Initialisez la classe avec les paramètres nécessaires.
    2. Appelez la méthode `create_geodatabase()` pour créer la géodatabase.
    
    Exemple d'utilisation :
    
    from module.geodatabase import Geodatabase
    
    gd = Geodatabase(
        geodatabase_path = "le chemin vers le dossier de la geodatabase", 
        geodatabase_name = "le nom de la géodatabase", 
    )
    
    gd.create_geodatabase()
    
    Remarques :
    
    - La création de la géodatabase va créer un dossier ".gdb"
    - La géodatabase est visualisable dans le logiciel ArcGis Pro d'Esri.
    """
    
    def __init__(self, geodatabase_path : str, geodatabase_name : str):
        self.geodatabase_path = geodatabase_path
        self.geodatabase_name = geodatabase_name
        
    def create_geodatabase(self) -> str:
        
        """
        Crée une nouvelle géodatabase à l'emplacement spécifié.

        Returns:
            str: Un message indiquant si la création de la géodatabase a réussi ou a échoué.
        """
        
        try :
            arcpy.CreateFileGDB_management(self.geodatabase_path, self.geodatabase_name) 
            return "Création d'une géodatabase réussie"
        except Exception as e :
            return f"Création d'une géodatabase échoué : {str(e)}"
