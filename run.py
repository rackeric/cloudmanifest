from manifest import create_app
#from manifest import app

app = create_app()
app.run(host='0.0.0.0', port=5000, debug=True)
