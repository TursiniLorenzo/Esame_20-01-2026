from dataclasses import dataclass

@dataclass
class Connessione :
    artist_id_A : int
    artist_id_B : int
    num_generi : int

    def __str__ (self) :
        return f'{self.artist_id_A} {self.num_generi} {self.artist_id_B}'

    def __hash__ (self) :
        return hash(self.artist_id_A)