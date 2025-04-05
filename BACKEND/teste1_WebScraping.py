import os
import re
import requests
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
DOWNLOAD_DIR = "downloads"
ZIP_FILENAME = "anexos_compactados.zip"

def get_anexo_links():
    """
    Busca os links dos arquivos dos Anexos (PDF) na página.
    Usa expressões regulares para identificar links que contenham 'Anexo_I' e terminem em '.pdf'.
    """
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    pdf_pattern = re.compile(r'Anexo_I.*\.pdf', re.IGNORECASE)
    
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if pdf_pattern.search(href):
            full_url = urljoin(BASE_URL, href)
            links.append(full_url)
            print(f"Link encontrado: {full_url}")
    return links

def download_files(links):
    """
    Faz o download dos arquivos dos links encontrados e os salva em DOWNLOAD_DIR.
    """
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    paths = []
    for url in links:
        filename = os.path.basename(url)
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        print(f"Baixando {filename}...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        paths.append(filepath)
    return paths

def zip_files(file_paths, zip_name):
    """
    Compacta os arquivos em file_paths em um arquivo ZIP.
    """
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            zipf.write(file_path, arcname=os.path.basename(file_path))
    print(f"Arquivos compactados em: {zip_name}")

def main():
    print("Iniciando o web scraping dos arquivos dos Anexos (PDF)...")
    links = get_anexo_links()
    if not links:
        print("Nenhum link encontrado.")
        return
    files = download_files(links)
    if files:
        zip_files(files, ZIP_FILENAME)

if __name__ == "__main__":
    main()
