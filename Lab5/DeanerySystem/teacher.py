class Teacher:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.time = 0

    def __str__(self):
       return (f'{self.name} {self.surname}')