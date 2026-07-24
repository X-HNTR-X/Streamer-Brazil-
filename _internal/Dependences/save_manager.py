import json, time, threading, copy, os, sys

# Trava para evitar conflito de gravação simultânea entre threads
lock = threading.Lock()


# Encontra o caminho correto do arquivo tanto em desenvolvimento quanto no executável (.exe)
def resolve_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(path):
            return path
    if getattr(sys, 'frozen', False):
        path = os.path.join(os.path.dirname(sys.executable), relative_path)
        if os.path.exists(path):
            return path
    return os.path.join(os.path.abspath("."), relative_path)


# Carrega os dados de um arquivo JSON e retorna o conteúdo (ou None em caso de erro/arquivo ausente)
def load_data(arquive):
    caminho_real = resolve_path(arquive)
    
    if not os.path.exists(caminho_real):
        return None
    try:
        with open(caminho_real, 'r', encoding='UTF-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError, OSError):
        return None


# Salva os dados no arquivo JSON de forma síncrona, garantindo que o diretório exista
def async_data(data, arquive):
    if getattr(sys, 'frozen', False):
        caminho_real = os.path.join(os.path.dirname(sys.executable), arquive)
    else:
        caminho_real = os.path.join(os.path.abspath("."), arquive)

    os.makedirs(os.path.dirname(caminho_real), exist_ok=True)

    with lock:
        time.sleep(1)
        with open(caminho_real, 'w', encoding='UTF-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


# Cria uma cópia dos dados e dispara o salvamento em uma thread separada em segundo plano
def async_data_background(data, arquive):
    data_copy = copy.copy(data)

    thread = threading.Thread(target=async_data, args=(data_copy, arquive))
    thread.start()
