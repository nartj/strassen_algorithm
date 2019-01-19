let matrix_a = [];
let matrix_b = [];
let matrix_c = [];
let strassen_computation_time = -1;
let strassen_multiplication_counter = -1;
let classical_computation_time = -1;
let classical_multiplication_counter = -1;
let matrix_size = 2;

let god_mode = false;

/*      CONTROL PANEL

Generate and interact with a control panel to change matrices size

*/

let FizzyText = function() {
    this.matrix_size = matrix_size
};

$(document).ready(function(){
    $(function(){
        $('#container').css({ "min-height": $(window).innerHeight() });
        $(window).resize(function(){
            $('#container').css({ "min-height": $(window).innerHeight() });
        });
        $('#statistics').css({ "display": "none" });
    });

    initMatrix(matrix_size);
    let fizzyText = new FizzyText();
    let gui = new dat.GUI();
    let matrixSizeController = gui.add(fizzyText,
        'matrix_size', matrix_size).min(2).max(32).step(1).name('Matrix size').listen();
    gui.open();

    matrixSizeController.onChange(function(size) {
        clearMatrix(size);
        $('#statistics').css({ "display": "none" });
        document.getElementById("hidden").hidden = true;
        matrix_size = size;
        initMatrix(size);
    });

});

/*      DYNAMIC HTML TEMPLATE

Generate and interact with matrices HTML template and DOM values
Handle matrices inputs generically thanks to their attributes

 */

function setMatrixHtmlTemplate(size) {
  $(".matrix-table-container").each(function() {
      let name = this.getAttribute('data-for');
      let table = '<table class="matrix-table"><tbody>';
      for (let i = 0; i < parseInt(size); i++) {
          table += '<tr data-for="' + name+'" data-row="' + i + '">';
          for (let j = 0; j < parseInt(size); j++) {
              let cell_coord = name+'-'+i+'-'+j;
              table += '<td class="matrix-table-cell"><span>'
                  + '<input id="' + cell_coord
                  + '" name="' + cell_coord
                  + '" oninput="handleInput(this)" type="number" class="matrix-table-input" data-for="' + name
                  + '" data-row="' + i +'" data-column="' + j +'"';
          if(name === 'C')
            table += " disabled";
          table += "></span></td>";
        }
        table += '</tr>';
      }
      table += '</tbody></table>';
      this.innerHTML = table;
  });
}

function setCell(matrixName, i, j, value, model_only=false) {
    switch (matrixName) {
        case 'A':
            matrix_a[i][j] = parseInt(value);
            if (!model_only) $('#A-' + i + '-' + j).val(parseInt(value));
            break;
        case 'B':
            matrix_b[i][j] = parseInt(value);
            if (!model_only) $('#B-' + i + '-' + j).val(parseInt(value));
            break;
        case 'C':
            matrix_c[i][j] = parseInt(value);
            if (!model_only) $('#C-' + i + '-' + j).val(parseInt(value));
            break;
    }
}

function handleInput(element) {
    setCell(
        element.getAttribute('data-for'),
        element.getAttribute('data-row'),
        element.getAttribute('data-column'),
        element.value);
    console.log(matrix_a);
}

/*      MATRICES JS MODEL

Define matrices values Javascript model (array of array) to store inputs data
or randomly generated data

 */

function initMatrix(size) {
    setMatrixHtmlTemplate(size);
    resetMatrixData(size);
}

function clearMatrix(size) {
    for (let i = 0; i < size; i++) {
        matrix_a = [];
        matrix_b = [];
        matrix_c = [];
        for (let j = 0; j < size; j++) {
            matrix_a[i] = [];
            matrix_b[i] = [];
            matrix_c[i] = [];
        }
    }
}

function generateRandomMatrix(size) {
    clearMatrix(size);
    resetMatrixData(size);
    generateRandomMatrixModel(size, true);
    $('#statistics').css({ "display": "none" });
    document.getElementById("hidden").hidden = true;
}

function resetMatrixData(size) {
    generateRandomMatrixModel(size);
}

function generateRandomMatrixModel(size, model_only=false) {
    let min = -10;
    let max = 10;

    for(let i = 0; i < size; i++) {
        matrix_a[i] = [];
        matrix_b[i] = [];
        for (let j = 0; j < size; j++) {
            setCell('A', i, j, Math.floor(Math.random() * (max - min + 1)) + min, model_only);
            setCell('B', i, j, Math.floor(Math.random() * (max - min + 1)) + min, model_only);
        }
    }

    if (model_only) {
        requestStrassenComputation([matrix_a, matrix_b]);
        setMatrixHtmlTemplate(value);
    }
}

/*      BUTTON CLICK HANDLING

Handle click on the different button
- clear
- random
- calculate
- god mode
- launch
using jQuery selectors.

 */


$('#btn-clear').click(function() {
    $('#statistics').css({ "display": "none" });
    document.getElementById("hidden").hidden = true;
    clearMatrix(matrix_size);
});

$('#btn-random').click(function() {
    $('#statistics').css({ "display": "none" });
    document.getElementById("hidden").hidden = true;

    let min = -10;
    let max = 10;

    for(let i = 0; i < matrix_size; i++) {
        matrix_a[i] = [];
        matrix_b[i] = [];

        for(let j = 0; j < matrix_size; j++) {
            setCell('A', i, j,Math.floor(Math.random() * (max - min + 1)) + min);
            setCell('B', i, j,Math.floor(Math.random() * (max - min + 1)) + min);
        }
    }
});

$('#btn-calc').click(function() {
    requestStrassenComputation([matrix_a, matrix_b]);
});


/*          GOD MODE

Allow the user to generate random big size matrices.
God Mode basically disable matrices inputs displays to fasten
the random generation.
God Mode is a switch button which once activated,
displays a input to set the wanted size and
a launch button to automatically generate matrices
and send the request to the python back-end

 */
