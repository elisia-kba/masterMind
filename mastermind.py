import random


class Mastermind ():
   
    def __init__(self):
        self.couleurs= ["red","yellow","blue","orange", "green","black", "purple", "pink"] # liste des couleurs possibles
        
    def generate_solution(self):
       return random.sample(self.couleurs, 4) # On génére une combinaison aléatoire de 4 couleurs
           
    def correction(self, solution, proposition) :
        correction = []
        if solution == proposition :
            correction = ["O","O","O","O"]
        else :
            bonnePlace =  sum(1 for i in range(4) if proposition[i] == solution[i]) # nombre de pion bien placé
            bonPion = sum(1 for c in proposition if c in solution)-bonnePlace       # nombre de pion qui sont dans la solution
            for i in range(bonnePlace):
                correction.append("O")
            for i in range (bonPion) :
                correction.append("X")
            
        return correction
    
    

