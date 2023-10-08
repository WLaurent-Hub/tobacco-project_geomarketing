import arcpy

class DataConvert:
    
    """
    Cette classe permet de faire une sélection spatiale par intersection puis de convertir les entités
    intersectées dans un fichier excel :
    
    Utilisation :
    1. Initialisez la classe avec les paramètres nécessaires.
    2. Appelez la méthode `shape_to_excel()` convertir les données en excel.
    
    Exemple d'utilisation :
    
    from module.dataconvert import DataConvert
    
    dc = DataConvert(
        input_layer = "la couche d'entrée à intersecter", 
        output_layer = "la couche de sortie pour l'intersection", 
        excel_output = "le chemin de sortie du fichier excel
    )
    
    dc.shape_to_excel()
    
    Remarques :
    
    - Les formats excel sont distribués sous type xls.
    - Des valeurs nulles peuvent être recensé 
    """
    
    def __init__(self, input_layer, output_layer, excel_output):
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.excel_output = excel_output
        self.debit_in_desserte = None
    
    def intersection_two_layers(self) -> str:
        
        """
        Effectue l'intersection entre les couches d'entrée et de sortie 
        et stocke le résultat dans self.debit_in_desserte.
        
        Return: 
            str: La couche résultante de l'intersection.
        """
        
        try:
            self.debit_in_desserte = arcpy.SelectLayerByLocation_management(
                in_layer=self.input_layer,
                overlap_type='INTERSECT',
                select_features=self.output_layer,
                selection_type='NEW_SELECTION')
            return self.debit_in_desserte
        except arcpy.ExecuteError:
            print("Erreur lors de l'intersection des couches.")
            return None
    
    def shape_to_excel(self) -> str:
        
        """
        Convertit la couche résultante en un fichier Excel, si elle existe.
        
        Returns:
            str: Un message indiquant si le géocodage a réussi ou s'il a échoué.
        """
        
        self.intersection_two_layers()
        
        if self.debit_in_desserte:
            try:
                arcpy.conversion.TableToExcel(self.debit_in_desserte, self.excel_output)
                print(f"Conversion en Excel réussie : {self.excel_output}")
            except arcpy.ExecuteError as e:
                print(f"Erreur lors de la conversion en Excel : {e}")
        else:
            print("Aucune sélection à convertir en Excel.")
            