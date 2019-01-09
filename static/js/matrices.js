let matrix_size = 2;
let matrix_a = [];
let matrix_b = [];
let matrix_c = [];
let strassen_computation_time = -1;
let strassen_multiplication_counter = -1;

let FizzyText = function() {
  this.matrix_size = matrix_size
};

$(document).ready(function(){
    initMatrix(matrix_size);
    let fizzyText = new FizzyText();
    let gui = new dat.GUI();
    let matrixSizeController = gui.add(fizzyText,
        'matrix_size', matrix_size).min(2).max(64).step(1).name('Matrix size').listen();
    gui.open();

    matrixSizeController.onChange(function(value) {
        matrix_size = value;
        initMatrix(value);
    });

});

function handleInput(element) {
    setCell(
        element.getAttribute('data-for'),
        element.getAttribute('data-row'),
        element.getAttribute('data-column'),
        element.value);
    console.log(matrix_a);
}

function initMatrix(value) {
    setMatrixHtmlTemplate(value);
    resetMatrixData(value);
}

function setMatrixHtmlTemplate(value) {
  $(".matrix-table-container").each(function() {
      let name = this.getAttribute('data-for');
      let table = '<table class="matrix-table"><tbody>';
      for (let i = 0; i < parseInt(value); i++) {
          table += '<tr data-for="' + name+'" data-row="' + i + '">';
          for (let j = 0; j < parseInt(value); j++) {
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

$('#btn-clear').click(function() {
  resetMatrixData(matrix_size);
});

function resetMatrixData(value) {
  matrix_a = [];
  matrix_b = [];
  matrix_c = [];

  for(let i=0; i < value; i++) {
      matrix_a[i] = [];
      matrix_b[i] = [];
      matrix_c[i] = [];

      for(let j = 0; j < value; j++) {
          setCell('A', i, j, undefined);
          setCell('B', i, j, undefined);
          setCell('C', i, j,undefined);
      }
  }
}

$('#btn-random').click(function() {
  let min = -10;
  let max = 10;

  for(let i = 0; i < matrix_size; i++) {
      matrix_a[i] = [];
      matrix_b[i] = [];

      for(let j = 0; j < matrix_size; j++) {
        setCell('A', i, j,Math.floor(Math.random() * (max - min +1)) + min);
        setCell('B', i, j,Math.floor(Math.random() * (max - min +1)) + min);
      }
  }
});

function setCell(matrixName, i, j, value) {
  if(matrixName === 'A') {
    matrix_a[i][j] = parseInt(value);
    $('#A-' + i + '-' + j).val(parseInt(value));
  }
  else if (matrixName === 'B') {
    matrix_b[i][j] = parseInt(value);
    $('#B-' + i + '-' + j).val(parseInt(value));
  }
  else if (matrixName === 'C') {
    matrix_c[i][j] = parseInt(value);
    $('#C-' + i + '-' + j).val(parseInt(value));
  }
}

$('#btn-calc').click(function() {
    console.log('sent:', [matrix_a, matrix_b]);
    requestStrassenComputation([matrix_a, matrix_b])
    $('html, body').animate({
        scrollTop: $("#statistics").offset().top
    }, 1000);
    $(function(){
        $('#statistics').css({ height: $(window).innerHeight() });
        $(window).resize(function(){
            $('#statistics').css({ height: $(window).innerHeight() });
        });
    });
});

function requestStrassenComputation(input) {
    $.ajax({
        type: "POST",
        url: "/compute",
        data: JSON.stringify({"matrix_a": JSON.stringify(input[0]), "matrix_b": JSON.stringify(input[1])}),
        success: function(response) {
            response = JSON.parse(response);
            console.log("response:", response);
            console.log("response length:", response.length);
            for(let i = 0; i < Math.sqrt(response.length - 2); i++) {
                matrix_c[i] = [];
                for(let j = 0; j < Math.sqrt(response.length - 2); j++) {
                    setCell('C', i, j, parseInt(response[Math.sqrt(response.length - 2) * i + j]));
                }
            }
            strassen_computation_time = response[response.length - 2];
            strassen_multiplication_counter = response[response.length - 1];
            console.log('computation time:', strassen_computation_time,
                        'multiplication counter:', strassen_multiplication_counter);

            $(document).ready(function(){
                let compute_time_element = document.getElementById("strassen-computation-time");
                compute_time_element.innerText = response[response.length - 2] === 0 ?
                    "< 0 ms." : response[response.length - 2] +  " ms.";
                let multiplication_counter_element = document.getElementById("strassen-multiplication-counter");
                multiplication_counter_element.innerText = response[response.length - 1] + " multiplications."
                document.getElementById("hidden").hidden = false;
            });
        }
    });


}

//https://gist.github.com/aybabtme/7567536