import pygame, os, sys

# Pega o caminho correto (executável ou script)
def get_external_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SoundManager:
    def __init__(self):
        # Evita erro do WASAPI no Windows forçando o DirectSound
        os.environ['SDL_AUDIODRIVER'] = 'dsound'
        try:
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.mixer.init()
        except Exception:
            try:
                pygame.mixer.init()
            except Exception:
                pass

        self.sons = {}
        self.load_sounds()

    # Carrega efeitos sonoros
    def load_sounds(self):
        caminhos = {
            "achievements": get_external_path("Dependences/sounds/achievement.mp3"),
            "erro":         get_external_path("Dependences/sounds/error.mp3"),
            "click":        get_external_path("Dependences/sounds/click.mp3")
        }

        for nome, caminho in caminhos.items():
            if os.path.exists(caminho):
                self.sons[nome] = pygame.mixer.Sound(caminho)

    # Toca efeito por chave (ex: "erro")
    def play_sound(self, sound_name):
        if sound_name in self.sons:
            self.sons[sound_name].play()

    # Toca música de fundo em loop
    def play_background(self, back_sound_name):
        caminho_bg = get_external_path(f"Dependences/sounds/{back_sound_name}")
        if os.path.exists(caminho_bg):
            pygame.mixer.music.load(caminho_bg)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)

    # Para a música de fundo
    def stop_background(self):
        pygame.mixer.music.stop()
