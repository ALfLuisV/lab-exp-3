import requests
import json
import time
import os 

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


URL = "https://api.github.com/graphql"

# --- MUDANÇA 1: Query Corrigida ---
# A variável $cursor precisa ser usada dentro da função search(after: $cursor)
# Também adicionei 'language:Java' para corresponder ao seu objetivo (opcional)
QUERY = """
query TopRepositories($cursor: String) {
  search(
    query: "is:public stars:>1000 sort:stars-desc"
    type: REPOSITORY
    first: 100
    after: $cursor
  ) {
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      ... on Repository {
        nameWithOwner
        pullRequests(states: [MERGED, CLOSED], first: 100) {
          totalCount
          nodes {
            ... on PullRequest {
              title
              number
              state
              url
              createdAt
              mergedAt
              closedAt
              author {
                login
              }
              reviews(first: 1) {
                totalCount
              }
              comments {
                totalCount
              }
              additions
              deletions
              changedFiles
            }
          }
        }
      }
    }
  }
}
"""

def run_query(query, variables):
    """
    Função para executar a query GraphQL, com retentativas e timeout.
    """
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    max_retries = 5
    base_wait_time = 5

    for attempt in range(max_retries):
        try:
            request = requests.post(
                URL, 
                json={'query': query, 'variables': variables}, 
                headers=headers, 
                timeout=30
            )
            
            if request.status_code == 502:
                print(f"  -> Tentativa {attempt + 1}/{max_retries}: Recebido erro 502 (Bad Gateway). Tentando novamente em {base_wait_time * (attempt + 1)}s...")
                time.sleep(base_wait_time * (attempt + 1))
                continue

            request.raise_for_status()
            
            return request.json()

        except requests.exceptions.RequestException as e:
            print(f"  -> Tentativa {attempt + 1}/{max_retries}: Ocorreu um erro de requisição: {e}. Tentando novamente em {base_wait_time * (attempt + 1)}s...")
            time.sleep(base_wait_time * (attempt + 1))
    
    raise Exception(f"Query falhou após {max_retries} tentativas.")

def get_top_repos():
    all_repos = []
    cursor = None
    
    # Vamos buscar 2 páginas para obter os 200 repositórios mais populares
    num_pages_to_fetch = 2
    
    print("Iniciando a coleta de dados do GitHub...")
    
    for i in range(num_pages_to_fetch):
        print(f"Buscando página {i + 1}/{num_pages_to_fetch}...")
        variables = {"cursor": cursor}
        
        try:
            result = run_query(QUERY, variables)
        except Exception as e:
            print(f"Erro fatal ao buscar a página {i + 1}: {e}")
            break
        
        if "errors" in result:
            print("Erro na API do GitHub:", result["errors"])
            break

        search_data = result.get("data", {}).get("search", {})
        if not search_data:
            print("Não foram encontrados dados na resposta da API.")
            break

        # --- MUDANÇA 2: Acumulando os dados corretamente ---
        # Usamos extend() para adicionar os itens da lista 'nodes' à nossa lista principal
        # Em vez de adicionar a página inteira com append()
        if 'nodes' in search_data:
            all_repos.extend(search_data['nodes'])
        
        page_info = search_data.get('pageInfo', {})
        has_next_page = page_info.get('hasNextPage', False)
        
        # --- MUDANÇA 3: Atualizando o cursor para a próxima página ---
        if has_next_page:
            cursor = page_info.get('endCursor')
        else:
            print("Chegamos à última página de resultados.")
            break
            
    print(f"\nColeta finalizada. Total de {len(all_repos)} repositórios encontrados.")
    return all_repos

# --- Execução Principal ---
if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("ERRO: A variável de ambiente GITHUB_TOKEN não está definida.")
    else:
        repositories = get_top_repos()
        
        if repositories:
            # --- MUDANÇA 4: Usando modo 'w' para escrever o arquivo JSON ---
            # O modo 'a' (append) corromperia o arquivo JSON em execuções múltiplas.
            output_filename = "github_data.json"
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(repositories, f, ensure_ascii=False, indent=2)
            print(f"Dados salvos com sucesso em '{output_filename}'")