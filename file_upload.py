from flask import Flask, request

flask_app = Flask(__name__)

@flask_app.route("/" , methods=['GET', 'POST'])
def uploader():
    if request.method=='POST':
        f = request.files['file1']
        print(f)
        return "Uploaded successfully!"
    else:
        raise

if __name__ == '__main__':
    flask_app.run(debug=True)