import os
import pdfkit
from urllib.parse import urlparse
import fitz

# Configuração do wkhtmltopdf
path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
if not os.path.exists(path_wkhtmltopdf):
    print("Caminho do wkhtmltopdf não encontrado:", path_wkhtmltopdf)
else:
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


def extract_filename_from_url(url):
    # Extraí o caminho da URL
    path = urlparse(url).path
    # Obtém o último segmento do caminho e remove a extensão se houver
    filename = os.path.basename(path).replace('.html', '')
    # Substitui caracteres indesejados por '_'
    filename = filename.replace('/', '_').replace(' ', '_')
    return filename

def pdf_contains_images(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            if len(page.get_images(full=True)) > 0:
                return True
        return False
    except Exception as e:
        print(f"Erro ao verificar imagens no PDF: {str(e)}")
        return False

def convert_urls_to_pdf(url,output_file):

    options = {
        '--page-width': '1920px',  # Largura da página
        '--page-height': '1200px',  # Altura da página
        '--load-error-handling': 'ignore',  # Ignorar erros de carregamento
        '--margin-left': '0mm',
        '--margin-right': '0mm',
        '--margin-top': '0mm',
        '--margin-bottom': '0mm',
        '--dpi': '96',
        '--no-background':None,
        '--javascript-delay': '60000',  # Tempo de espera adicional para carregar scripts (em milissegundos)
        '--viewport-size': '1920x1200  # D', # define o tamanho da viewport
        '--run-script': "document.getElementById('atIdViewHeader').style.display = 'none'; document.querySelector('footer[jsname=\"yePe5c\"]').style.display = 'none'; var checkImages = function() { var images = document.images; for (var i = 0; i < images.length; i++) { if (!images[i].complete) { return false; } } return true; }; var waitForImages = function() { if (!checkImages()) { setTimeout(waitForImages, 100); } else { window.status = 'ready'; } }; waitForImages();"
    }

    try:
        print(f'Gerando PDF para {url}...')
        pdfkit.from_url(url, output_file, configuration=config, options=options)
        print(f'PDF gerado para {url}')
    except Exception as e:
        print(f'Erro ao gerar PDF para {url}: {str(e)}')

if __name__ == '__main__':

    input_file = 'urls.txt'  # Nome do arquivo de entrada com os URLs
    if not os.path.exists(input_file):
        print("Arquivo de entrada não encontrado:", input_file)
    else:
        if not os.path.exists('output_pdfs'):
            os.makedirs('output_pdfs')

        with open('urls.txt', 'r') as file:
            urls = file.readlines()

        for i, url in enumerate(urls):
            url = url.strip()
            if url:
                filename = extract_filename_from_url(url)
                output_file = os.path.join('output_pdfs', f'{filename}.pdf')

                attempt = 0
                while attempt < 3:  # Limite de tentativas
                    convert_urls_to_pdf(url, output_file)
                    if pdf_contains_images(output_file):
                        break
                    else:
                        print(f'Retentando gerar PDF para {url}, tentativa {attempt + 1}')
                    attempt += 1
                
                if attempt == 5:
                    print(f'Falha ao gerar PDF com imagens para {url} após 5 tentativas.')

                
