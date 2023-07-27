from database.lines_dto import LinesDTO
import copy

class LinesService:
    def __init__(self, config) -> None:
        self.linesDTO = LinesDTO(config)
    
    def get_all(self):
        lines = self.linesDTO.get_all()
        data_return = []
        dep = {}
        
        for line in lines:
            dep["id"] = line.id
            dep['desc_line'] = line.desc_line
            data_return.append(copy.copy(dep))
        
        return data_return