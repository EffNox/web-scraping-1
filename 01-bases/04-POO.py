class Casa:
    def __init__(self, color):
        self.color = color
        self.consumo_de_luz = 0
        self.consume_de_agua = 0

    def pintar(self, color):
        self.color = color

    def prender_luz(self):
        self.consumo_de_luz += 10

    def abrir_ducha(self):
        self.consume_de_agua += 10

    def tocar_timbre(self):
        print("RINNG")
        self.consumo_de_luz += 2


# mi_casa = Casa("Grey")
# print(mi_casa.color)
# print(mi_casa.consumo_de_luz)
# mi_casa.tocar_timbre()
# print(mi_casa.consumo_de_luz)

class Mansion(Casa):
    def prender_luz(self):
        self.consumo_de_luz += 50

    def abrir_ducha(self):
        self.consumo_de_agua += 50

    def tocar_timbre(self):
        print("DING DONG")
        self.consumo_de_luz += 3


mi_mansion = Mansion("azul")
print(mi_mansion.color)
mi_mansion.tocar_timbre()
mi_mansion.pintar("plateado")
print(mi_mansion.color)
