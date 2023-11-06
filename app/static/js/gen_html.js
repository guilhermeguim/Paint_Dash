$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Evento para receber o sinal de atualização da tabela
    socket.on('update_table', function(data){
        // Atualize a tabela aqui
        console.log(data.update);
        updateCount();
    });
});


$ (document).ready (function () {
    updateCount();
});

function updateCount () {
    var filterTime = $('#time-dropdown').val();
    $.ajax ({
        // Rota Flask para obter os dados atualizados
        url: '/heatmap?namePage=' + currentPage + '&filterTime=' + filterTime,
        method: 'GET',
        dataType: 'json',
        success: function (response) {
        // Converta o JSON para um objeto JavaScript usando JSON.parse
        const data = JSON.parse (response.data);

        // Acessar o valor de 'max_value'
        const max_value = response.max_value;
        console.log ('max_value:', max_value);

        // Definir a quantidade de níveis na escala (neste caso, 10 níveis)
        const numLevels = 10;

        // Calcular o tamanho de cada intervalo na escala
        const intervalSize = max_value / numLevels;

        // Iterar sobre os objetos no array 'data'
        data.forEach (item => {
            // Acessar cada atributo dentro do objeto 'item'
            const region = item.REGION.replace (',', '');
            const side = item.SIDE;
            const location = item.LOCATION.replace (' ', '_');
            const localType = item.LOCAL_TYPE;
            const active = item.ACTIVE;

            if (max_value == 0){
                console.log ('é igual');
                var scaledValue = 0;
                console.log(scaledValue);
            } else {
                console.log ('n é igual');
                // Calcular o valor na escala de 0 a 10 para o atributo 'active'
                var scaleValue = Math.ceil (active / intervalSize);

                // Limitar o valor da escala para não exceder o número de níveis (10)
                var scaledValue = Math.min (scaleValue, numLevels);
                console.log(scaledValue);
            }

            
            // Faça o que desejar com os atributos, por exemplo, exibir no console
            //console.log(`REGION: ${region}, SIDE: ${side}, LOCATION: ${location}, LOCAL_TYPE: ${localType}, ACTIVE: ${active}`);

            // Criar o nome da variável dinamicamente
            const variableName = `${localType}_${side}_${location}_${region}`;
            //console.log (variableName);

            const badgeValue = document.querySelector (`.${variableName}`);
            badgeValue.textContent = active;

            const colorValue = document.querySelector (`.${variableName}_class`);
            //console.log ('custom-button-' + scaledValue);
            // Remove all classes starting with "custom-button-" from colorValue
            colorValue.classList.forEach(className => {
                if (className.startsWith("custom-button-")) {
                    colorValue.classList.remove(className);
                }
            });
            colorValue.classList.add ('custom-button-' + scaledValue); // Using el.classList.add()
            //colorValue.textContent = scaledValue;
        });


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
        updateCount();
    }
  }
  
  // Executa a função a cada minuto para verificar se está na hora redonda
  setInterval(hourly, 60000);

