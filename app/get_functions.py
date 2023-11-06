import os

def get_path():
    db_name = None # inicializa a variável db_name como None

    curr_path = get_curr_path()
    

    for file in os.listdir(curr_path): # percorre os arquivos do diretório local
        if file.endswith(".db"): # verifica se o arquivo termina com .db
            db_name = file # salva o nome do arquivo na variável db_name
            break # interrompe o loop
    db_path = curr_path + '/' + str(db_name)
    
    return db_path

def get_curr_path():
    curr_path = os.path.dirname (os.path.abspath (__file__))
    curr_path = curr_path.replace('\\', '/')  # Substitui as barras invertidas por barras normais
    curr_path = curr_path.replace('interface', '')
    return curr_path

if __name__ == '__main__':
    get_path()