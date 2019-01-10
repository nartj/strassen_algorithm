from flask import Flask, render_template, request
from static.services.computationservice import *
from static.services.decoder import *

app = Flask(__name__)


@app.route("/strassen")
def get_front():
    return render_template("index.html")


@app.route("/compute", methods=["POST"])
def compute():
    service = ComputationService(
            np.asarray(json.loads(json.loads(request.get_data())['matrix_a'], object_hook=json_numpy_obj_hook)),
            np.asarray(json.loads(json.loads(request.get_data())['matrix_b'], object_hook=json_numpy_obj_hook))
    )
    response, strassen_comp_time, strassen_mult_cnt, classical_comp_time, classical_mult_cnt = service.get_result()
    # Appending all infos to response matrix to facilitate Javascript interpretation
    response = np.append(response, strassen_comp_time * 1000)
    response = np.append(response, strassen_mult_cnt)
    response = np.append(response, classical_comp_time * 1000)
    response = np.append(response, classical_mult_cnt)
    return json.dumps(response.tolist())


if __name__ == '__main__':
    app.run(debug=True)
