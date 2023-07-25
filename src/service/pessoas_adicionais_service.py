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
            data_return.append(copy.copy(data))
        return data_return
    
    def update_pessoa(self, pessoa_id, id_departamento, line):
        try:
            if(id_departamento):
                self.pessoasAdicionaisDTO.update_departamento(pessoa_id=pessoa_id, id_departamento=id_departamento)
            if(line):
                self.pessoasAdicionaisDTO.update_line(pessoa_id=pessoa_id, line=line)
            
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