$('#btn-god-mode').click(function() {
    god_mode = !god_mode;

    document.getElementById("container").hidden = god_mode;
    document.getElementsByClassName("matrix-container").hidden = god_mode;
    document.getElementById("btn-random").hidden = god_mode;
    document.getElementById("btn-calc").hidden = god_mode;
    document.getElementById("btn-clear").hidden = god_mode;

    document.getElementById("god-mode-form").hidden = !god_mode;
    document.getElementById("btn-launch").hidden = !god_mode;
});

$('#btn-launch').click(function() {
    if (god_mode) {
        launchGodMode();
    }
});

function launchGodMode() {
    var element = document.getElementById("god-mode-size");
    let value = element.value;
    generateRandomMatrix(value);
}

/*          API REQUESTS AND GRAPHICS PLOT

Send the computation request to python back-end using REST endpoints
Pull the statistics data using another endpoint and draw graphics using Plotly
Display graphics and scroll down to the page

 */

function requestStrassenComputation(input) {
    // request to python back end
    $.ajax({
        type: "POST",
        url: "/compute",
        contentType: "text/json",
        data: JSON.stringify({"matrix_a": JSON.stringify(input[0]), "matrix_b": JSON.stringify(input[1])}),
        success: function(response) {
            handleComputationResponse(response);
        }
    });
}

function handleComputationResponse(response) {
    response = JSON.parse(response);
    for(let i = 0; i < Math.sqrt(response.length - 4); i++) {
        matrix_c[i] = [];
        for(let j = 0; j < Math.sqrt(response.length - 4); j++) {
            setCell('C', i, j, parseInt(response[Math.sqrt(response.length - 4) * i + j]));
        }
    }
    displayDataAndGraphics(response);
}

function displayDataAndGraphics(response) {
    strassen_computation_time = response[response.length - 4];
    strassen_multiplication_counter = response[response.length - 3];
    classical_computation_time = response[response.length - 2];
    classical_multiplication_counter = response[response.length - 1];

    $(document).ready(function(){
        let strassen_compute_time_element = document.getElementById("strassen-computation-time");
        strassen_compute_time_element.innerText = strassen_computation_time === 0 ?
            "< 0.1 ms." : strassen_computation_time +  " ms.";
        let strassen_multiplication_counter_element = document.getElementById("strassen-multiplication-counter");
        strassen_multiplication_counter_element.innerText = strassen_multiplication_counter + " multiplications.";

        let classical_compute_time_element = document.getElementById("classical-computation-time");
        classical_compute_time_element.innerText = classical_computation_time === 0 ?
            "< 0.1 ms." : classical_computation_time +  " ms.";
        let classical_multiplication_counter_element = document.getElementById("classical-multiplication-counter");
        classical_multiplication_counter_element.innerText = classical_multiplication_counter + " multiplications.";

        plotGraphics();
        $('#statistics').css({ "display": "initial" });
        document.getElementById("hidden").hidden = false;
    });
}

function plotGraphics() {
    let matrix_sizes = [],
        strassen_multip_nb = [],
        strassen_comput_time = [],
        classical_multip_nb = [],
        classical_comput_time = [];

    $.ajax({
        url: "/list-strassen-stats",
        success: function(response) {
            console.log("plot strassen:", response);
            let rows = JSON.parse(response);
            console.log("plot strassen:", response);
            for (let i = 0; i < rows.length; i++) {
                matrix_sizes.push(rows[i][0]);
                strassen_comput_time.push(rows[i][1]);
                strassen_multip_nb.push(rows[i][2]);
            }
            thenRequestClassicalStats();
        }
    });

    function thenRequestClassicalStats() {
        $.ajax({
            url: "/list-classical-stats",
            success: function(response) {
                console.log("plot classical:", response);
                let rows = JSON.parse(response);
                console.log("plot classical:", response);
                for (let i = 0; i < rows.length; i++){
                    classical_comput_time.push(rows[i][1]);
                    classical_multip_nb.push(rows[i][2]);
                }
                thenPlot();
            }
        });
    }


    function thenPlot() {
        matrix_sizes = matrix_sizes.sort(function(a,b) { return a - b; });

        let strassen_mult_axes = {
            x: matrix_sizes, // matrix sizes
            y: strassen_multip_nb, // nb mult done
            name: 'Strassen'
        };

        let strassen_time_axes = {
            x: matrix_sizes, // matrix sizes
            y: strassen_comput_time, // comp time
            name: 'Strassen'
        };

        let classical_mult_axes = {
            x: matrix_sizes, // matrix sizes
            y: classical_multip_nb, // nb mult done
            name: 'Classical'
        };

        let classical_time_axes = {
            x: matrix_sizes, // matrix sizes
            y: classical_comput_time, // comp time
            name: 'Classical'
        };

        let data = [strassen_mult_axes, classical_mult_axes];

        var nb_mult_title = {
            title: 'Numbers of multiplications',
            showlegend: false
        };

        var comp_time_title = {
            title: 'Computation time',
            showlegend: false
        };

        Plotly.newPlot('nb-mult-plot', data, nb_mult_title);
        data = [strassen_time_axes, classical_time_axes];
        Plotly.newPlot('time-plot', data, comp_time_title);
        scrollToStatistics();
    }

    function scrollToStatistics() {
        $('html, body').animate({
            scrollTop: $("#statistics").offset().top
        }, 1000);
        $(function(){
            $('#statistics').css({ height: $(window).innerHeight() });
            $(window).resize(function(){
                $('#statistics').css({ height: $(window).innerHeight() });
            });
        });
    }

}
//https://gist.github.com/aybabtme/7567536