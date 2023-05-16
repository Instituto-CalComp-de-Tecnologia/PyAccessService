from database.dto import SecullumDB

class AccessService:
    def __init__(self) -> None:
        self.db = SecullumDB()
    
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
                    'orientarion': row[5]
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
                    'orientarion': row[5]
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
                'classification': row[3]
            })
            
            if(row[3] not in data_return):
                data_return[row[3]] = 1
            else:
                data_return[row[3]] += 1
        
        return data_return