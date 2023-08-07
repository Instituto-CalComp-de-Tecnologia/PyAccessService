from database.access_dto import AccessDTO
import copy
import datetime

HOUR_ENT = datetime.datetime(2009, 12, 2, 7, 45, 0)

class AccessService:
    def __init__(self, config) -> None:
        self.db = AccessDTO(config)
    
    def find_total_acess_today_detail(self, local: str):
        access_rows = self.db.get_access_today_detail(local=local)
        data_return = {}
        
        for row in access_rows:            
            date = row[1]
            date_str = date.strftime("%d/%m/%Y")
            
            if(row[8] not in data_return):
                data_return[row[8]] = {
                    'access': [],
                    'total_e': 0,
                    'total_s': 0
                }
                
                data_return[row[8]]['access'].append({
                    'date': date_str,
                    'hour': row[2],
                    'name': row[4],
                    'register': row[3],
                    'equipament': row[6],
                    'orientarion': row[5],
                    'department': row[9],
                    'line': row.desc_line
                })
                
                if(row[5] == 'E'):
                    data_return[row[8]]['total_e'] += 1
                if(row[5] == 'S'):
                    data_return[row[8]]['total_s'] += 1
            else:
                data_return[row[8]]['access'].append({
                    'date': date_str,
                    'hour': row[2],
                    'name': row[4],
                    'register': row[3],
                    'equipament': row[6],
                    'orientarion': row[5],
                    'department': row[9],
                    'line': row.desc_line
                })
                if(row[5] == 'E'):
                    data_return[row[8]]['total_e'] += 1
                if(row[5] == 'S'):
                    data_return[row[8]]['total_s'] += 1
        return data_return
    
    def get_total_access_by_local_today(self):
        access_rows = self.db.get_total_access_by_local_today()
        return access_rows
    
    def get_present_people_by_local(self, local):
        data_return = {
            'access': []
        }
        access_rows = self.db.get_present_people_by_local(local=local)
        
        for row in access_rows:
            data_return['access'].append({
                'register': row[1],
                'name': row[2],
                'classification': row[3],
                'department': row[5],
                'line': row.desc_line
            })
            
            if(row[3] not in data_return):
                data_return[row[3]] = 1
            else:
                data_return[row[3]] += 1
        
        return data_return
    
    def get_absents(self, id_departamento, id_line, type_period, start_date, final_date):
        
        if(type_period == 'D'):
            absents_rows = self.db.get_absents(id_departamento=id_departamento, id_line=id_line)
            
            data_return = []
            data = {}
            for absent in absents_rows:
                if(absent.hor_entrada != None):
                    str_time = absent.hor_entrada.split(':')
                    access_ent = datetime.datetime(2009, 12, 2, int(str_time[0]), int(str_time[1]), int(str_time[2]))
                    if(access_ent > HOUR_ENT):
                        data['id'] = absent.id
                        data['n_folha'] = absent.n_folha
                        data['nome'] = absent.nome
                        data['id_line'] = absent.id_line
                        data['line'] = absent.line
                        data['id_departamento'] = absent.id_departamento
                        data['departamento'] = absent.departamento
                        data['hor_entrada'] = absent.hor_entrada
                        data['desc_turno'] = absent.desc_turno
                        data_return.append(copy.copy(data))
                else:
                    data['id'] = absent.id
                    data['n_folha'] = absent.n_folha
                    data['nome'] = absent.nome
                    data['id_line'] = absent.id_line
                    data['line'] = absent.line
                    data['id_departamento'] = absent.id_departamento
                    data['departamento'] = absent.departamento
                    data['hor_entrada'] = absent.hor_entrada
                    data['desc_turno'] = absent.desc_turno
                    data_return.append(copy.copy(data))
            return data_return
        
        if(type_period == 'W'):
            absents_rows = self.db.get_absents(id_departamento=id_departamento, id_line=id_line)
            data_return = []
            data = {}
            
            for absent in absents_rows:
                entrances = self.db.get_entrances_by_date(absent.id, 'W', None, None)
                access = []
                for entrance in entrances:
                    if(entrance.hor_access != None):
                        str_time = entrance.hor_access.split(':')
                        access_ent = datetime.datetime(2009, 12, 2, int(str_time[0]), int(str_time[1]), int(str_time[2]))
                        if(access_ent > HOUR_ENT):
                            ent = {
                                'data': entrance.date_compare.strftime('%d/%m/%Y'),
                                'week_day': entrance.week_day,
                                'hor_access': entrance.hor_access
                            }
                            access.append(ent)
                    else:
                        ent = {
                                'data': entrance.date_compare.strftime('%d/%m/%Y'),
                                'week_day': entrance.week_day,
                                'hor_access': None
                            }
                        access.append(ent) 
                data['id'] = absent.id
                data['n_folha'] = absent.n_folha
                data['nome'] = absent.nome
                data['id_line'] = absent.id_line
                data['line'] = absent.line
                data['id_departamento'] = absent.id_departamento
                data['departamento'] = absent.departamento
                data['hor_entrada'] = absent.hor_entrada
                data['desc_turno'] = absent.desc_turno
                data['access'] = access
                data_return.append(copy.copy(data))
            return data_return
        
        if(type_period == 'P'):
            absents_rows = self.db.get_absents(id_departamento=id_departamento, id_line=id_line)
            data_return = []
            data = {}
            
            for absent in absents_rows:
                entrances = self.db.get_entrances_by_date(absent.id, 'P', init_date=start_date, end_date=final_date)
                access = []
                for entrance in entrances:
                    if(entrance.hor_access != None):
                        str_time = entrance.hor_access.split(':')
                        access_ent = datetime.datetime(2009, 12, 2, int(str_time[0]), int(str_time[1]), int(str_time[2]))
                        if(access_ent > HOUR_ENT):
                            ent = {
                                'data': entrance.date_compare.strftime('%d/%m/%Y'),
                                'week_day': entrance.week_day,
                                'hor_access': entrance.hor_access
                            }
                            access.append(ent)
                    else:
                        ent = {
                                'data': entrance.date_compare.strftime('%d/%m/%Y'),
                                'week_day': entrance.week_day,
                                'hor_access': None
                            }
                        access.append(ent) 
                data['id'] = absent.id
                data['n_folha'] = absent.n_folha
                data['nome'] = absent.nome
                data['id_line'] = absent.id_line
                data['line'] = absent.line
                data['id_departamento'] = absent.id_departamento
                data['departamento'] = absent.departamento
                data['hor_entrada'] = absent.hor_entrada
                data['desc_turno'] = absent.desc_turno
                data['access'] = access
                data_return.append(copy.copy(data))
            return data_return