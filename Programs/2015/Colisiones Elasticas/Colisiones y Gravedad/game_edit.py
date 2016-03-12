def edit(file,index,data):
    """ Edita un cierto valor en un archivo
    """
    data = data.split()
    for palabra in data:
        if palabra == " ":
            data.remove(palabra)
    data = "".join(data)        
    fr = open(file,"r")        
    config = fr.read()
    fr.close()
    config = config.split()
    config[index] = data
    config = "\n".join(config)
    fw = open(file,"w")
    fw.write(config)
    fw.close()
    
def get_tuple(file,index):
    """ Obtiene tupla de archivo
    """
    fr = open(file,"r")
    config = fr.read()
    fr.close()
    config = config.split()
    string = config[index]
    lista = string.split(",")
    lista_aux = []
    for elemento in lista:
        string_aux = ""
        for palabra in elemento:
            if palabra != ")" and palabra != "(" and palabra != "," :
                string_aux += palabra         
        try:
            lista_aux.append(int(string_aux))
        except:
            lista_aux.append(float(string_aux))
    return tuple(lista_aux)

def get_bool(file,index):
    """ returna un bool
    dependiendo de la tupla
    """
    x = get_tuple(file,index)[0]
    if x == 0:
        return False
    else:
        return True
    
