from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog_database.db"

db = SQLAlchemy()
db.init_app(app)

class Blog(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(500), nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(JSON, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "createdAt": self.createdAt.isoformat() if self.createdAt else None,
            "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None
        }
    

with app.app_context():
    db.create_all()


# Create Routes

@app.route("/posts", methods=["POST"])
def post():
    data = request.get_json()
    
    new_blog = Blog(title=data["title"], content=data["content"], category=data["category"], tags=data["tags"])
    
    db.session.add(new_blog)
    db.session.commit()
    
    return jsonify(new_blog.to_dict()), 201
    
    
@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_blog_post(post_id):
    required_fields = ["title", "content", "category", "tags"]
    
    data = request.get_json()
    
    current_blog = Blog.query.get(post_id)
    
    if not current_blog:
        
        return jsonify({"error": "Invalid or missing JSON"}), 400
    
    missing_fields = []
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400
        
    current_blog.title = data["title"]
    current_blog.content = data["content"]
    current_blog.category = data["category"]
    current_blog.tags = data["tags"]
    
    db.session.commit()
    
    return jsonify(current_blog.to_dict()), 200


@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_blog_post(post_id):
    blog = Blog.query.get(post_id)
    
    if blog:
        db.session.delete(blog)
        db.session.commit()
        
        return jsonify({"message": "OK"}), 200
    else:
        return jsonify({"error": "Not Found"}), 404


@app.route("/posts/<int:post_id>", methods=["GET"])
def get_blog_post(post_id):
    blog = Blog.query.get(post_id)
    
    if blog:
        return jsonify(blog.to_dict()), 200
    else: 
        return jsonify({"error": "Not Found"}), 404


@app.route("/posts", methods=["GET"])
def get_all_posts():
    blogs = Blog.query.all()

    return jsonify([blog.to_dict() for blog in blogs]), 200    

@app.route("/posts", methods=["GET"])
def get_by_tag():
    tag = request.args.get("tag")
    
    blogs = Blog.query.all()
    
    if "tag" in tag:
        return jsonify([blog.to_dict() for blog in blogs if tag in blog.tags]), 200
    else: 
        return jsonify({"error": "Wrong tag"}), 400



if __name__ == "__main__":
    app.run(debug=True)