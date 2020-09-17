#Realizando importaciones 
import yaml
#Agregando variable 
__config = None 
#Funcion de configuracion
def config():
    global __config
    #validacion de la variable __config  para que no este vacio
    if not __config:
        with open('config.yaml', mode='r') as f:
            __config = yaml.safe_load(f)

        return __config
