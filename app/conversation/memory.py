from collections import defaultdict

class ConverstaionMemory:

    def __init__(self):
        self.memory=defaultdict(list)


    def add_message(
            self,
            conversation_id:str,
            role:str,
            content:str,
    ):

        self.memory[conversation_id].append(
            {
                "role":role,
                "content":content,
            }
        )   



    def get_history(
            self,
            conversation_id:str,
    ):
        return self.memory.get(conversation_id,[])


    def clear(
            self,
            conversation_id:str,
    ):
        self.memory.pop(conversation_id,None)    