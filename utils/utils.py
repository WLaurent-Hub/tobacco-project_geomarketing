import os
import arcpy
import glob 
import pandas as pd

def create_folder(path) -> str:
    
    """
    Fonction utilitaire pour créer un dossier
    
    Returns:
        str: Un message indiquant si la création du dossier a réussi ou a échoué.
    """
    
    try:
        os.mkdir(path)
        return "Création du dossier réussie"
    except Exception as e:
        return f"Création du dossier fail : {e}"

def to_shapefile(geodatabase_path, geocoding_output) -> str:
    
    """
    Fonction utilitaire pour convertir une couche dans 
    une géodatabase en fichier géospatial shapefile
    
    Returns:
        str: Un message indiquant si la conversion a réussi ou a échoué.
    """
    
    try:
        arcpy.FeatureClassToShapefile_conversion(geodatabase_path, geocoding_output)
        return "Conversion en shapefile réussie"
    except Exception as e:
        return f"Conversion en shapefile fail : {str(e)}"

def conversion_to_excel(shape_layer, excel_layer) -> str:
    
    """
    Fonction utilitaire pour convertir une couche géospatiale
    en fichier excel
    
    Returns:
        str: Un message indiquant si la conversion a réussi ou a échoué.
    """
    
    if shape_layer:
        try:
            arcpy.conversion.TableToExcel(shape_layer, excel_layer)
        except arcpy.ExecuteError as e:
            print(f"Erreur lors de la conversion en Excel : {e}")
    else:
        print("Aucune sélection à convertir en Excel.")
        
def merge_all_xls(root, output_excel):
    
    """
    Fonction utilitaire pour fusionner tous les fichiers excel du projet
    en un seul fichier xlsx
    
    Returns:
        str: Un message indiquant si la conversion a réussi ou a échoué.
    """
    
    search_excel = os.path.join(root, "**", "*.xls*")
    excel_file_found = glob.glob(search_excel, recursive=True)
    dataframes = []

    for excel_file in excel_file_found:
        sheet = os.path.basename(excel_file).split(".")[0]
        df1 = pd.read_excel(excel_file)
        df1.fillna(value="N/A", inplace=True)
        dataframes.append((df1, sheet))

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        for df, sheet_name in dataframes:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print("Fusion réussie des fichiers excel")