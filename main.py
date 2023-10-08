import os
from config import ROOT_DIR, USER, PASSWORD
from module.geodatabase import Geodatabase
from module.geocoder import Geocoder
from module.geoprocessing import Geoprocessing
from module.dataconvert import DataConvert
from utils.utils import create_folder, to_shapefile, conversion_to_excel, merge_all_xls
import arcpy

def main():
    
    """
    Fonction principale pour l'exécution du flux de travail de l'étude géomarketing sur l'implantation d'un tabac.
    
    Returns:
        None
        
    Remarques:
        - Cette fonction exécute un flux de travail qui comprend la création d'une géodatabase,
          le géocodage d'adresses, la conversion des résultats en formats divers, la génération de zones de service
          et d'itinéraires, ainsi que la fusion de fichiers Excel.
          
        - Elle configure et utilise plusieurs classes et méthodes pour accomplir ces tâches :
          Geodatabase, Geocoder, Geoprocessing, DataConvert, etc.
          
        - Cette fonction coordonne toutes les étapes du processus et peut être utilisée comme point d'entrée pour
          exécuter l'ensemble du flux de travail.
          
        - Les détails spécifiques de configuration (chemins de fichiers, services ArcGIS, géotraitement, etc.)
          sont définis dans la fonction et config.py
    """
    
    # Configuration du service de géocodage
    standard_geocod : str = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/ArcGIS World Geocoding Service"

    # Création d'une instance et d'une geodatabase
    geodatabase : object = Geodatabase(geodatabase_path = ROOT_DIR, geodatabase_name = "geodatabase")
    geodatabase.create_geodatabase()
    
    # Configuration du géocodeur
    geocoding_tabac_name : str = "tabac"
    geocoding_implantation_name : str = "implantation"
    tabac_excel_path = os.path.join("data", "adresse", "tabac.xls", "Feuil1$")
    implantation_excel_path = os.path.join("data", "adresse", "implantation.xls", "Feuil1$")
    tabac_gdb_path  = os.path.join(ROOT_DIR, geodatabase.geodatabase_name + ".gdb", geocoding_tabac_name)
    implantation_gdb_path = os.path.join(ROOT_DIR, geodatabase.geodatabase_name + ".gdb", geocoding_implantation_name)

    # Création d'instances Géocodage et géocodage des objets
    geocoder_tabac : object = Geocoder(tabac_excel_path, standard_geocod, tabac_gdb_path)
    geocoder_tabac.geocoding_adress()

    geocoder_implantation : object = Geocoder(implantation_excel_path, standard_geocod, implantation_gdb_path)
    geocoder_implantation.geocoding_adress()
    
    # Création des dossiers pour stocker les résultats du géocodage
    geocoding_output_folder = os.path.join(ROOT_DIR, "output")
    tabac_output_folder = os.path.join(ROOT_DIR, geocoding_output_folder, geocoding_tabac_name)
    implantation_output_folder = os.path.join(ROOT_DIR, geocoding_output_folder, geocoding_implantation_name)

    create_folder(geocoding_output_folder)
    create_folder(tabac_output_folder)
    create_folder(implantation_output_folder)
    
    # Conversion des résultats au format shapefile
    to_shapefile(tabac_gdb_path, tabac_output_folder)
    to_shapefile(implantation_gdb_path, implantation_output_folder)
    
    # Configuration des services ArcGis
    sa_service = f"https://logistics.arcgis.com/arcgis/services;World/ServiceAreas;{USER};{PASSWORD}"
    cf_service = f"https://logistics.arcgis.com/arcgis/services;World/ClosestFacility;{USER};{PASSWORD}"
    
    # Configuration des répertoires pour le geoprocessing
    service_area_name : str = "desserte_et_distance"
    dessert_area_name : str = "desserte"
    routes_area_name : str = "distances"
    
    geodatabase_implantation_path = os.path.join(
        geodatabase.geodatabase_path, 
        geodatabase.geodatabase_name + ".gdb", 
        geocoding_implantation_name
    )
    
    geodatabase_tabac_path = os.path.join(
        geodatabase.geodatabase_path, 
        geodatabase.geodatabase_name + ".gdb", 
        geocoding_tabac_name
    )
    
    geoprocessing_output_folder = os.path.join(ROOT_DIR, geocoding_output_folder, service_area_name)
    geoprocessing_desserte_folder = os.path.join(geoprocessing_output_folder, dessert_area_name)
    geoprocessing_routes_folder = os.path.join(geoprocessing_output_folder, routes_area_name)

    create_folder(geoprocessing_output_folder)

    # Création dune instance Geoprocessing
    geoprocessing : object = Geoprocessing (
        username = USER, 
        password = PASSWORD, 
        sa_service = sa_service, 
        cf_service = cf_service,
        facilities = geodatabase_implantation_path,
        incidents = geodatabase_tabac_path,
        output_service_areas = geoprocessing_desserte_folder,
        output_routes = geoprocessing_routes_folder,
    )
    
    # Connexion à ArcGis et géotraitement de la zone de desserte
    geoprocessing.login_arcgis()
    geoprocessing.generate_service_area()
    
    # Configuration des chemins excels et communes.shp
    commune_path = os.path.join(ROOT_DIR, "data", "communes", "communes.shp")
    excel_output_path = os.path.join(geocoding_output_folder, "excel_data")
    create_folder(excel_output_path)
    
    # Création de deux instances DataConvert
    convert_tabac_in_dessert : object = DataConvert(
        input_layer = geodatabase_tabac_path,
        output_layer = geoprocessing_desserte_folder,
        excel_output = os.path.join(excel_output_path, "tabac_in_dessert.xls")
    )
    
    convert_commune_in_dessert : object = DataConvert(
        input_layer = commune_path,
        output_layer = geoprocessing_desserte_folder,
        excel_output = os.path.join(excel_output_path , "commune_in_dessert.xls")
    )
    
    # Sélection par intersection et conversion des fichiers de formes en excel
    convert_tabac_in_dessert.shape_to_excel()
    convert_commune_in_dessert.shape_to_excel()
    conversion_to_excel(f"{geoprocessing_routes_folder}.shp", os.path.join(excel_output_path, "distances.xls"))
    
    # Fusionne tous les fichiers excel
    data_excel_merge = os.path.join(ROOT_DIR, "data.xlsx")
    merge_all_xls(ROOT_DIR, data_excel_merge)

if __name__ == "__main__":
    main()
    