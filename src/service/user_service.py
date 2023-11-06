from database.user_dto import UserDTO

class UserService:
    def __init__(self, config) -> None:
        self.userDTO = UserDTO(config)
    
    def create(self, userName: str, password: str):
        userData = self.userDTO.create(userName=userName, password=password)
        return userData
    
    def login(self, password: str):
        data = self.userDTO.login(password=password)
        if(data['status']):
            return {
                'status': True,
                'message': f'User successfully logged',
                'data': {
                    'UserRefectory': data['UserRefectory']
                }
            }
        else:
            return {
                'status': False,
                'message': f'User not found!',
                'data': []
            }