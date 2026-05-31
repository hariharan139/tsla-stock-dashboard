from flask import Flask
from routes.stock_routes import stock_bp
from db.database import init_db

app = Flask(__name__)

init_db()

app.register_blueprint(
    stock_bp
)

if __name__ == "__main__":
    app.run(
        debug=True
    )