from flask import Blueprint,request,jsonify
from services import reviewer_service

reviewer_bp = Blueprint("reviewer_bp",__name__)

@reviewer_bp.route("/assigned-articles", methods=["GET"])
def list_assigned_articles():
    email = request.args.get("email", "").strip()
    data, status = reviewer_service.list_assigned_articles_service(email)
    return jsonify(data), status

@reviewer_bp.route("/submit-review", methods=["POST"])
def submit_review():
    body = request.json or {}
    email = body.get("email", "").strip()
    tracking_code = body.get("tracking_code", "").strip()
    review_text = body.get("review_text", "").strip()
    is_final = body.get("is_final", False)

    data, status = reviewer_service.submit_review_service(email, tracking_code, review_text, is_final)
    return jsonify(data), status

@reviewer_bp.route("/all-reviewers", methods=["GET"])
def list_all_reviewers():
    data, status = reviewer_service.list_all_reviewers_service()
    return jsonify(data), status

@reviewer_bp.route("/publish-article", methods=["POST"])
def route_publish_article():
    data = request.json or {}
    if "article_id" not in data:
        return jsonify({"error": "article_id is required"}), 400
    
    article_id = data["article_id"]
    
    result, status_code = reviewer_service.publish_article_service(article_id=article_id,)
    return jsonify(result), status_code