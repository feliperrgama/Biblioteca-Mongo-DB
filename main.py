from bson.objectid import ObjectId
from datetime import datetime
from src.mongo_db import books_col, requests_col


def add_book(dados_livro):
    documento = {
        "title": dados_livro.get("title"),
        "author": dados_livro.get("author"),
        "isbn": dados_livro.get("isbn"),
        "year": int(dados_livro.get("year")) if dados_livro.get("year") else None,
        "copies": int(dados_livro.get("copies", 1)),
        "available": int(dados_livro.get("copies", 1)),
        "description": dados_livro.get("description", ""),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    resultado = books_col.insert_one(documento)
    return str(resultado.inserted_id)

def remove_book(id_livro):
    try:
        obj_id = ObjectId(id_livro)
    except Exception:
        return False, "ID inválido"

    emprestimo_ativo = requests_col.find_one({"book_id": obj_id, "status": "approved"})
    
    if emprestimo_ativo:
        return False, "Ação bloqueada: Existem empréstimos ativos para este livro."

    resultado = books_col.delete_one({"_id": obj_id})
    if resultado.deleted_count == 1:
        return True, "Livro removido com sucesso"
    else:
        return False, "Livro não encontrado"

def list_books(filtro=None):
    consulta = filtro or {}
    documentos = books_col.find(consulta).sort("title", 1)
    lista_retorno = []
    for doc in documentos:
        doc["_id"] = str(doc["_id"])
        lista_retorno.append(doc)
    return lista_retorno

def get_book(id_livro):
    try:
        obj_id = ObjectId(id_livro)
    except Exception:
        return None
    documento = books_col.find_one({"_id": obj_id})
    if not documento:
        return None
    documento["_id"] = str(documento["_id"])
    return documento

def list_requests(status=None):
    consulta = {}
    if status:
        consulta["status"] = status
    documentos = requests_col.find(consulta).sort("created_at", -1)
    lista_retorno = []
    for doc in documentos:
        doc["_id"] = str(doc["_id"])
        if "book_id" in doc:
            doc["book_id"] = str(doc["book_id"])
        lista_retorno.append(doc)
    return lista_retorno

def respond_request(id_solicitacao, approve: bool, id_admin=None, nota=None):
    """
    Parâmetros mantidos: approve (bool).
    Retorna (sucesso: bool, mensagem: str)
    """
    try:
        req_id = ObjectId(id_solicitacao)
    except Exception:
        return False, "ID de solicitação inválido"

    solicitacao = requests_col.find_one({"_id": req_id})
    if not solicitacao:
        return False, "Solicitação não encontrada"

    if solicitacao.get("status") != "pending":
        return False, f"Solicitação já processada ({solicitacao.get('status')})"

    id_obj_livro = solicitacao.get("book_id")
    if not id_obj_livro:
        return False, "Solicitação sem referência de livro"

    if approve:
        livro = books_col.find_one({"_id": id_obj_livro})
        if not livro:
            return False, "Livro não existe"
        
       
        if livro.get("available", 0) <= 0:
            requests_col.update_one({"_id": req_id}, {"$set": {
                "status": "rejected",
                "processed_by": id_admin,
                "processed_at": datetime.utcnow(),
                "note": "Sem exemplares disponíveis" if not nota else nota
            }})
            return False, "Sem exemplares disponíveis"

        
        books_col.update_one({"_id": id_obj_livro}, {"$inc": {"available": -1}, "$set":{"updated_at": datetime.utcnow()}})
        requests_col.update_one({"_id": req_id}, {"$set": {
            "status": "approved",
            "processed_by": id_admin,
            "processed_at": datetime.utcnow(),
            "note": nota or ""
        }})
        return True, "Solicitação aprovada"
    else:
        
        requests_col.update_one({"_id": req_id}, {"$set": {
            "status": "rejected",
            "processed_by": id_admin,
            "processed_at": datetime.utcnow(),
            "note": nota or ""
        }})
        return True, "Solicitação recusada"