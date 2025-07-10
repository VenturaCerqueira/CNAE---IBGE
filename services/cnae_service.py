import requests
import time
from typing import List, Dict, Optional
from models.cnae_model import CnaeTratado

# --- Cache Simples em Memória ---
cache: Optional[Dict] = None
CACHE_DURATION_MS = 60 * 60 * 1000  # 1 hora em milissegundos
# -------------------------------

# --- Configurações de Batch e Retry ---
BATCH_SIZE = 15  # Tamanho do lote para requisições em paralelo
MAX_RETRIES = 2  # Número máximo de retentativas para cada requisição
RETRY_DELAY_MS = 500  # Tempo de espera inicial entre retentativas (em milissegundos)
# ------------------------------------

def process_subclasse_data(subclasse: Optional[Dict], classe_fallback: Optional[Dict] = None) -> Optional[CnaeTratado]:
    """Função para processar dados de subclasses."""
    if subclasse and subclasse.get('id') and subclasse.get('descricao'):
        return CnaeTratado(
            Codigo=str(subclasse['id']),
            Descricao=subclasse['descricao'],
            Percentual=0.0
        )
    elif classe_fallback and classe_fallback.get('id') and classe_fallback.get('descricao'):
        # Se a subclasse não for válida, retorna dados da classe como fallback
        return CnaeTratado(
            Codigo=f"{classe_fallback['id']}00",
            Descricao=classe_fallback['descricao'],
            Percentual=0.0
        )
    return None

def fetch_with_retry(url: str, retries: int = MAX_RETRIES, delay: int = RETRY_DELAY_MS) -> requests.Response:
    """Função auxiliar para buscar dados com retentativas."""
    try:
        response = requests.get(url, timeout=15)  # Timeout de 15 segundos
        response.raise_for_status()  # Lança uma exceção para erros HTTP
        return response
    except requests.exceptions.RequestException as e:
        if retries > 0:
            print(f"Retentando {url} ({retries} retentativas restantes) após erro: {e}")
            time.sleep(delay / 1000)  # Converter ms para segundos
            return fetch_with_retry(url, retries - 1, delay * 2)  # Backoff exponencial
        print(f"Falha ao buscar {url} após múltiplas retentativas: {e}")
        raise

async def get_cnae_classe_subclasse_data() -> List[CnaeTratado]:
    """Função principal para buscar dados de CNAE."""
    global cache
    now = int(time.time() * 1000)  # Captura o timestamp atual em milissegundos
    if cache and (now - cache['timestamp'] < CACHE_DURATION_MS):
        print('Retornando dados do cache.')
        return cache['data']

    print('Cache expirado ou inexistente. Buscando dados do IBGE...')
    ibge_api_url_classes = 'https://servicodados.ibge.gov.br/api/v2/cnae/classes'

    try:
        print(f"Buscando dados de classes em: {ibge_api_url_classes}")
        classes_response = fetch_with_retry(ibge_api_url_classes)
        classes = classes_response.json()

        if not isinstance(classes, list):
            print('Formato inesperado da resposta de classes do IBGE:', classes)
            raise ValueError('Formato inesperado da resposta de classes do IBGE')

        print(f"Encontradas {len(classes)} classes. Buscando subclasses em lotes de {BATCH_SIZE}...")

        processed_data_map = {}  # Usar dict para garantir unicidade por Codigo
        all_results = []

        # Processar em lotes
        for i in range(0, len(classes), BATCH_SIZE):
            batch = classes[i : i + BATCH_SIZE]
            print(f"Processando lote {i // BATCH_SIZE + 1} (classes {i + 1} a {min(i + BATCH_SIZE, len(classes))})...")

            batch_results = []
            for classe in batch:
                subclasses_url = f"https://servicodados.ibge.gov.br/api/v2/cnae/classes/{classe['id']}/subclasses"
                try:
                    response = fetch_with_retry(subclasses_url)
                    batch_results.append({'status': 'fulfilled', 'value': response.json(), 'class_data': classe})
                except Exception as e:
                    batch_results.append({'status': 'rejected', 'reason': str(e), 'class_data': classe})
            all_results.extend(batch_results)

        print('Todas as requisições de subclasses concluídas. Processando resultados...')

        # Processar todos os resultados coletados
        for result in all_results:
            if result['status'] == 'fulfilled':
                subclasses = result['value']
                classe_original = result['class_data']

                if isinstance(subclasses, list) and len(subclasses) > 0:
                    for subclasse in subclasses:
                        item = process_subclasse_data(subclasse)
                        if item and item.Codigo not in processed_data_map:
                            processed_data_map[item.Codigo] = item
                else:
                    # Array de subclasses vazio ou inválido
                    item = process_subclasse_data(None, classe_original)
                    if item and item.Codigo not in processed_data_map:
                        processed_data_map[item.Codigo] = item
            else:  # result['status'] == 'rejected'
                classe_original = result['class_data']
                error_reason = result['reason']
                print(f"Erro final ao buscar subclasses da classe {classe_original['id']}: {error_reason}")

                # Fallback com dados da classe
                item = process_subclasse_data(None, classe_original)
                if item and item.Codigo not in processed_data_map:
                    processed_data_map[item.Codigo] = item

        final_processed_data = list(processed_data_map.values())
        print(f"Dados processados: {len(final_processed_data)} itens únicos.")

        cache = {
            'data': final_processed_data,
            'timestamp': int(time.time() * 1000),
        }

        return final_processed_data

    except Exception as e:
        print(f"Erro GERAL ao buscar ou processar dados do IBGE: {e}")
        raise