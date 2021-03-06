import pygame as pg
import sys

from arkanoid.entities import Bola, Raqueta, Ladrillo
from arkanoid import niveles, FPS

class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_ppal() -> bool:
        return


class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.bola = Bola(self.pantalla.get_width() // 2, 
                         self.pantalla.get_height() // 2, self.pantalla)
        self.raqueta = Raqueta(self.pantalla.get_width()//2, 
                        self.pantalla.get_height() - 30, self.pantalla)

        self.fuente = pg.font.Font("resources/fonts/FredokaOne-Regular.ttf", 15)
        self.fondo = pg.image.load("resources/images/background.jpg")
        self.ladrillos = pg.sprite.Group()
        self.todos = pg.sprite.Group()
        self.reset()


    def reset(self):
        self.ladrillos.empty()
        self.todos.empty()
        self.todos.add(self.bola, self.raqueta)
        self.contador_vidas = 3


    def crea_ladrillos(self, nivel):
        for col, fil in niveles[nivel]:
            l = Ladrillo(5 + 60 * col, 100 + 30 * fil, 50, 20)
            self.ladrillos.add(l)
        
        self.todos.add(self.ladrillos)

    def bucle_ppal(self) -> bool:
        nivel = 0
        self.reset()
        # Inicializaciones 

        while self.contador_vidas > 0 and nivel < len(niveles):
            self.crea_ladrillos(nivel)

            while self.contador_vidas > 0 and len(self.ladrillos) > 0: 
                # Este if equivale a
                # and  len(self.ladrillos) > 0
                # puesto en la línea del while
                
                self.reloj.tick(FPS)

                eventos = pg.event.get()
                for evento in eventos:
                    if evento.type == pg.QUIT:
                        return False
                    if evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                self.pantalla.blit(self.fondo, (0, 0))   

                self.todos.update()

                self.bola.compruebaChoque(self.raqueta)
                if not self.bola.esta_viva:
                    self.contador_vidas -= 1
                    self.bola.reset()

                for ladrillo in self.ladrillos:
                    if ladrillo.comprobarToque(self.bola):
                        self.ladrillos.remove(ladrillo)
                        self.todos.remove(ladrillo)

                self.todos.draw(self.pantalla)

                texto_contador = self.fuente.render('Contador de vidas: ' + str(self.contador_vidas), True, (255, 255, 255))
                texto_niveles = self.fuente.render('Nivel: ' + str(nivel + 1), True, (255, 255, 255))

                self.pantalla.blit(texto_contador, (self.pantalla.get_width() - 160, 10))
                self.pantalla.blit(texto_niveles, (self.pantalla.get_width() - 160, 30))

                pg.display.flip()

            nivel += 1
            self.bola.reset()

        return True

class GameOver(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/FredokaOne-Regular.ttf", 60)

    def bucle_ppal(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return False
                
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_SPACE:
                        return True
                    if evento.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

            self.pantalla.fill((173, 216, 230))
            texto_final = self.fuente.render("GAME OVER", True, (255, 255, 255))
            rectexto = texto_final.get_rect()
            
            self.pantalla.blit(texto_final, ((self.pantalla.get_width() - rectexto.width)//2,
                                            (self.pantalla.get_height() - rectexto.h)//2))

            pg.display.flip()