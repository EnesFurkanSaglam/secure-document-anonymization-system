from flask import Blueprint,request,jsonify
from services import editor_service

editor_bp = Blueprint("editor_bp",__name__)

@editor_bp.route("/list-articles", methods=["GET"])
def list_articles():

    status = request.args.get("status", None)
    if status:
        data, code = editor_service.list_articles_by_status_service(status)
    else:
        data, code = editor_service.list_all_articles_service()
    return jsonify(data), code

@editor_bp.route("/view-logs", methods=["GET"])
def view_logs():
    data, code = editor_service.view_logs_service()
    return jsonify(data), code

@editor_bp.route("/get-article-by-id", methods=["GET"])
def get_article_by_id():
    article_id = request.args.get("article_id", "").strip()
    data, code = editor_service.get_article_by_id_service(article_id)
    return jsonify(data), code

@editor_bp.route("/get-logs-by-article", methods=["GET"])
def get_logs_by_article():
    article_id = request.args.get("article_id", "").strip()
    data, code = editor_service.get_logs_by_article_id_service(article_id)
    return jsonify(data), code

@editor_bp.route("/messages", methods=["GET"])
def list_article_messages():
    
    tracking_code = request.args.get("tracking_code", "").strip()
    data, code = editor_service.list_article_messages_service(tracking_code)
    return jsonify(data), code

@editor_bp.route("/messages", methods=["POST"])
def send_message_as_editor():
    
    body = request.json or {}
    tracking_code = body.get("tracking_code", "").strip()
    content = body.get("content", "").strip()

    data, code = editor_service.send_message_as_editor_service(tracking_code, content)
    return jsonify(data), code


# #!not tested
# @editor_bp.route("/auto-assign-article", methods=["POST"])
# def auto_assign_article():

#     body = request.json or {}
#     tracking_code = body.get("tracking_code", "").strip()

#     data, code = editor_service.auto_assign_article_service(tracking_code)
#     return jsonify(data), code



# @editor_bp.route("/anonymize-article", methods=["POST"])
# def anonymize_article():

#     body = request.json or {}
#     tracking_code = body.get("tracking_code", "").strip()

#     data, code = editor_service.anonymize_article_service(tracking_code)
#     return jsonify(data), code


# @editor_bp.route("/revert-anonymized", methods=["POST"])
# def revert_anonymized():

#     body = request.json or {}
#     tracking_code = body.get("tracking_code", "").strip()

#     data, code = revert_anonymized_sections_service(tracking_code)
#     return jsonify(data), code