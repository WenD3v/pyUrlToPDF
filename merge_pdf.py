import os
import PyPDF2
from datetime import datetime

# Função para obter a data de criação de um arquivo
def get_creation_date(filepath):
    return os.path.getctime(filepath)

# Caminho para a pasta contendo os PDFs
pdf_folder = "output_pdfs/"

# Lista todos os arquivos na pasta
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Ordena os arquivos pela data de criação
pdf_files.sort(key=lambda x: get_creation_date(os.path.join(pdf_folder, x)))

# Cria um objeto de saída PDF
output_pdf = PyPDF2.PdfMerger()

# Adiciona cada PDF ao objeto de saída
for pdf_file in pdf_files:
    output_pdf.append(os.path.join(pdf_folder, pdf_file))

# Especifica o caminho e nome do PDF final
output_path = os.path.join(pdf_folder, "PDF_combinado.pdf")

# Escreve o PDF combinado para o disco
with open(output_path, "wb") as output_f:
    output_pdf.write(output_f)

print(f"PDF combinado criado em: {output_path}")
