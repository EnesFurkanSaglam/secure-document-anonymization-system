from flask import Blueprint,request,jsonify
from services import author_service

author_bp = Blueprint("author_bp",__name__)


@author_bp.route("/upload-article", methods=["POST"])
def upload_article():
    email = request.form.get("email","").strip()
    pdf_file = request.files.get("pdf",None)
    data,status = author_service.upload_article_service(email,pdf_file)
    return jsonify(data), status

@author_bp.route("/check-status",methods=["GET"])
def check_status():
    tracking_code = request.args.get("tracking_code","").strip()
    email = request.args.get("email","").strip()
    
    data,status = author_service.check_status_service(email,tracking_code)    
    return jsonify(data),status

@author_bp.route("/reupload-article", methods=["POST"])
def reupload_article():
    email = request.form.get("email", "").strip()
    tracking_code = request.form.get("tracking_code", "").strip()
    pdf_file = request.files.get("pdf", None)

    data, status = author_service.reupload_article_service(email, tracking_code, pdf_file)
    return jsonify(data), status


#! not tested
@author_bp.route("/send-message",methods=["POST"])
def send_message():
    body = request.json or {}
    email = body.get("email","").strip()
    tracking_code = body.get("tracking_code","").strip()
    content = body.get("content","").strip()
    
    data,status = author_service.send_message_service(email,tracking_code,content)
    return jsonify(data),status


