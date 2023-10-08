import arcpy

class Geoprocessing:
    
    """
    Cette classe se connecte à ArcGis en utilisant les identifiants de l'utilisateur (voir config.py).
    Elle permet de créer une zone de desserte (zone la plus proche) avec une distance à pied de 1,5 kilomètres.
    
    Utilisation :
    
    1. Initialisez la classe avec les paramètres nécessaires.
    2. Appelez la méthode `login_arcgis()` pour vous connecter à ArcGis.
    3. Appelez la méthode `generate_service_area()` pour créer la zone de desserte.
    
    Exemple d'utilisation :
    
    from geoprocessing import Geoprocessing
    
    gp = Geoprocessing(username="votre_utilisateur", password="votre_mot_de_passe")
    gp.login_arcgis()
    gp.generate_service_area()
    
    Remarques :
    
    - Assurez-vous d'avoir configuré les identifiants de l'utilisateur dans config.py.
    - La zone de desserte générée sera renvoyée sous forme de données géospatiales polygonales et linéaires.
    - Le système de coordonnées est en RGF 1993 Lambert-93.
    """
    
    PORTAL_URL = "https://www.arcgis.com"
    WALKING_DISTANCE = "1,5"
    DISTANCE_UNIT = "Kilometers"
    
    def __init__(
        self, 
        username : str, 
        password : any, 
        sa_service : str, 
        cf_service : str, 
        facilities : str, 
        incidents : str, 
        output_service_areas : str, 
        output_routes : str):
        
        self.username = username
        self.password = password
        self.sa_service = sa_service
        self.cf_service = cf_service
        self.facilities = facilities
        self.incidents = incidents
        self.output_service_areas = output_service_areas
        self.output_routes = output_routes
        
    def login_arcgis(self) -> None:
        
        """
        Connecte l'utilisateur à ArcGIS Portal, importe des boîtes à outils de services d'analyse spatiale (SA)
        et de services de cartographie (CF).
        
        Returns:
            None
        """
        
        arcpy.SignInToPortal(Geoprocessing.PORTAL_URL, self.username, self.password) 
        arcpy.ImportToolbox(self.sa_service)
        arcpy.ImportToolbox(self.cf_service)
   
    @staticmethod
    def setup_walking_distance() -> str:
        
        """
        Récupère et configure le mode de déplacement à pied pour le calcul de la distance.

        Returns:
            str: Une description du mode de déplacement à pied configuré.
        """
        
        travel_mode_list = arcpy.na.GetTravelModes(Geoprocessing.PORTAL_URL)
        walking_distance = travel_mode_list["Walking Distance"]
        return str(walking_distance)
    
    def generate_service_area(self):
        
        """
        Génère des zones de service et des itinéraires pour les installations 
        spécifiées en utilisant des modes de déplacement à pied.

        Returns:
            None
        """
        
        result_desserte = arcpy.ServiceAreas.GenerateServiceAreas(
            self.facilities, 
            Geoprocessing.WALKING_DISTANCE, 
            Geoprocessing.DISTANCE_UNIT, 
            Travel_Mode=Geoprocessing.setup_walking_distance()
        )
        
        result_closestFacility = arcpy.ClosestFacility.FindClosestFacilities(
            self.incidents, 
            self.facilities, 
            Geoprocessing.DISTANCE_UNIT, 
            Travel_Mode=Geoprocessing.setup_walking_distance()
        )
        
        while result_desserte.status < 4:
            time.sleep(1)
            
        result_severity = result_desserte.maxSeverity
        
        if result_severity == 2:
            arcpy.AddError("Une erreur s'est produite lors de l'exécution")
            arcpy.AddError(result_desserte.getMessages(2), result_closestFacility.getMessages(2))
            sys.exit(2)  
        elif result_severity == 1:
            arcpy.AddWarning("Un avertissement s'est produit lors de l'exécution ")
            arcpy.AddWarning(result_desserte.getMessages(1), result_closestFacility.getMessages(1)) 
        
        try :
            result_desserte.getOutput(0).save(self.output_service_areas)
            result_closestFacility.getOutput(0).save(self.output_routes)
        except RuntimeError as e:
            return e
                
    