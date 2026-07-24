from .calculo import Calculos
import builtins, time
from Dependences import save_manager
from Dependences.sounds.sound_manager import SoundManager

sound = SoundManager()
print_original = builtins.print

def printmd(*args, **kwargs):
    kwargs.setdefault('flush', True)
    texto = " ".join(str(arg) for arg in args)
    for letra in texto:
        print_original(letra, end="", flush=True)
        time.sleep(0.01)
    print_original(**kwargs)

builtins.print = printmd

# Instancia da calculadora: fornece funções de cálculo para views, follows e lucros
calculadora = Calculos()

# Classe Player: representa o self e seu estado (atributos e métodos)
class Player:
    def save_achievements(self, categoria, nome):
        if nome in self.conquistas_desbloqueadas:
            return

        conquistas_mestre = save_manager.load_data("Dependences/achievements.json") or {}
        conquista = conquistas_mestre.get("achievements", {}).get(categoria, {}).get(nome)

        if conquista:
            self.conquistas_desbloqueadas.append(nome)

            sound.play_sound("achievements")
            # Corrigido aspas duplas aninhadas na f-string
            print(f"\n{'='*50}\n")
            print(f"Ganhou a conquista: {nome}\n")
            message = conquista.get("message", "")
            print(f"{message}")
            print(f"\n{'='*50}")
            self.save()

    def check_achievements(self):
        if self.yt_status.get("views_yt", 0) >= 5000:
            self.save_achievements("básicos", "Vídeo bom!")

        if self.yt_status.get("ganho_yt", 0) >= 1 or self.insta_status.get("ganho_insta", 0) >= 1:
            self.save_achievements("básicos", "Lucro é lucro!")

        if self.status.get("carteira_assinada"):
            self.save_achievements("básicos", "Um bom começo, CLT!")

        if self.habilidades:
            self.save_achievements("básicos", "Habilidade gênial!")

        if self.status.get("computador"):
            self.save_achievements("básicos", "Computador da xuxa...")

        if self.status.get("money", 0) <= 0:
            self.save_achievements("básicos", "A que ponto chegamos?")

        if self.status.get("divida", 0) > 0:
            self.save_achievements("básicos", "O Serasa não vai gostar...")

        if self.status.get("emprestimo"):
            self.save_achievements("básicos", "Eu juro que é emprestado!")

        if self.tempo.get("dia_semana", "segunda") == "sexta" and self.status.get("folga_do_dia", False) == True:
            self.save_achievements("básicos", "Sextou!")

        if self.status.get("saude", 0) <= 0:
            self.save_achievements("secretos", "Morreu!")

        if self.status.get("fome", 0) >= 80:
            self.save_achievements("secretos", "Tá passando fome?")

        if self.tempo.get("ano") == 2030:
            self.save_achievements("secretos", "Ano de copa!")

        if self.status.get("id_vaga"):
            if self.status.get("id_vaga") == 3 and self.pais_atual == "Brasil":
                self.save_achievements("normais", "Progamador é um trabalho?")

        if len(self.habilidades) >= 3:
            self.save_achievements("normais", "Estudioso ein?")

        if len(self.habilidades) >= 6:
            self.save_achievements("especialista", "Eita bixo habilidoso!")

        if len(self.habilidades) >= len(self.habilidades_para_desbloquear):
            self.save_achievements("pro", "O amante de estudos!")

        if self.yt_status.get("subscribers", 0) >= 1000 or self.insta_status.get("follows", 0) >= 1000:
            self.save_achievements("básicos", "Seguidores fantasma!")

    
    def data_to_async(self, data):
        # Trata caso receba o dicionário 'progress' direto ou a raiz do JSON
        progress = data.get("progress", data)

        if "status" in progress:
            self.status.update(progress["status"])
            self.status["energia"] = max(0, self.status.get("energia", 0))

        if "pc_atual" in progress:
            self.pc_atual.update(progress["pc_atual"])

        if "boletos" in progress:
            self.boletos.update(progress["boletos"])

        if "insta_status" in progress:
            self.insta_status.update(progress["insta_status"])

        if "yt_status" in progress:
            self.yt_status.update(progress["yt_status"])

        if "banco_inter" in progress:
            self.banco_inter.update(progress["banco_inter"])

        if "tempo" in progress:
            self.tempo.update(progress["tempo"])

        # Restaura lista de conquistas salvas
        if "achievements" in data:
            self.conquistas_desbloqueadas = data["achievements"]
        elif "achievements" in progress:
            self.conquistas_desbloqueadas = progress["achievements"]

        self.pais_atual = progress.get("pais_atual", self.pais_atual)
        self.level_celular_atual = progress.get("level_celular_atual", self.level_celular_atual)
        self.habilidades = progress.get("habilidades", self.habilidades)

    # Inicializa um novo self com atributos, status e inventários
    def __init__(self, nome, id):
        self.id = id
        self.nome = nome
        # Status principal do self: dinheiro, energia, saúde, etc.
        self.status = {
            "money_usd": 0,
            "money": 150,
            "money_euro": 0,
            "xp_trabalho": 0,
            "xp": 0,
            "energia": 100,
            "fome": 0, 
            "saude": 100,
            "estresse": 0,
            "ansiedade": 0,
            "depressao": False,
            "computador": False,
            "pontos": 0,
            "carteira_assinada": False,
            "faltas": 0,
            "postou_no_insta": False,
            "postou_no_yt": False,
            "folga": True,
            "folga_do_dia": True,
            "energia_antes_de_dormir": 0,
            "id_vaga": None,
            "divida": 0,
            "pagou_divida": False,
            "emprestimo": False,
            "pegou_emprestado": 0
        }
        self.conquistas_desbloqueadas = []
        # Configuração atual do PC (peças instaladas)
        self.pc_atual = {
            #azt type index: 1 = HDD 2 = SATA 3 = NVMe / mmy socket: 1 = DDR4 2 = DDR5
            "processador": 0,
            "placa de video": 0,
            "armazenamento": 0,
            "azt type": 0,
            "memory": 0,
            "mmy socket": 0,
            "mmy quantidade": 0,
            "monitor hz": 0,
            "mouse level": 0,
            "teclado level": 0,
            "OS level": 0
        }
        # Boletos mensais do self
        self.boletos = {
            "luz": {"valor": 100, "pago": False},
            "agua": {"valor": 80, "pago": False},
            "internet": {"valor": 120, "pago": False},
            "aluguel": {"valor": 500, "pago": False}
        }
        # Catálogo de peças disponíveis na loja
        self.pecas_loja = {
            "processadores": {
                1: {"nome": "i3 11ª geração", "custo": 400, "qualidade": 1},
                2: {"nome": "i5 12ª geração", "custo": 600, "qualidade": 2},
                3: {"nome": "i7 13ª geração", "custo": 1000, "qualidade": 3},
                4: {"nome": "i9 14ª geração", "custo": 1500, "qualidade": 4}
            },
            "placas de video": {
                1: {"nome": "GTX 1650", "custo": 800, "qualidade": 1},
                2: {"nome": "RTX 2060", "custo": 1100, "qualidade": 2},
                3: {"nome": "RX 5600", "custo": 1300, "qualidade": 3},
                4: {"nome": "RTX 3050", "custo": 1500, "qualidade": 4}
            },
            "rams_ddr4": {
                1: {"nome": "1 pente de 8GB", "custo": 450, "total_memory": 8, "quantidade": 1, "socket": "DDR4"},
                2: {"nome": "2 pentes de 8GB", "custo": 900, "total_memory": 16, "quantidade": 2, "socket": "DDR4"},
                3: {"nome": "1 pente de 16GB", "custo": 750, "total_memory": 16, "quantidade": 1, "socket": "DDR4"},
                4: {"nome": "2 pentes de 16GB", "custo": 1500, "total_memory": 32, "quantidade": 2, "socket": "DDR4"}
            },
            "placas mãe": {
                1: {"nome": "B710M", "custo": 500, "socket": "DDR4"},
                2: {"nome": "---", "custo": 700, "socket": "DDR4"}
            },
            "ssd": {
                1: {"nome": "HDD de 256GB", "custo": 150, "armazenamento": 256, "tipo": "HDD"},
                2: {"nome": "HDD de 512GB", "custo": 300, "armazenamento": 512, "tipo": "HDD"},
                3: {"nome": "SSD SATA de 256GB", "custo": 250, "armazenamento": 256, "tipo": "SATA"},
                4: {"nome": "SSD SATA de 512GB", "custo": 400, "armazenamento": 512, "tipo": "SATA"}
            },
            "monitores": {
                1: {"nome": "Monitor LED 30hz 1080p", "custo": 300, "max_fps": 30, "display": "LED"},
                2: {"nome": "Monitor VA 60hz 1080p", "custo": 450, "max_fps": 60, "display": "VA"},
                3: {"nome": "Monitor IPS 60hz 1080p", "custo": 550, "max_fps": 60, "display": "IPS"},
                4: {"nome": "monitor IPS 120hz 1080", "custo": 650, "max_fps": 120, "display": "IPS"}
            },
            "mouse": {
                1: {"nome": "Mouse cabeado sem marca", "custo": 20, "vantagem": 1},
                2: {"nome": "Mouse cabeado classico", "custo": 45, "vantagem": 3},
                3: {"nome": "Mouse sem fio classico", "custo": 95, "vantagem": 5},
                4: {"nome": "Mouse 3-Mode 1000hz", "custo": 130, "vantagem": 7}
            },
            "teclado": {
                1: {"nome": "Teclado de escritorio", "custo": 30, "vantagem": 1},
                2: {"nome": "Teclado Semi-Mecanico", "custo": 45, "vantagem": 3},
                3: {"nome": "Teclado Mecanico Switch Azul", "custo": 100, "vantagem": 6},
                4: {"nome": "Teclado Mecanico Switch Vermelho", "custo": 150, "vantagem": 8}
            },
            "OS": {
                1: {"nome": "Windows 10 Home", "custo": 200,"level": 1},
                2: {"nome": "Windowns 11 Pro", "custo": 500,"level": 2}
            }
        }
        # Estatísticas do Instagram do self
        self.insta_status = {
            "follows": 0,
            "top_video": 0,
            "ganho_insta": 0,
            "views_insta": 0
        }
        # Estatísticas do YouTube do self
        self.yt_status = {
            "subscribers": 0,
            "top_video": 0,
            "ganho_yt": 0,
            "views_yt": 0
        }
        # Habilidades disponíveis para desbloqueio
        self.habilidades_para_desbloquear = {
            1: {"nome": "programacao", "custo": 2, "beneficios": "Libera mais trabalhos"},
            2: {"nome": "RH", "custo": 4, "beneficios": "Libera mais trabalhos, pode ir aos EUA"},
            3: {"nome": "gerencia", "custo": 3, "beneficios": "Libera mais trabalhos"},
            4: {"nome": "frontend", "custo": 2, "beneficios": "Libera mais trabalhos"},
            5: {"nome": "backend", "custo": 2, "beneficios": "Libera mais trabalhos"},
            6: {"nome": "vicio em jogos", "custo": 5, "beneficios": "Libera mais trabalhos, pode ir a Espanha"},
            7: {"nome": "talento", "custo": 6, "beneficios": "Trabalhos melhores"},
            8: {"nome": "sensos rapidos", "custo": 7, "beneficios": "Trabalhos melhores"},
            9: {"nome": "egoista", "custo": 4, "beneficios": "Trabalhos ainda melhores"}
        }

        # Controle do tempo do jogo
        self.tempo = {
            "hora": 6,
            "minutos": 0,
            "dia": 1,
            "mes": 1,
            "ano": 2026
        }

        # Trabalhos disponíveis por país, com requisitos e ganhos
        self.trabalhos = {
            "Brasil": {
                1: {"nome": "Entregador do Ifood", "ganho": 1000, "energia_gasta": 40, "estresse_acumulado": 40, "xp_obrig": 0, "habilidades_obrig": [], "tempo_gasto": 12, "xp_trabalho_ganho": 5, "fome": 30},
                2: {"nome": "Cozinheiro PJ do Giraffas", "ganho": 1500, "energia_gasta": 50, "estresse_acumulado": 30, "xp_obrig": 50, "habilidades_obrig": [], "tempo_gasto": 8, "xp_trabalho_ganho": 10, "fome": 40},
                #trabalhos para a cidade de Sao Paulo
                3: {"nome": "Programador Junior", "ganho": 2000, "energia_gasta": 75, "estresse_acumulado": 70, "xp_obrig": 100, "habilidades_obrig": ["programacao"], "tempo_gasto": 10, "xp_trabalho_ganho": 20, "fome": 50},
            },
            # EUA Jobs
            "USA": {
                1: {"nome": "Gerente de RH", "ganho": 2500, "energia_gasta": 55, "estresse_acumulado": 30, "xp_obrig": 250, "habilidades_obrig": ["RH"], "tempo_gasto": 9, "xp_trabalho_ganho": 40, "fome": 40},
                2: {"nome": "Gerente de Posto", "ganho": 3000, "energia_gasta": 65, "estresse_acumulado": 50, "xp_obrig": 500, "habilidades_obrig": ["Gerencia", "RH"], "tempo_gasto": 10, "xp_trabalho_ganho": 40, "fome": 50},
                #trabalhos para New York
                3: {"nome": "Programador FullStack", "ganho": 3500, "energia_gasta": 80, "estresse_acumulado": 75, "xp_obrig": 750, "habilidades_obrig": ["programacao", "frontend", "backend"], "tempo_gasto": 12, "xp_trabalho_ganho": 50, "fome": 50},
            },
            # Spain Jobs
            "Spain": {
                1: {"nome": "Pro player de CS2", "ganho": 4000, "energia_gasta": 50, "estresse_acumulado": 60, "xp_obrig": 1000, "habilidades_obrig": ["vicio em jogos", "talento", "sensos rapidos"], "tempo_gasto": 6, "xp_trabalho_ganho": 50, "fome": 50},
                2: {"nome": "Programador Backend da Google", "ganho": 4500, "energia_gasta": 50, "estresse_acumulado": 70, "xp_obrig": 1500, "habilidades_obrig": ["programacao", "backend"], "tempo_gasto": 9, "xp_trabalho_ganho": 50, "fome": 50},
                #Trabalhos para Madrid
                3: {"nome": "Pro player de FPS", "ganho": 5500, "energia_gasta": 60, "estresse_acumulado": 65, "xp_obrig": 2500, "habilidades_obrig": ["vicio em jogos", "talento", "sensos rapidos", "egoista"], "tempo_gasto": 7, "xp_trabalho_ganho": 50, "fome": 50}
            }
        }

        # Bicos rápidos disponíveis para gerar dinheiro extra no início do jogo
        self.bicos = {
            1: {"nome": "Seguranca de Shopping", "ganho": 180, "tempo": 8, "fome": 20, "energia": 45, "estresse_acumulado": 20},
            2: {"nome": "Cobrador de Estacionamento", "ganho": 220, "tempo": 6, "fome": 17, "energia": 35, "estresse_acumulado": 15},
            3: {"nome": "Montador de Stands em Evento", "ganho": 250, "tempo": 7, "fome": 19, "energia": 40, "estresse_acumulado": 20},
            4: {"nome": "Ajudante de Carga em Mercado", "ganho": 300, "tempo": 9, "fome": 25, "energia": 50, "estresse_acumulado": 22},
            5: {"nome": "Recepcionista de Salão", "ganho": 340, "tempo": 10, "fome": 26, "energia": 45, "estresse_acumulado": 25},
            6: {"nome": "Assistente de Loja no Fim de Semana", "ganho": 400, "tempo": 11, "fome": 32, "energia": 48, "estresse_acumulado": 28}
        }

        # Informações sobre países e câmbio
        self.paises = {
            "Brasil": {"moeda": "BRL", "cambio": 1},
            "USA": {"moeda": "USD", "cambio": 6},
            "Espanha": {"moeda": "EUR", "cambio": 6}
        }
        self.casas = {
            "Brasil": {
                1: {"nome": "Casa em Osasco", "Aluguel": 500, "agua": 80, "luz": 100, "internet": 120, "entrada": 1500}
            }
        }
        self.pais_atual = "Brasil"

        # Limiares por nível do celular para alcance/engajamento
        self.level_celular = {
            "level1": {"insta": [250, 2500], "yt": [100, 1000], "follows": [125, 1250], "subscribers": [50, 500]},
            "level2": {"insta": [2500, 12500], "yt": [1000, 5000], "follows": [1250, 6250], "subscribers": [500, 2500]},
            "level3": {"insta": [12500, 50000], "yt": [5000, 20000], "follows": [6250, 25000], "subscribers": [2500, 10000]},
            "level4": {"insta": [50000, 250000], "yt": [20000, 100000], "follows": [25000, 125000], "subscribers": [10000, 50000]},
            "level5": {"insta": [250000, 1250000], "yt": [100000, 500000], "follows": [125000, 625000], "subscribers": [50000, 250000]}
        }

        # Estado inicial das habilidades e do celular do jogador
        self.habilidades = []
        self.level_celular_atual = "level1"

        # Estado do banco: conta, investimento e flags
        self.banco_inter = {
            "valor_em_conta": 0,
            "rende": False,
            "investiu": False,
            "investido": 0
        }

    def return_all_data(self):
        all_data = {
            "id": self.id,
            "nome": self.nome,
            "progress": {
                "status": self.status,
                "tempo": self.tempo,
                "pc_atual": self.pc_atual,
                "boletos": self.boletos,
                "insta_status": self.insta_status,
                "yt_status": self.yt_status,
                "banco_inter": self.banco_inter,
                "level_celular_atual": self.level_celular_atual,
                "habilidades": self.habilidades,
                "pais_atual": self.pais_atual
                },
            "achievements": self.conquistas_desbloqueadas
        }
        return all_data

    def save(self):
        data = self.return_all_data()
        save_manager.async_data_background(data, f"Dependences/save{self.id}.json")

    # Aplica desgaste mental: aumenta estresse/ansiedade e marca depressao
    def aplicar_desgaste_mental(self, estresse_ganho, ansiedade_ganha):
        self.status["ansiedade"] = min(100, self.status["ansiedade"] + ansiedade_ganha)
        self.status["estresse"] = min(100, self.status["estresse"] + estresse_ganho)
        if self.status["ansiedade"] >= 100 or self.status["estresse"] >= 100:
            self.status["depressao"] = True

    # Reduz desgaste mental (estresse/ansiedade) e remove depressao quando aplicável
    def tirar_desgaste_mental(self, estresse_aliviado, ansiedade_aliviada):
        self.status["ansiedade"] = max(0, self.status["ansiedade"] - ansiedade_aliviada)
        self.status["estresse"] = max(0, self.status["estresse"] - estresse_aliviado)
        if self.status["ansiedade"] < 100 and self.status["estresse"] < 100:
            self.status["depressao"] = False

    # Estudar por um tempo dado: ganha XP, fica com fome e perde energia
    def estudar(self, tempo):
        self.ganhar_xp(ganhado=tempo * 2)
        self.ganhar_fome(ganho=tempo * 3)
        self.perder_energia(perda=tempo * 3)
        self.tempo["hora"] += tempo
            
    # Descansar pelo resto do dia: recupera energia e avança dia
    def dormir(self):
        print("\nVocê deitou e descansou pelo resto do dia...\n")
        self.tirar_desgaste_mental(estresse_aliviado=40, ansiedade_aliviada=30)
        self.status["energia"] = 100
        self.tempo["hora"] = 23

    # Converter parte do dinheiro para moeda estrangeira, dependendo do país
    def converter(self):
        if self.pais_atual == "USA":
            self.status["money_usd"] = int(self.status["money"] / 6)
            self.status["money"] -= int(self.status["money"] / 6)
        elif self.pais_atual == "Spain":
            self.status["money_euro"] = int(self.status["money"] / 6)
            self.status["money"] -= int(self.status["money"] / 6)

    # Operações de dinheiro simples
    def ganhar_money(self, ganho):
        self.status["money"] += ganho

    def perder_money(self, perda):
        self.status["money"] -= perda

    # Avança o relógio do self
    def passar_hora(self, passado):
        self.tempo["hora"] += passado
    
    # Ajusta o nível de fome do jogador (mantém entre 0 e 100)
    def ganhar_fome(self,ganho):
        self.status["fome"] = min(100, self.status["fome"] + ganho)
        if self.status["fome"] == 100:
            self.status["saude"] -= 20

    # Reduz a fome do jogador (não fica negativa)
    def perder_fome(self, perda):
        self.status["fome"] = max(0, self.status["fome"] - perda)

    # Avança o dia e reseta a hora para o início do dia (6h)
    def virar_dia(self):
        self.tempo["dia"] += 1
        self.tempo["hora"] = 6

    def passar_minuto(self):
        self.tempo["minutos"] += 1
        if self.tempo["minutos"] == 60:
            self.passar_hora(1)
            self.tempo["minutos"] = 0

    # Publicar vídeo em Insta/YouTube: calcula views, follows e lucro
    def postar_video(self, id):
        if id == "insta":

            dados = self.level_celular[self.level_celular_atual]["insta"]
            dados_follows = self.level_celular[self.level_celular_atual]["follows"]

            min_follows = dados_follows[0]
            max_follows = dados_follows[1]

            min_views_insta = dados[0]
            max_views_insta = dados[1]

            self.aplicar_desgaste_mental(estresse_ganho=10, ansiedade_ganha=30)
            self.perder_energia(perda=20)
            self.ganhar_fome(ganho=10)
            self.passar_hora(passado=2)
            
            follows = calculadora.calcular_follows_subscribers(min=min_follows, max=max_follows)
            views_insta = calculadora.calcular_views(min_views=min_views_insta, max_views=max_views_insta)
            if views_insta:
                self.insta_status["views_insta"] = views_insta
            
            if views_insta > self.insta_status["top_video"]:
                self.insta_status["top_video"] = views_insta

            self.insta_status["follows"] += min(views_insta, follows)

            ganho = calculadora.calcular_lucro(base=views_insta, nome="insta")
            if ganho:
                self.insta_status["ganho_insta"] = ganho
        
        elif id == "youtube":
            dados = self.level_celular[self.level_celular_atual]["yt"]
            dados_subs = self.level_celular[self.level_celular_atual]["subscribers"]

            min_subs = dados_subs[0]
            max_subs = dados_subs[1]
            min_views_yt = dados[0]
            max_views_yt = dados[1]    

            self.aplicar_desgaste_mental(estresse_ganho=20, ansiedade_ganha=40)
            self.perder_energia(perda=30)
            self.ganhar_fome(ganho=20)
            self.passar_hora(passado=4)
            
            subs = calculadora.calcular_follows_subscribers(min=min_subs, max=max_subs)
            views_yt = calculadora.calcular_views(min_views=min_views_yt, max_views=max_views_yt)
            if views_yt:
                self.yt_status["views_yt"] = views_yt

            if views_yt > self.yt_status["top_video"]:
                self.yt_status["top_video"] = views_yt

            self.yt_status["subscribers"] += min(views_yt, subs)

            ganho = calculadora.calcular_lucro(base=views_yt, nome="youtube")
            if ganho:
                self.yt_status["ganho_yt"] = ganho
        
    # Operações bancárias: deposito, saque, investimento
    def deposito_banco(self, valor_a_depositar):
        self.banco_inter["valor_em_conta"] += valor_a_depositar
        self.status["money"] -= valor_a_depositar
        self.banco_inter["rende"] = True
    
    def saque_banco(self, valor_a_retirar):
        self.banco_inter["valor_em_conta"] -= valor_a_retirar
        self.status["money"] += valor_a_retirar
        if self.banco_inter["valor_em_conta"] <= 0:
            self.banco_inter["rende"] = False

    def investir_banco(self, investido):
        self.banco_inter["investido"] += investido
        self.status["money"] -= investido
        if self.banco_inter["investido"] > 0:
            self.banco_inter["investiu"] = True

    def retirar_lucro_banco(self, valor_a_retirar):
        self.banco_inter["investido"] -= valor_a_retirar
        self.status["money"] += valor_a_retirar
        if self.banco_inter["investido"] <= 0:
            self.banco_inter["investiu"] = False

    # Avança o mês e reseta o dia para o primeiro dia do mês
    def virar_mes(self):
        self.tempo["mes"] += 1
        self.tempo["dia"] = 1

    # Avança o ano e reseta o mês para o primeiro mês
    def virar_ano(self):
        self.tempo["ano"] += 1
        self.tempo["mes"] = 1

    # Ajusta energia do jogador mantendo o valor entre 0 e 100
    def perder_energia(self, perda):
        self.status["energia"] = max(0, self.status["energia"] - perda)

    # Recupera energia do jogador sem exceder 100
    def ganhar_energia(self, ganho):
        self.status["energia"] = min(100, self.status["energia"] + ganho)

    # Concede XP; ao alcançar 100 XP, converte em ponto e reduz XP acumulado
    def ganhar_xp(self, ganhado):
        self.status["xp"] += ganhado
        if self.status["xp"] >= 100:
            self.status["pontos"] += 1
            self.status["xp"] -= 100
        return self.status["pontos"], self.status["xp"]

    # Valida requisitos para trabalhar em uma vaga
    def pode_trabalhar(self, id_trabalho):
        vaga = self.trabalhos[self.pais_atual][id_trabalho]
        if self.status["xp_trabalho"] < vaga["xp_obrig"]:
            print(f"\n Falta experiência de trabalho! Exigido: {vaga['xp_obrig']}, Você tem: {self.status['xp_trabalho']}.")
            return False
        for hab in vaga["habilidades_obrig"]:
            if hab not in self.habilidades:
                print(f"\n Você não possui a habilidade necessária: '{hab}'!")
                return False
        return True
    
    # Diminui pontos do jogador (não fica negativo)
    def perder_pontos(self, perda):
        self.status["pontos"] = max(0, self.status["pontos"] - perda)

    # Executa um trabalho: consome energia, ganha XP de trabalho e aplica desgaste
    def trabalhar(self, id_trabalho):
        vaga = self.trabalhos[self.pais_atual][id_trabalho]
        self.perder_energia(perda=vaga["energia_gasta"])
        self.status["xp_trabalho"] += vaga["xp_trabalho_ganho"]
        self.aplicar_desgaste_mental(vaga["estresse_acumulado"], 15)
        self.passar_hora(vaga["tempo_gasto"])
        self.ganhar_fome(vaga["fome"])

    # Realiza uma verificação de chance/evento usando a calculadora
    def sortear(self, chance):
        resultado = calculadora.chance_evento(chance=chance)
        return resultado

    def check_ups (self, id):
        if id == "diario":
            # Se a hora passou de 22h, vira o dia
            self.status["energia_antes_de_dormir"] = self.status["energia"] 
            self.virar_dia()         

            # Reativa boletos pagos para o próximo ciclo
            for boleto in self.boletos:
                if self.boletos[boleto]["pago"]:
                    self.boletos[boleto]["pago"] = False

            # Processa ganhos de postagens nas redes sociais
            if self.status["postou_no_yt"] or self.status["postou_no_insta"]:
                
                if self.status["postou_no_yt"]:
                    print(f"Seu Youtube rendeu: {self.yt_status['ganho_yt']} pelo seu video de {self.yt_status['views_yt']} views!\n")
                    self.status["postou_no_yt"] = False
                    self.ganhar_money(ganho=self.yt_status["ganho_yt"])
                    self.yt_status["ganho_yt"] = 0

                if self.status["postou_no_insta"]:
                    print(f"Seu Instagram rendeu: {self.insta_status['ganho_insta']} pelo seu reel de {self.insta_status['views_insta']} views!\n")
                    self.status["postou_no_insta"] = False
                    self.ganhar_money(ganho=self.insta_status["ganho_insta"])   
                    self.insta_status["ganho_insta"] = 0

            # Verifica se o self trabalha com carteira assinada
            if self.status["carteira_assinada"]:
                if self.status["folga"] == False:
                    if self.status["id_vaga"]:
                        if self.status["depressao"] != True:
                            self.status["folga_do_dia"] = self.status["folga"]
                            self.status["folga"] = True
                            self.trabalhar(id_trabalho=self.status["id_vaga"])
                            print("Hoje você trabalhou, amanhã é seu dia de folga!")
                        else:
                            faltou = self.sortear(chance=30)
                            if faltou:
                                print("Voce faltou por que se sentiu muito deprimido hoje!")
                                self.status["faltas"] += 1
                                self.status["folga"] = True
                else:
                    print("Hoje é seu dia de folga, aproveite para descansar!")
                    self.status["folga_do_dia"] = self.status["folga"]
                    self.status["folga"] = False

            if self.banco_inter["rende"]:
                if self.banco_inter["valor_em_conta"] < 5000:
                    self.banco_inter["valor_em_conta"] *= 1.05
                else:
                    print("Seu dinheiro não rende mais, tire uma parte para ele continuar rendendo!")
                    
            self.save()
        
        elif id == "mensal":
            self.virar_mes()

            # Recebe salário se estiver com carteira assinada
            if self.status["carteira_assinada"]:
                self.ganhar_money(self.trabalhos[self.pais_atual][self.status["id_vaga"]]["ganho"])
                print(f"Seu salário caiu! Valor: {self.trabalhos[self.pais_atual][self.status["id_vaga"]]["ganho"]}")
                self.save_achievements("básicos", "Dinheiro sempre é bom, né?")

            # Atualiza investimentos se houver valor investido
            if self.banco_inter["investiu"]:
                self.banco_inter["investido"] *= 1.10

            # Pagamento automático de boletos no começo do mês
            for boleto in self.boletos:
                if self.boletos[boleto]["pago"] == False:
                    if self.status["money"] >= self.boletos[boleto]["valor"]:
                        self.perder_money(perda=self.boletos[boleto]["valor"])
                        self.boletos[boleto]["pago"] = True
                        print("Boletos pagos!\n")
                        print(f"Total pago: {sum(self.boletos[boleto]['valor'] for boleto in self.boletos)}\n")
                        self.save_achievements("básicos", "Acabou de entrar e já saiu...")

        elif id == "anual":
            pass
