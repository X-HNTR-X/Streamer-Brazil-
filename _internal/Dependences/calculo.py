import random

# Classe Calculos: utilitários para views, follows, lucros e avaliação de hardware
class Calculos:
    # Calcula um número de visualizações aleatório entre os limites
    def calcular_views(self, min_views, max_views):
        resultado = random.randint(min_views, max_views)
        return resultado

    # Calcula um número de follows/subscribers aleatório entre os limites
    def calcular_follows_subscribers(self, min, max):
        resultado = random.randint(min, max)
        return resultado
    
    def peak_viewers(self, min, max, extra_multi):
        viewers = random.randint(min, max)
        peak_viewers = viewers * extra_multi
        return peak_viewers
    
    def peak_subs(self, base):
        base_ = (base / 4)
        return base_

    def progress(self, conquistas_save, conquistas):
        progresso = (conquistas_save / conquistas)
        return f"{progresso:.0%}"
    
    # Calcula lucro baseado na plataforma (insta / youtube)
    def calcular_lucro(self, base, nome):
        if nome == "insta":
            resultado = round(base / 2500)
            return resultado

        if nome == "youtube":
            resultado = round(base / 1000)
            return resultado

    # Sorteia um evento com a chance informada (1-100)
    def chance_evento(self, chance):
        resultado = random.randint(1, 100)
        if resultado <= chance:
            return True
        else:
            return False
        
    # Avalia um 'nível' de PC com base nas peças informadas
    def calcular_nivel_pc(self, processador, placa_video, armazenamento, armazenamento_type, memory, memory_socket, memory_quantidade, monitor_hz, teclado, mouse, OS):
        extra_type = 1
        dual_channel = False
        extra_type_amz = 0.25

        if memory_socket == 2:
            extra_type = 2
        if memory_quantidade >= 2:
            dual_channel = True
        if armazenamento_type == 2:
            extra_type_amz = 0.5
        elif armazenamento_type == 3:
            extra_type_amz = 0.75
        
        armazenamento_value = armazenamento * extra_type_amz

        memory_value = memory * 2 if dual_channel else memory

        memory_value = memory_value * extra_type
        
        level = (processador + placa_video + memory_value + armazenamento_value + teclado + mouse + OS + monitor_hz)
        return level
