from database.access_dto import AccessDTO
import copy
import datetime

HOUR_ENT_T1 = datetime.datetime(2009, 12, 2, 7, 45, 0)
HOUR_ENT_T2 = datetime.datetime(2009, 12, 2, 17, 33, 0)
HOUR_ENT_T3 = datetime.datetime(2009, 12, 2, 0, 0, 0)
HOUR_ENT_TRAINEE = datetime.datetime(2009, 12, 2, 7, 45, 0)

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
                    if(('TURNO-07:45' in absent.desc_turno) and (access_ent > HOUR_ENT_T1)):
                        data['id'] = absent.id
                        data['n_folha'] = absent.n_folha
                        data['nome'] = absent.nome
                        data['id_line'] = absent.id_line
                        data['line'] = absent.line
                        data['id_departamento'] = absent.id_departamento
                        data['departamento'] = absent.departamento
                        data['hor_entrada'] = absent.hor_entrada
                        data['desc_turno'] = absent.desc_turno
                        data['desc_classificacao'] = absent.desc_classificacao
                        data_return.append(copy.copy(data))
                    elif(('TURNO-17:33' in absent.desc_turno) and (access_ent > HOUR_ENT_T2)):
                        data['id'] = absent.id
                        data['n_folha'] = absent.n_folha
                        data['nome'] = absent.nome
                        data['id_line'] = absent.id_line
                        data['line'] = absent.line
                        data['id_departamento'] = absent.id_departamento
                        data['departamento'] = absent.departamento
                        data['hor_entrada'] = absent.hor_entrada
                        data['desc_turno'] = absent.desc_turno
                        data['desc_classificacao'] = absent.desc_classificacao
                        data_return.append(copy.copy(data))
                    elif(('TURNO-00:00' in absent.desc_turno) and (access_ent > HOUR_ENT_T3)):
                        data['id'] = absent.id
                        data['n_folha'] = absent.n_folha
                        data['nome'] = absent.nome
                        data['id_line'] = absent.id_line
                        data['line'] = absent.line
                        data['id_departamento'] = absent.id_departamento
                        data['departamento'] = absent.departamento
                        data['hor_entrada'] = absent.hor_entrada
                        data['desc_turno'] = absent.desc_turno
                        data['desc_classificacao'] = absent.desc_classificacao
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
                    data['desc_classificacao'] = absent.desc_classificacao
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
                        if(('TURNO-07:45' in absent.desc_turno) and (access_ent > HOUR_ENT_T1)):
                            ent = {
                                'data': entrance.date_compare.strftime('%d/%m/%Y'),
                                'week_day': entrance.week_day,
                                'hor_access': entrance.hor_access
                            }
                            access.append(ent)
                        elif(('TURNO-17:33' in absent.desc_turno) and (access_ent > HOUR_ENT_T2)):
                            ent = {
                                'data': entrance.date_compare.strftime('%d/%m/%Y'),
                                'week_day': entrance.week_day,
                                'hor_access': entrance.hor_access
                            }
                            access.append(ent)
                        elif(('TURNO-00:00' in absent.desc_turno) and (access_ent > HOUR_ENT_T3)):
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
                data['desc_classificacao'] = absent.desc_classificacao
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
                        if(('TURNO-07:45' in absent.desc_turno) and (access_ent > HOUR_ENT_T1)):
                            ent = {
                                'data': entrance.date_compare.strftime('%d/%m/%Y'),
                                'week_day': entrance.week_day,
                                'hor_access': entrance.hor_access
                            }
                            access.append(ent)
                        elif(('TURNO-17:33' in absent.desc_turno) and (access_ent > HOUR_ENT_T2)):
                            ent = {
                                'data': entrance.date_compare.strftime('%d/%m/%Y'),
                                'week_day': entrance.week_day,
                                'hor_access': entrance.hor_access
                            }
                            access.append(ent)
                        elif(('TURNO-00:00' in absent.desc_turno) and (access_ent > HOUR_ENT_T3)):
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
                data['desc_classificacao'] = absent.desc_classificacao
                data['access'] = access
                data_return.append(copy.copy(data))
            return data_return
    
    def get_refectory_access_by_date(self, init_date, final_date, shift, service: str):
        data_return = []
        access_rows = self.db.get_refectory_access_by_date(init_date=init_date, final_date=final_date, shift=shift, service=service)
        data = {}
        
        for access in access_rows:
            data['id_pessoa'] = access.id_pessoa
            data['n_folha'] = access.n_folha
            data['name'] = access.nome
            data['classificacao'] = access.classificacao
            data['departamento'] = access.departamento
            data['turno'] = access.turno
            data['desc_line'] = access.desc_line
            data['qtd_acessos'] = access.qtd_acessos
            data['access_detail'] = self.db.get_refectory_access_by_date_detail(init_date=init_date, final_date=final_date, shift=shift, service=service, id_pessoa=access.id_pessoa)
            data_return.append(copy.copy(data))
        return data_return
    
    def get_exits_by_local_date(self, init_date, final_date, local, name: str):
        data_return = []
        access_rows = self.db.get_exits_by_local_date(init_date=init_date, final_date=final_date, local=local, name=name)
        data = {}
        
        for access in access_rows:
            data['id'] = access.id
            data['n_folha'] = access.n_folha
            data['name'] = access.nome
            data['department'] = access.department
            data['shift'] = access.shift
            data['qtd_saida'] = access.qtd_saida
            data['total_time'] = self.db.get_total_exit_time_by_date(init_date=init_date, final_date=final_date, pessoa_id=access.id, local=local)
            data_return.append(copy.copy(data))
        return data_return
    
    def get_access_f1(self, init_date, final_date):
        data_return = []
        access_rows = self.db.get_access_f1(init_date=init_date, final_date=final_date)
        data = {}
        
        for access in access_rows:
            data['id'] = access.id
            data['register'] = access.register
            data['date_access'] = access.date_access
            data['hour'] = access.hour
            data['direction'] = access.direction
            data['equipment'] = access.equipment
            data['type'] = access.type
            data['function'] = access.function
            data_return.append(copy.copy(data))
        return data_return