from app import create_app

config = None
factota = create_app(config)

if __name__ == '__main__':
    factota.run(host='0.0.0.0', port='8080', use_reloader=True, debug=True)
