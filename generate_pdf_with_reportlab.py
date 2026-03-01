from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from PyPDF2 import PdfReader, PdfWriter
import logging
import os
from datetime import datetime
import re

from reportlab_pages.draw_client_page import draw_client_page
from reportlab_pages.draw_cover_page import draw_cover_page
from reportlab_pages.draw_index_page import draw_index_page
from reportlab_pages.draw_index_of_figures_and_tables import draw_index_of_figures_and_tables
from reportlab_pages.draw_packing_list_page import draw_packing_list_page
from reportlab_pages.draw_narrative_page import draw_narrative_page
from reportlab_pages.draw_statement_page import draw_statement_page
from reportlab_pages.draw_vessel_page import draw_vessel_page
from reportlab_pages.draw_crane_page import draw_crane_page
from reportlab_pages.draw_cargos_page import draw_cargos_page
from reportlab_pages.draw_lifting_page import draw_lifting_page
from reportlab_pages.draw_operation_page import draw_operation_page
from reportlab_pages.draw_stowage_page import draw_stowage_page
from reportlab_pages.draw_conclusion_page import draw_conclusion_page
from reportlab_pages.draw_remarks_page import draw_remarks_page
from reportlab_pages.draw_lashing_page import draw_lashing_page
from utils.register_fonts import register_fonts
from utils.set_page import set_page
from utils.data_loaders import load_demanda_data, load_cargo_table, load_lifting_table, load_lashing_table, load_demanda_ids
from utils.upload_pdf_to_drive import upload_report_to_drive
from querys.update_create_pdf import update_created_status

