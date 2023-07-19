from database.pessoas_adicionais_dto import PessoasAdicionaisDTO

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
            data_return.append(data)
        return data_return