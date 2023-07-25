from database.departamento_dto import DepartamentoDTO
import copy

class DepartamentoService:
    def __init__(self, config) -> None:
        self.departamentoDTO = DepartamentoDTO(config)
    
    def get_all(self):
        departaments = self.departamentoDTO.get_all()
        data_return = []
        dep = {}
        
        for department in departaments:
            dep["id"] = department.id
            dep['descricao'] = str(department.descricao)
            data_return.append(copy.copy(dep))
        
        return data_return