def generate_pdf_with_reportlab():
    try:
        output = io.BytesIO()
        register_fonts()

        # Carregar dados principais com verificação
        result = load_demanda_ids()
        if result is None:
            logging.error("load_demanda_ids() returned None - check database connection")
            return
        demanda_id_data, error = result
        if error:
            logging.error(f"Error loading demanda IDs: {error}")
            return
        if not demanda_id_data:
            logging.info("No pending surveys to process")
            return

        for item in demanda_id_data:
            demanda_id = item["id_demanda"]
            logging.info(f"Processing survey ID: {demanda_id}")
            
            # Carregar dados da demanda
            result = load_demanda_data(demanda_id)
            if result is None:
                logging.error(f"load_demanda_data({demanda_id}) returned None")
                continue
            demanda_data, error = result
            if error:
                logging.error(f"Error loading demanda data for {demanda_id}: {error}")
                continue
            
            # Carregar dados de cargo
            result = load_cargo_table(demanda_id)
            if result is None:
                logging.error(f"load_cargo_table({demanda_id}) returned None")
                continue
            table_data_cargo, error = result
            if error:
                logging.error(f"Error loading cargo table for {demanda_id}: {error}")
                continue
            
            # Carregar dados de lifting
            result = load_lifting_table(demanda_id)
            if result is None:
                logging.error(f"load_lifting_table({demanda_id}) returned None")
                continue
            table_data_lifting, error = result
            if error:
                logging.error(f"Error loading lifting table for {demanda_id}: {error}")
                continue
            
            # Carregar dados de lashing
            result = load_lashing_table(demanda_id)
            if result is None:
                logging.error(f"load_lashing_table({demanda_id}) returned None")
                continue
            table_data_lashing, error = result
            if error:
                logging.error(f"Error loading lashing table for {demanda_id}: {error}")
                continue

            c = canvas.Canvas(output, pagesize=A4)
            width, height = A4

            # Geração das páginas
            draw_cover_page(c, width, height, demanda_data["cliente"], demanda_data["subject"], 
                            demanda_data["vessel"], demanda_data["cargos"], demanda_data["dt_abertura"])
            
            c.bookmarkPage("cliente")
            draw_client_page(c, width, height, demanda_data["cliente"], demanda_data["subject"], demanda_data["nm_demanda"], demanda_id)
            
            if demanda_data["cod_atividade"] == "2":
                index_data = [
                        {"title": "1. PACKING LIST", "page_num": None, "bookmark_key": "packing_list"},
                        {"title": "2. NARRATIVE/SURVEY CIRCUMSTANCES", "page_num": None, "bookmark_key": "narrative"},
                        {"title": "3. STATEMENT OF FACTS", "page_num": None, "bookmark_key": "statement"},
                        {"title": "4. VESSEL", "page_num": None, "bookmark_key": "vessel"},
                        {"title": "5. VESSEL'S CRANE", "page_num": None, "bookmark_key": "crane"},
                        {"title": "6. CARGOS", "page_num": None, "bookmark_key": "cargo"},
                        {"title": "7. LIFTING APPLIANCES & EQUIPMENT", "page_num": None, "bookmark_key": "lifting"},
                        {"title": "8. CARGOS OPERATION", "page_num": None, "bookmark_key": "operation"},
                        {"title": "9. STOWAGE AREA", "page_num": None, "bookmark_key": "stowage"},
                        {"title": "10. QHSE REMARKS / POINTS TO IMPROVE", "page_num": None, "bookmark_key": "remarks"},
                        {"title": "11. CONCLUSION/ REMARKS", "page_num": None, "bookmark_key": "conclusion"},
                    ]
                index_table_data = [
                        {"title": "Table 1 – Cargos Characteristics", "page_num": None, "bookmark_key": "packing_list"},
                        {"title": "Table 2 – Lifting Appliances Description", "page_num": None, "bookmark_key": "lifting"},
                ]
            else:
                index_data = [
                        {"title": "1. PACKING LIST", "page_num": None, "bookmark_key": "packing_list"},
                        {"title": "2. NARRATIVE/SURVEY CIRCUMSTANCES", "page_num": None, "bookmark_key": "narrative"},
                        {"title": "3. STATEMENT OF FACTS", "page_num": None, "bookmark_key": "statement"},
                        {"title": "4. VESSEL", "page_num": None, "bookmark_key": "vessel"},
                        {"title": "5. VESSEL'S CRANE", "page_num": None, "bookmark_key": "crane"},
                        {"title": "6. CARGOS", "page_num": None, "bookmark_key": "cargo"},
                        {"title": "7. LIFTING APPLIANCES & EQUIPMENT", "page_num": None, "bookmark_key": "lifting"},
                        {"title": "8. LASHING APPLIANCES & EQUIPMENT", "page_num": None, "bookmark_key": "lashing"},
                        {"title": "9. CARGOS OPERATION", "page_num": None, "bookmark_key": "operation"},
                        {"title": "10. STOWAGE AREA", "page_num": None, "bookmark_key": "stowage"},
                        {"title": "11. QHSE REMARKS / POINTS TO IMPROVE", "page_num": None, "bookmark_key": "remarks"},
                        {"title": "12. CONCLUSION/ REMARKS", "page_num": None, "bookmark_key": "conclusion"},
                ]
                index_table_data = [
                        {"title": "Table 1 – Cargos Characteristics", "page_num": None, "bookmark_key": "packing_list"},
                        {"title": "Table 2 – Lifting Appliances Description", "page_num": None, "bookmark_key": "lifting"},
                        {"title": "Table 3 – Lashing Appliances Description", "page_num": None, "bookmark_key": "lashing"},
                ]

            index_figures_data = []
            
            c.showPage()
            set_page(index_data, "packing_list", c.getPageNumber())
            set_page(index_table_data, "packing_list", c.getPageNumber())
            c.bookmarkPage("packing_list")
            draw_packing_list_page(c, width, height, table_data_cargo, demanda_data["cliente"])

            quantity = 0 if (len(table_data_cargo) == 1 and all(cell.strip() == "-" for cell in table_data_cargo[0])) else len(table_data_cargo)

            c.showPage()
            set_page(index_data, "narrative", c.getPageNumber())
            c.bookmarkPage("narrative")
            index_figures_narrative = draw_narrative_page(c, width, height, demanda_data["cliente"], demanda_data["vessel"], 
                                                          demanda_data["location"], quantity, demanda_data["dt_abertura"], 
                                                          demanda_data["bollards_aft"], demanda_data["bollards_fwd"], demanda_id)
            index_figures_data.extend(index_figures_narrative)

            c.showPage(); set_page(index_data, "statement", c.getPageNumber()); c.bookmarkPage("statement"); 
            draw_statement_page(c, width, height, demanda_id, table_data_cargo)

            c.showPage(); set_page(index_data, "vessel", c.getPageNumber()); c.bookmarkPage("vessel"); 
            draw_vessel_page(c, width, height, demanda_data["vessel"], demanda_data["vessel_type"], 
                            demanda_data["country_flag"], demanda_data["imo_number"], demanda_data["year_of_built"], 
                            demanda_data["dwt"], demanda_data["vessel_breadth"], demanda_data["vessel_length"])
            
            c.showPage(); set_page(index_data, "crane", c.getPageNumber()); c.bookmarkPage("crane"); 
            index_figures_crane = draw_crane_page(c, width, height, demanda_data["vessel"], demanda_id, 
                                                  demanda_data["vessel_id"])
            index_figures_data.extend(index_figures_crane)

            c.showPage(); set_page(index_data, "cargo", c.getPageNumber()); c.bookmarkPage("cargo"); 
            index_figures_cargo, figure_number = draw_cargos_page(c, width, height, demanda_id, table_data_cargo)
            index_figures_data.extend(index_figures_cargo)

            c.showPage() 
            set_page(index_data, "lifting", c.getPageNumber())
            set_page(index_table_data, "lifting", c.getPageNumber())
            c.bookmarkPage("lifting")
            index_figures_lifting, figure_number = draw_lifting_page(c, width, height, demanda_id, table_data_lifting, 
                                                                     figure_number)
            index_figures_data.extend(index_figures_lifting)

            if demanda_data["cod_atividade"] != "2":
                c.showPage() 
                set_page(index_data, "lashing", c.getPageNumber())
                set_page(index_table_data, "lashing", c.getPageNumber())
                c.bookmarkPage("lashing")
                index_figures_lashing, figure_number = draw_lashing_page(c, width, height, demanda_id, 
                                                                         table_data_lashing, figure_number)
                index_figures_data.extend(index_figures_lashing)

            c.showPage(); set_page(index_data, "operation", c.getPageNumber()); c.bookmarkPage("operation"); 
            index_figures_operation, figure_number = draw_operation_page(c, width, height, demanda_id, table_data_cargo, 
                                                                         figure_number, demanda_data["cod_atividade"])
            index_figures_data.extend(index_figures_operation)

            c.showPage(); set_page(index_data, "stowage", c.getPageNumber()); c.bookmarkPage("stowage"); 
            index_figures_stowage = draw_stowage_page(c, width, height, demanda_id, table_data_cargo, figure_number, 
                                                      demanda_data["cod_atividade"])
            index_figures_data.extend(index_figures_stowage)

            c.showPage(); set_page(index_data, "remarks", c.getPageNumber()); c.bookmarkPage("remarks"); 
            draw_remarks_page(c, width, height, demanda_data["cod_atividade"], demanda_id)
            
            c.showPage(); set_page(index_data, "conclusion", c.getPageNumber()); c.bookmarkPage("conclusion"); 
            draw_conclusion_page(c, width, height, demanda_data["cod_atividade"], demanda_id)

            c.showPage()
            draw_index_of_figures_and_tables(c, width, height, index_figures_data, index_table_data)

            c.showPage()
            draw_index_page(c, width, height, index_data)

            c.save()
            output.seek(0)

            logging.info(f"PDF generation successful (ReportLab), length: {len(output.getbuffer())}")

            # Reorganizar páginas usando PyPDF2
            output.seek(0)
            reader = PdfReader(output)
            writer = PdfWriter()

            num_pages = len(reader.pages)

            # Posições importantes
            cover_page = 0
            client_page = 1
            index2 = num_pages - 1

            # 1. Capa
            writer.add_page(reader.pages[cover_page])

            # 2. Cliente
            writer.add_page(reader.pages[client_page])

            # 3. Índices (a última página)
            writer.add_page(reader.pages[index2])

            # 4. Demais páginas (do 2 até index1-1)
            for i in range(2, index2):
                writer.add_page(reader.pages[i])

            # Novo PDF reorganizado
            final_output = io.BytesIO()
            writer.write(final_output)
            final_output.seek(0)
        
            # Criar diretório pdf_<demanda_id> se não existir
            base_dir = os.path.join("generate_pdf")
            pasta_destino = os.path.join(base_dir, f"pdf_{demanda_id}")

            os.makedirs(pasta_destino, exist_ok=True)

            # Gerar timestamp no formato dd-mm-yyyy_hh-mm
            current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M")
            # Limpar nome_demanda (permitindo apenas letras, números e underscore)
            raw_nome_demanda = demanda_data["nome_demanda"]
            nome_demanda_clean = re.sub(r'[^A-Za-z0-9]+', '_', raw_nome_demanda).strip('_')

            # Definir nome do arquivo como survey_<id>_<data>.pdf
            file_name = f"survey_{nome_demanda_clean}_{current_datetime}.pdf"

            # Caminho completo do arquivo
            file_path = os.path.join(pasta_destino, file_name)

            # Salvar o PDF no disco
            with open(file_path, "wb") as f:
                f.write(final_output.read())

            logging.info(f"PDF salvo em: {file_path}")

            # Enviar para o Google Drive
            file_url = upload_report_to_drive(
                file_path=file_path,
                folder_id=demanda_data["id_pasta_gd_demanda"]
            )

            # Apagar o arquivo PDF
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Arquivo deletado: {file_path}")

            # Apagar o diretório (se estiver vazio)
            if os.path.exists(pasta_destino) and not os.listdir(pasta_destino):
                os.rmdir(pasta_destino)
                logging.info(f"Pasta deletada: {pasta_destino}")

            ok, error = update_created_status(demanda_id, file_url)
            if ok:
                print("Created atualizado com sucesso ✅")
            else:
                print("Erro:", error)

    except Exception as e: 
        logging.error(f"PDF generation error (ReportLab): {e}", exc_info=True) 
        return

if __name__ == "__main__":
    generate_pdf_with_reportlab()

import requests
import os

def shutdown_vm():
    # Obtém metadados da instância
    metadata_server = "http://metadata.google.internal/computeMetadata/v1"
    headers = {"Metadata-Flavor": "Google"}
    project_id = requests.get(f"{metadata_server}/project/project-id", headers=headers).text
    zone = requests.get(f"{metadata_server}/instance/zone", headers=headers).text.split("/")[-1]
    instance_name = requests.get(f"{metadata_server}/instance/name", headers=headers).text

    # Obtém o token de autenticação da conta de serviço da VM
    token = requests.get(f"{metadata_server}/instance/service-accounts/default/token", headers=headers).json()["access_token"]

    # Faz requisição para parar a VM
    compute_url = f"https://compute.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/instances/{instance_name}/stop"
    response = requests.post(
        compute_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    print("Shutdown response:", response.status_code, response.text)

# No fim do script:
shutdown_vm()
