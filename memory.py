import lancedb
from character import Character, create_character

class Memory:
    def __init__(self, uri="data/sample-lancedb", character_name: str = "John Doe", character: Character = create_character()):
        self.uri = uri
        self.db = self.connect_db()
        self.character_name = character_name
        self.character = character
        self.create_bot_character(
            character_name=self.character.name,
            character_definition=self.character
        )

    def connect_db(self):
        return lancedb.connect(self.uri)

    def create_table(self, table_name, data):
        self.table = self.db.create_table(table_name, data=data)
    
    def create_bot_character(self, character_name, character_definition):
        return self.create_table(
            table_name=f"{character_name}",
            data=character_definition,
        )
    
    def search_memory(self, query, limit=2):
        return self.table.search(query).limit(limit).to_pandas()
    
    def add_memory(self, memory):
        return self.table.add(memory)
    
    