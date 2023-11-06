$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Evento para receber o sinal de atualização da tabela
    socket.on('update_table', function(data){
        // Atualize a tabela aqui
        updateGraph();
    });
});

$ (document).ready (function () {
    updateGraph();
    
});

$ (document).ready (function () {
    // Chamar a função de redimensionamento quando a janela for redimensionada
    window.addEventListener('resize', function() {
        updateGraph();
    });
});

function updateGraph () {

    var screen_size = 0;

    if (window.innerWidth >= 1500){
        screen_size = 3;
    } else if (window.innerWidth >= 1280) {
        screen_size = 4;
    } else if (window.innerWidth >= 1025) {
    screen_size = 1;
    } else {
    screen_size = 2;
    }


    $.ajax ({
        // Rota Flask para obter os dados atualizados
        url: '/update_dash?screenSize=' + screen_size,
        method: 'GET',
        dataType: 'json',
        success: function (response) {

        const total_events = response.total_events_today;
        const total1 = response.shift1;
        const total2 = response.shift2;
        const total3 = response.shift3;

        const graph1Json = response.graph_json1;
        const graph2Json = response.graph_json2;
        const graph3Json = response.graph_json3;
        const graph4Json = response.graph_json4;
        const graph5Json = response.graph_json5;
        const graph6Json = response.graph_json6;
        const graph7Json = response.graph_json7;
        const graph8Json = response.graph_json8;
        const graph9Json = response.graph_json9;


        // Parse the JSON back to a plotly figure
        const graph1 = JSON.parse(graph1Json);
        const graph2 = JSON.parse(graph2Json);
        const graph3 = JSON.parse(graph3Json);
        const graph4 = JSON.parse(graph4Json);
        const graph5 = JSON.parse(graph5Json);
        const graph6 = JSON.parse(graph6Json);
        const graph7 = JSON.parse(graph7Json);
        const graph8 = JSON.parse(graph8Json);
        const graph9 = JSON.parse(graph9Json);
        // // Parse the JSON back to a plotly figure


        console.log(total_events);
        document.getElementById('total-events').innerHTML = total_events;
        document.getElementById('total-1').innerHTML = '1st Shift: ' + total1;
        document.getElementById('total-2').innerHTML = '2nd Shift: ' + total2;
        document.getElementById('total-3').innerHTML = '3rd Shift: ' + total3;

        // Update the graph in the <p> tag
        Plotly.react('graph1', graph1); // Use 'Plotly.react' to update the existing graph
        Plotly.react('graph2', graph2);
        Plotly.react('graph3', graph3);
        Plotly.react('graph4', graph4);
        Plotly.react('graph5', graph5);
        Plotly.react('graph6', graph6);
        Plotly.react('graph7', graph7);
        Plotly.react('graph8', graph8);
        Plotly.react('graph9', graph9);

        },

        error: function (error) {
        console.log ('AJAX request error: ' + error);
        },
    });
}

function hourly() {
    const now = new Date();
    const minutes = now.getMinutes();

  
    // Verifica se está na hora redonda (minutos e segundos iguais a zero)
    if (minutes === 0) {
        updateGraph();
    }
  }
  
  // Executa a função a cada segundo para verificar se está na hora redonda
  setInterval(hourly, 60000);