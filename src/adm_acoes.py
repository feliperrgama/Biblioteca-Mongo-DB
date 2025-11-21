# src/adm_actions.py
from bson.objectid import ObjectId
from datetime import datetime
from src.mongo_db import books_col, requests_col

def add_book(book_data):
    """
    book_data: dict com keys:
      - title (str), author (str), isbn (str), year (int), copies (int), description (str optional)
    Retorna inserted_id
    """
    doc = {
        "title": book_data.get("title"),
        "author": book_data.get("author"),
        "isbn": book_data.get("isbn"),
        "year": int(book_data.get("year")) if book_data.get("year") else None,
        "copies": int(book_data.get("copies", 1)),
        "available": int(book_data.get("copies", 1)),
        "description": book_data.get("description", ""),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    res = books_col.insert_one(doc)
    return str(res.inserted_id)

def remove_book(book_id):
    """
    Remove um livro pelo _id (string). Retorna True se removeu.
    Só remove se não houver empréstimos ativos — essa verificação pode ser adaptada:
    """
    try:
        oid = ObjectId(book_id)
    except Exception:
        return False, "ID inválido"

    # Exemplo simples: apenas remove
    res = books_col.delete_one({"_id": oid})
    if res.deleted_count == 1:
        return True, "Livro removido"
    else:
        return False, "Livro não encontrado"

def list_books(filter_query=None):
    q = filter_query or {}
    docs = books_col.find(q).sort("title", 1)
    ret = []
    for d in docs:
        d["_id"] = str(d["_id"])
        ret.append(d)
    return ret

def get_book(book_id):
    try:
        oid = ObjectId(book_id)
    except Exception:
        return None
    d = books_col.find_one({"_id": oid})
    if not d:
        return None
    d["_id"] = str(d["_id"])
    return d

def list_requests(status=None):
    q = {}
    if status:
        q["status"] = status  # "pending", "approved", "rejected"
    docs = requests_col.find(q).sort("created_at", -1)
    ret = []
    for d in docs:
        d["_id"] = str(d["_id"])
        d["book_id"] = str(d["book_id"])
        ret.append(d)
    return ret

def respond_request(request_id, approve: bool, admin_id=None, note=None):
    """
    Aprovar ou recusar uma solicitação.
    - request_id: str
    - approve: True -> aprovar, False -> recusar
    - admin_id: opcional, id do admin que responde
    - note: opcional
    Retorna (ok:bool, message:str)
    """
    try:
        rid = ObjectId(request_id)
    except Exception:
        return False, "ID de solicitação inválido"

    req = requests_col.find_one({"_id": rid})
    if not req:
        return False, "Solicitação não encontrada"

    if req.get("status") != "pending":
        return False, f"Solicitação já processada ({req.get('status')})"

    book_oid = req.get("book_id")
    if not book_oid:
        return False, "Solicitação sem referência de livro"

    if approve:
        # Verifica disponibilidade
        book = books_col.find_one({"_id": book_oid})
        if not book:
            return False, "Livro não existe"
        if book.get("available", 0) <= 0:
            # não há exemplares disponíveis
            # opcional: marcar como rejeitado
            requests_col.update_one({"_id": rid}, {"$set": {
                "status": "rejected",
                "processed_by": admin_id,
                "processed_at": datetime.utcnow(),
                "note": "Sem exemplares disponíveis" if not note else note
            }})
            return False, "Sem exemplares disponíveis"

        # decrementa disponível, marca solicitação aprovada
        books_col.update_one({"_id": book_oid}, {"$inc": {"available": -1}, "$set":{"updated_at": datetime.utcnow()}})
        requests_col.update_one({"_id": rid}, {"$set": {
            "status": "approved",
            "processed_by": admin_id,
            "processed_at": datetime.utcnow(),
            "note": note or ""
        }})
        return True, "Solicitação aprovada"
    else:
        # recusar
        requests_col.update_one({"_id": rid}, {"$set": {
            "status": "rejected",
            "processed_by": admin_id,
            "processed_at": datetime.utcnow(),
            "note": note or ""
        }})
        return True, "Solicitação recusada"
