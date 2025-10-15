import requests
import time
import json
from datetime import datetime

# --- 1. CONFIGURAÇÃO ---
GITHUB_TOKEN = ""
INPUT_JSON_FILE = "repositorios_filtrados_em_lotes2.json"
OUTPUT_JSON_FILE = "dados_pull_requests3.json"

# <--- ALTERAÇÃO: Limite de PRs a serem buscados por repositório
MAX_PRS_TO_FETCH_PER_REPO = 1000


# --- 2. QUERY GRAPHQL COMPLETA ---
# <--- ALTERAÇÃO: Aumentado de 'first: 50' para 'first: 100' para buscar mais rápido
GET_ALL_PR_DETAILS_QUERY = """
query GetAllPullRequestDetails($searchQuery: String!, $cursor: String) {
  search(query: $searchQuery, type: ISSUE, first: 100, after: $cursor) {
    issueCount
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      ... on PullRequest {
        url
        number
        title
        author { login }
        createdAt
        closedAt
        merged
        additions
        deletions
        changedFiles
        body
        participants(first: 1) { totalCount }
        comments(first: 1) { totalCount }
        reviewThreads(first: 1) { totalCount }
        reviews(first: 1) { totalCount }
      }
    }
  }
}
"""

# --- 3. FUNÇÕES DE APOIO ---


def run_graphql_query(query, variables):
    headers = {"Authorization": f"bearer {GITHUB_TOKEN}"}
    response = requests.post("https://api.github.com/graphql",
                             json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    return response.json()


def run_query_with_retry(query, variables, retry_delay_seconds=5):
    while True:
        try:
            return run_graphql_query(query, variables)
        except requests.exceptions.RequestException as e:
            print(
                f"\n⚠️ Erro de comunicação com a API: {e}. Tentando novamente em {retry_delay_seconds} segundos...")
            time.sleep(retry_delay_seconds)


def load_repositories_from_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        repo_list = [repo['nameWithOwner'] for repo in data]
        print(
            f"✅ Sucesso! Carregados {len(repo_list)} repositórios do arquivo '{filename}'.")
        return repo_list
    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo de entrada '{filename}' não foi encontrado.")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(
            f"❌ ERRO: Falha ao ler ou processar o arquivo JSON '{filename}'. Verifique o formato do arquivo.")
        print(f"   Detalhe do erro: {e}")
        return []

# --- 4. SCRIPT PRINCIPAL DE EXTRAÇÃO ---


def main():
    target_repositories = load_repositories_from_json(INPUT_JSON_FILE)
    if not target_repositories:
        print("Nenhum repositório para processar. Encerrando o script.")
        return

    all_prs_data = []
    total_repos = len(target_repositories)

    print(f"\nIniciando extração de dados para {total_repos} repositório(s).")
    print(f"Limite de {MAX_PRS_TO_FETCH_PER_REPO} PRs por repositório.")

    for i, repo_full_name in enumerate(target_repositories):
        print(
            f"\n--- Processando Repositório {i+1}/{total_repos}: {repo_full_name} ---")

        has_next_page = True
        cursor = None
        prs_fetched_for_repo = 0
        search_query_string = f"repo:{repo_full_name} is:pr is:closed reviews:>=1"

        while has_next_page:
            if prs_fetched_for_repo >= MAX_PRS_TO_FETCH_PER_REPO:
                print(f"  ... Limite de {MAX_PRS_TO_FETCH_PER_REPO} PRs atingido. Pulando para o próximo repositório.")
                break

            variables = {"searchQuery": search_query_string, "cursor": cursor}
            result = run_query_with_retry(GET_ALL_PR_DETAILS_QUERY, variables)
            
            if not result or 'data' not in result or not result['data']['search']:
                print(f"  ❗️ Falha ao obter dados ou sem resultados para a query. Resposta: {result}")
                break

            search_data = result['data']['search']
            pull_requests = search_data['nodes']
            
            for pr in pull_requests:
                # <--- CORREÇÃO AQUI ---
                # Adiciona uma verificação para ignorar PRs nulos ou inacessíveis
                if not pr:
                    print("  ... Encontrado um Pull Request nulo ou inacessível. Ignorando.")
                    continue # Pula para o próximo item do loop

                if prs_fetched_for_repo >= MAX_PRS_TO_FETCH_PER_REPO:
                    break
                
                # O resto do seu código continua normalmente
                created_at = datetime.fromisoformat(pr['createdAt'].replace('Z', '+00:00'))
                closed_at = datetime.fromisoformat(pr['closedAt'].replace('Z', '+00:00'))
                tempo_analise_delta = closed_at - created_at
                num_comentarios_total = pr['comments']['totalCount'] + pr['reviewThreads']['totalCount']
                
                all_prs_data.append({
                    'repositorio': repo_full_name,
                    'pr_number': pr['number'],
                    'pr_url': pr['url'],
                    'titulo': pr['title'],
                    'autor': (pr.get('author') or {}).get('login', 'N/A'),
                    'estado': 'MERGED' if pr['merged'] else 'CLOSED',
                    'data_criacao': pr['createdAt'],
                    'data_fechamento': pr['closedAt'],
                    'tempo_analise_dias': round(tempo_analise_delta.total_seconds() / 86400, 2),
                    'num_arquivos_alterados': pr['changedFiles'],
                    'linhas_adicionadas': pr['additions'],
                    'linhas_removidas': pr['deletions'],
                    'tamanho_descricao_caracteres': len(pr.get('body', '') or ''),
                    'num_participantes': pr['participants']['totalCount'],
                    'num_comentarios': num_comentarios_total,
                    'num_revisoes': pr['reviews']['totalCount'],
                })
                prs_fetched_for_repo += 1

            total_prs_in_repo = search_data['issueCount']
            print(f"  ... Buscados {prs_fetched_for_repo} de {total_prs_in_repo} Pull Requests.")

            has_next_page = search_data['pageInfo']['hasNextPage']
            cursor = search_data['pageInfo']['endCursor']
            time.sleep(1)

    print(
        f"\n--- Extração Finalizada. Total de {len(all_prs_data)} PRs coletados. ---")

    # --- 5. SALVANDO DADOS EM JSON ---
    if not all_prs_data:
        print("Nenhum dado de PR foi coletado. O arquivo JSON não será gerado.")
        return

    print(f"Salvando dados no arquivo: {OUTPUT_JSON_FILE}")
    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_prs_data, jsonfile, ensure_ascii=False, indent=4)

    print("✅ Processo concluído com sucesso!")


if __name__ == "__main__":
    main()
