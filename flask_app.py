from app.app import app, init_app

if __name__ == "__main__":
    init_app()
    app.run(debug=True)