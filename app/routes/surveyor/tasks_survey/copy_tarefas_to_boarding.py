from flask import request, jsonify
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import task_survey_schema

@tasks_survey_bp.route('/boarding/copy_from_tarefas', methods=['POST'])
def copy_tarefas_to_boarding():
    """
    Copy all records from tbl_tarefas to tbl_task_survey_boarding.
    """
    current_session = Session()
    try:
        # Fetch all records from tbl_tarefas
        tarefas = current_session.execute(
            text("""
                SELECT id_tarefas, demanda, nome_demanda, nome_tarefa, descricao
                FROM tbl_tarefas 
                WHERE tipo = 'OPERAÇÕES'
            """)
        ).fetchall()

        if not tarefas:
            return jsonify({"message": "No records found in tbl_tarefas."}), 404

        # Insert each record into tbl_task_survey_boarding
        for tarefa in tarefas:
            demanda = current_session.execute(
                text("""
                    SELECT id_demanda, nome_demanda
                        FROM tbl_demandas
                        WHERE nome_demanda = :nome_demanda AND numero = :numero
                """),
                {
                    "nome_demanda": tarefa.nome_demanda,
                    "numero": str(tarefa.demanda)
                }
            ).fetchone()

            if not demanda:
                continue

            id_demanda = demanda._mapping["id_demanda"]
            nome_demanda = demanda._mapping["nome_demanda"]

            print(f"{id_demanda} - {nome_demanda}")

            current_session.execute(
                text("""
                    INSERT INTO tbl_task_survey_boarding (
                        id_task, id_survey, task_title, task_description,
                        finished, last_task_done, num_bollards_fwd, num_bollards_aft,
                        finished_mark_one, finished_mark_two, finished_mark_three
                    )
                    VALUES (
                        :id_task, :id_survey, :task_title, :task_description,
                        false, -1, 0, 0,
                        false, false, false
                    )
                """),
                {
                    "id_task": tarefa.id_tarefas,
                    "id_survey": id_demanda,
                    "task_title": tarefa.nome_tarefa,
                    "task_description": tarefa.descricao
                }
            )

        current_session.commit()
        return jsonify({"message": f"Copied {len(tarefas)} records from tbl_tarefas to tbl_task_survey_boarding."}), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error copying tarefas: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()