from database.turno_dto import TurnoDTO
import copy

class TurnoService:
    def __init__(self, config) -> None:
        self.turnoDTO = TurnoDTO(config)
    
    def get_all(self):
        turnos = self.turnoDTO.get_all()
        data_return = []
        turn = {}
        
        for turno in turnos:
            turn["id"] = turno.id
            turn['descricao'] = str(turno.descricao)
            data_return.append(copy.copy(turn))
        
        return data_return