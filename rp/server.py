from flask import Flask, render_template
app = Flask(__name__,template_folder='www',static_folder='www/images')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  print ('I got clicked!')

  return 'Click.'

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
  print(deviceName + '--->' + action)
  #return render_template('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=5000)
#app.run(debug=True)
