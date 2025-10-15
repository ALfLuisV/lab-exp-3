import requests
import json
import time

# --- CONFIGURAÇÃO ---
# ⚠️ SUBSTITUA PELO SEU TOKEN DE ACESSO PESSOAL DO GITHUB
GITHUB_TOKEN = ""
GITHUB_API_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

# Limites
MAX_REPOS_TO_CHECK = 200  # Máximo de repositórios para buscar no total (pode ser 500, 1000, etc.)
MIN_PRS_REQUIRED = 100    # Mínimo de PRs fechados/mesclados para manter o repositório

# --- QUERIES GRAPHQL ---
# 1. Busca os nomes dos 100 repositórios mais populares por vez.
TOP_REPOS_QUERY = """
query GetTopRepositoriesList($cursor: String) {
    search(
        query: "is:public stars:>=1000 sort:stars-desc"
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
            }
        }
    }
}
"""

# 2. Busca detalhes dos PRs para um único repositório.
REPO_PR_DETAILS_QUERY = """
query GetRepositoryPullRequestDetails($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
        nameWithOwner
        pullRequests(states: [MERGED, CLOSED], first: 200) {
            totalCount
            nodes {
                ... on PullRequest {
                    title
                    # ... outros campos de PRs
                    state
                    createdAt
                    mergedAt
                    # Mantive apenas alguns campos para brevidade, adicione o restante se necessário.
                }
            }
        }
    }
}
"""


REPO_PR_DETAILS_QUERY2 = """
query SearchPullRequestsWithReviews($searchQuery: String!) {
  search(query: $searchQuery, type: ISSUE, first: 100) {
    issueCount
    nodes {
      ... on PullRequest {
        title
        url
        state
        createdAt
        mergedAt
        # Adicionado para você poder verificar a contagem de revisões
        reviews(first: 1) {
          totalCount
        }
      }
    }
  }
}
"""

def run_graphql_query(query, variables=None):
    """Função genérica para executar qualquer query GraphQL."""
    data = {'query': query, 'variables': variables}
    response = requests.post(GITHUB_API_URL, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: Status Code {response.status_code}")
        print(response.text)
        return None
    

def run_query_with_retry(query, variables, retry_delay_seconds=10):
    """
    Executa uma query GraphQL, com retentativas infinitas em caso de erro de rede ou servidor (como 502).
    """
    while True:
        try:
            # Tenta executar a query original
            result = run_graphql_query(query, variables)
            return result
        except requests.exceptions.RequestException as e:
            # Captura qualquer exceção da biblioteca requests (incluindo timeouts, erros de conexão e erros HTTP como 502)
            print(f"\n⚠️ Erro de comunicação com a API: {e}. Tentando novamente em {retry_delay_seconds} segundos...")
            time.sleep(retry_delay_seconds)


def fetch_process_and_filter():
    """Busca repositórios em lotes, processa e filtra cada lote."""
    print(f"--- INICIANDO COLETA E FILTRAGEM ---")
    print(f"Meta: {MAX_REPOS_TO_CHECK} repositórios. Filtro: >= {MIN_PRS_REQUIRED} PRs.")
    
    all_filtered_repos = []
    cursor = None
    repos_checked_count = 0
    
    while repos_checked_count < MAX_REPOS_TO_CHECK:
        print(f"\n--- Buscando lote de repositórios (Início: {repos_checked_count + 1})... ---")
        
        # 1. Executa a primeira query para buscar o lote
        variables = {"cursor": cursor}
        result = run_graphql_query(TOP_REPOS_QUERY, variables)
        

        if not result or 'data' not in result or not result['data']['search']['nodes']:
            print("Não foi possível buscar mais repositórios ou atingiu o final da lista.")
            break

        search_data = result['data']['search']
        repo_batch = [node['nameWithOwner'] for node in search_data['nodes'] if node]
        
        if not repo_batch:
            print("Lote vazio, encerrando busca.")
            break

        # 2. Processa e filtra o lote
        print(f"Lote de {len(repo_batch)} repositórios coletado. Iniciando filtragem...")
        
        for full_name in repo_batch:
            if repos_checked_count >= MAX_REPOS_TO_CHECK:
                break
                
            # A query de busca precisa de uma string formatada, não de owner/name separados
            search_query_string = f"repo:{full_name} is:pr is:closed"

            print(f"Verificando repositório: {full_name}...")

            # A ÚNICA MUDANÇA REAL NO SEU LOOP É ESTA LINHA:
            # Trocamos `run_graphql_query` por `run_query_with_retry`
            pr_details_result = run_query_with_retry(
                REPO_PR_DETAILS_QUERY2, 
                {"searchQuery": search_query_string}
            )
            
            repos_checked_count += 1
            
            # Adaptei a lógica para a query de busca (search) que retorna `issueCount`
            if pr_details_result and 'data' in pr_details_result and pr_details_result['data']['search']:
                repo_data = pr_details_result['data']['search']
                pr_count = repo_data['issueCount']
                
                if pr_count >= MIN_PRS_REQUIRED:
                    # Como a busca não retorna o nameWithOwner, adicionamos manualmente
                    repo_info = {'nameWithOwner': full_name, 'pullRequests': {'totalCount': pr_count}}
                    all_filtered_repos.append(repo_info)
                    print(f"  [{repos_checked_count}/{MAX_REPOS_TO_CHECK}] ✅ {full_name}: {pr_count} PRs. (Mantido)")
                else:
                    print(f"  [{repos_checked_count}/{MAX_REPOS_TO_CHECK}] ❌ {full_name}: {pr_count} PRs. (Descartado)")
            else:
                # Se a API retornar um erro no JSON (diferente de um erro HTTP)
                print(f"  [{repos_checked_count}/{MAX_REPOS_TO_CHECK}] ❗️ Falha ao obter dados para {full_name}. Resposta: {pr_details_result}")

            time.sleep(0.3) # Pequena pausa para evitar Rate Limit
        
        # 4. Configura para a próxima iteração
        cursor = search_data['pageInfo']['endCursor']
        has_next_page = search_data['pageInfo']['hasNextPage']
        
        if not has_next_page:
            print("Atingiu o final da lista de repositórios no GitHub.")
            break

    return all_filtered_repos

def save_to_json(data, filename="repositorios_filtrados_em_lotes2.json"):
    """Salva os dados coletados em um arquivo JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n--- SUCESSO! Dados finais salvos em '{filename}' ({len(data)} repositórios mantidos) ---")

if __name__ == "__main__":
    if GITHUB_TOKEN == "SEU_TOKEN_AQUI":
        print("ERRO: Por favor, substitua 'SEU_TOKEN_AQUI' pelo seu Personal Access Token do GitHub.")
    else:
        final_filtered_data = fetch_process_and_filter()
        save_to_json(final_filtered_data)