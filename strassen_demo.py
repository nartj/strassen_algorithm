from flask import Flask, render_template, request
from static.services.strassen import *
from static.services.decoder import *

app = Flask(__name__)


@app.route("/strassen")
def get_front():
    return render_template("index.html")


@app.route("/compute", methods=["POST"])
def compute():
    service = Strassen(
            np.asarray(json.loads(json.loads(request.get_data())['matrix_a'], object_hook=json_numpy_obj_hook)),
            np.asarray(json.loads(json.loads(request.get_data())['matrix_b'], object_hook=json_numpy_obj_hook))
    )
    response, computation_time, multiplication_counter = service.get_result()
    response = np.append(response, computation_time * 1000)
    return json.dumps(np.append(response, multiplication_counter).tolist())


if __name__ == '__main__':
    app.run(debug=True)
