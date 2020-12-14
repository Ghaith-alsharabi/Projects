from sport import create_app
if __name__ == '__main__':
    app = create_app()

#    app.secret_key = '4ddf8a374af1d4c912235859fb715b27'
    # app.run(host='0.0.0.0')
    # Voor lokale testpip
    app.run(debug=True)

