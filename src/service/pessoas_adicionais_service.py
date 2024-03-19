from database.pessoas_adicionais_dto import PessoasAdicionaisDTO
import copy

class PessoasAdicionaisService:
    def __init__(self, config) -> None:
        self.pessoasAdicionaisDTO = PessoasAdicionaisDTO(config)
    
    def get_all(self):
        persons = self.pessoasAdicionaisDTO.get_all()
        data_return = []
        data = {}
        for person in persons:
            data['id'] = person.id
            data['n_folha'] = person.n_folha
            data['nome'] = person.nome
            data['line'] = person.line
            data['departamento'] = person.departamento
            data['turno'] = person.turno
            data['classificacao'] = person.classificacao
            data_return.append(copy.copy(data))
        return data_return
    
    def update_pessoa(self, pessoa_id, id_departamento, id_line, id_turno):
        try:
            if(id_departamento):
                self.pessoasAdicionaisDTO.update_departamento(pessoa_id=pessoa_id, id_departamento=id_departamento)
            if(id_line):
                self.pessoasAdicionaisDTO.update_line(pessoa_id=pessoa_id, id_line=id_line)
            if(id_turno):
                self.pessoasAdicionaisDTO.update_turno(pessoa_id=pessoa_id, id_turno=id_turno)
            
            return {
                'status': False,
                'message': f'Pessoa updated successfully.',
                'data': []
            }
        except Exception as err:
            return {
                'status': False,
                'message': f'Error on update pessoa: {str(err)}',
                'data': []
            }