import sqlite3
import pandas as pd
from flask import jsonify
import datetime
import openpyxl

class db_manager():
    def __init__(self,db_path):
        self.db_path = (db_path)
        
    def input_data(self, data):
        valid_data = self.validate_data(data)
        
        
        
        local_type = valid_data[0]
        side = valid_data[1]
        location = valid_data[2]
        region = valid_data[3]
        code = valid_data[4]
        date_time = valid_data[5]
        operator = valid_data[6]
        active = 1
        
        connection = sqlite3.connect(self.db_path)
        connection.execute("INSERT INTO HISTORY ('LOCAL_TYPE', 'SIDE', 'LOCATION', 'REGION', 'CODE', 'DATE_TIME', 'OPERATOR','ACTIVE') \
                        VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}',{7})"
                        .format(local_type,side,location,region,code,date_time,operator,active)) 
        connection.commit()
        connection.close()
        
    def validate_data(self, data):
        new_data = []
        try:
            local_type = str(data[0])
            new_data.append(local_type)
            side = str(data[1])
            new_data.append(side)
            location = str(data[2])
            new_data.append(location)
            region = str(data[3])
            new_data.append(region)
            code = str(data[4])
            new_data.append(code)
            date_time = str(data[5])
            new_data.append(date_time)
            operator = str(data[6])
            new_data.append(operator)
            
            return new_data
        except:
            print('Invalid Data')
        
    def delete_data(self, id, date, hmc):
        
        connection = sqlite3.connect(self.db_path)
        
        edit =  '''
                UPDATE HISTORY
                SET ACTIVE = 0
                WHERE ID = ?
                '''
    
        connection.execute(edit,(id,))
        connection.commit()
        connection.execute("INSERT INTO DELETED ('DATE_TIME_DELETED','DELETED_BY','HISTORY_ID') \
                        VALUES ('{0}','{1}',{2})"
                        .format(date,hmc,id)) 

        connection.commit()
        connection.close()
    
    def add_operator(self, hmc, date, name, pwd):
        
        connection = sqlite3.connect(self.db_path)
        connection.execute("INSERT INTO OPERATOR_LIST ('HMC','UPDATED_AT','NAME','PASSWORD') \
                        VALUES ('{0}','{1}','{2}','{3}')"
                        .format(hmc,date,name,pwd)) 
        
        connection.commit()
        connection.close()
        
    def delete_operator(self, hmc):
        
        connection = sqlite3.connect(self.db_path)
        delete = '''
                DELETE FROM OPERATOR_LIST
                WHERE HMC = ?
                '''
        
        connection.execute(delete,(hmc,))
        connection.commit()
        connection.close()
        
    def rst_pwd_operator(self, hmc, date, password):
        
        connection = sqlite3.connect(self.db_path)
        edit =  '''
                UPDATE OPERATOR_LIST
                SET UPDATED_AT = ?,
                PASSWORD = ?
                WHERE HMC = ?
                '''
                
        connection.execute(edit,(date,password,hmc))
        connection.commit()
        connection.close()
        
    def edit_pwd_operator(self, hmc, date, password):
        
        connection = sqlite3.connect(self.db_path)
        edit =  '''
                UPDATE OPERATOR_LIST
                SET UPDATED_AT = ?,
                PASSWORD = ?
                WHERE HMC = ?
                '''
                
        connection.execute(edit,(date,password,hmc))
        connection.commit()
        connection.close()
        
    def edit_operator(self, hmc, name, date, old_hmc):
        
        connection = sqlite3.connect(self.db_path)
        edit =  '''
                UPDATE OPERATOR_LIST
                SET HMC = ?,
                NAME = ?,
                UPDATED_AT = ?
                WHERE HMC = ?
                '''
                
        connection.execute(edit,(hmc,name,date,old_hmc))
        connection.commit()
        connection.close()
        
    def export_excel(self,path):
        connection = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM HISTORY WHERE ACTIVE = 1", connection)
        df.to_excel(path, index=False)
        connection.close()
        
    def get_hmc_list(self): 
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        data = [data[0] for data in cursor.execute("SELECT HMC FROM OPERATOR_LIST")]
        connection.close()
        return data
    
    def get_history(self, d_type, side, location, region, date):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        select_query = "SELECT * FROM HISTORY WHERE ACTIVE = 1"
        
        parameter_list = []
        
        if d_type != "all":
            select_query = select_query + " AND LOCAL_TYPE = ?"
            parameter_list.append(d_type)
        if side != "all":
            select_query = select_query + " AND SIDE = ?"
            parameter_list.append(side)
        if location != "all":
            select_query = select_query + " AND LOCATION = ?"
            parameter_list.append(location)
        if region != "all":
            select_query = select_query + " AND REGION = ?"
            parameter_list.append(region)
            
        if date != "all":
            select_query = select_query + " AND date(DATE_TIME) = date(?)"
            parameter_list.append(date)
        else:
            select_query = select_query + " AND date(DATE_TIME )  >= date('now', '-10 day')"
            
        cursor.execute(select_query, parameter_list)
            
        data = cursor.fetchall()
        connection.close()
        data.reverse()
        return data
    
    def get_graph_data(self):

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        df = pd.read_sql_query("SELECT * FROM HISTORY WHERE ACTIVE = 1 AND date(DATE_TIME )  >= date('now', '-15 day')",connection)
            
        connection.close()

        return df
    
    def query_user_by_hmc(self, hmc):
        # Consulta o banco de dados pelo nome de usuário
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id,HMC,PASSWORD FROM OPERATOR_LIST WHERE HMC=?", (hmc,))
        user_record = cursor.fetchone()
        cursor.close()
        connection.close()
        return user_record

    def query_user_by_id(self, user_id):
        # Consulta o banco de dados pelo ID do usuário
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id,HMC,PASSWORD FROM OPERATOR_LIST WHERE id=?", (user_id,))
        user_record = cursor.fetchone()
        cursor.close()
        connection.close()
        return user_record
    
    def get_all_data_from_user(self, hmc):
        # Consulta o banco de dados pelo nome de usuário
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id,HMC,UPDATED_AT,NAME FROM OPERATOR_LIST WHERE HMC=?", (hmc,))
        user_record = cursor.fetchone()
        cursor.close()
        connection.close()
        return user_record
    
    def get_dates(self):
        date_list = []
        today = datetime.date.today()
        # Usar um loop for para gerar as datas anteriores
        for i in range(10):
            # Subtrair i dias da data de hoje
            date = today - datetime.timedelta(days=i)
            # Converter a data para o formato dd/mm/yyyy
            format_date = date.strftime("%Y-%m-%d")
            # Adicionar a data formatada à lista
            date_list.append(format_date)
        # Retornar a lista
        return date_list
    
    def calculate_sums(self, local, time):
        connection = sqlite3.connect(self.db_path)

        # Update the SQL queries to filter by LOCAL_TYPE = local_recebido
        query_df = f"SELECT * FROM HISTORY WHERE ACTIVE = 1 AND LOCAL_TYPE = '{local}' AND date(DATE_TIME) >= date('now', '-{time}')"
        query_df2 = f"SELECT * FROM LOCATIONS_LIST WHERE LOCAL_TYPE = '{local}'"

        df = pd.read_sql_query(query_df, connection)
        df2 = pd.read_sql_query(query_df2, connection)

        connection.close()

        # If df is an empty DataFrame, create an empty DataFrame with columns from df2 and add 'ACTIVE' column filled with zeros.
        if df.empty:
            merged_df = df2.copy()
            merged_df['ACTIVE'] = 0.0
        else:
            # Agrupar os dados por 'REGION', 'SIDE', 'LOCATION' e 'LOCAL_TYPE' e calcular a soma de 'ACTIVE'
            sums_df = df.groupby(['LOCAL_TYPE', 'SIDE', 'LOCATION', 'REGION'])['ACTIVE'].sum().reset_index()

            # Realizar o merge dos dataframes combinando as colunas-chave e adicionando a coluna 'ACTIVE'
            merged_df = df2.merge(sums_df[['LOCAL_TYPE', 'SIDE', 'LOCATION', 'REGION', 'ACTIVE']], on=['LOCAL_TYPE', 'SIDE', 'LOCATION', 'REGION'], how='left')

            # Preencher os valores ausentes na coluna 'ACTIVE' com 0
            merged_df['ACTIVE'] = merged_df['ACTIVE'].fillna(0)

        # Calcular o valor máximo de 'ACTIVE'
        max_active = merged_df['ACTIVE'].max()

        return merged_df, max_active
    
    def insert_location(self):
        
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        # Abrir o arquivo XLSX
        workbook = openpyxl.load_workbook('locations.xlsx')
        sheet = workbook.active
        
        for row in sheet.iter_rows(min_row=1, values_only=True):
            local_type, side, location, region = row
            query = "INSERT INTO LOCATIONS_LIST (LOCAL_TYPE, SIDE, LOCATION, REGION) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (local_type, side, location, region))

        # Confirmar as alterações e fechar a conexão
        connection.commit()
        connection.close()

