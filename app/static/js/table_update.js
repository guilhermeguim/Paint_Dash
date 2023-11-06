$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Evento para receber o sinal de atualização da tabela
    socket.on('update_table', function(data){
        // Atualize a tabela aqui
        console.log(data.update);
        updateTable();
    });
});

function updateTable() {

    var filterType = $('#type-dropdown').val();
    var filterSide = $('#side-dropdown').val();
    var filterLocation = $('#location-dropdown').val();
    var filterRegion = $('#region-dropdown').val();
    var filterDate = $('#date-dropdown').val(); 

    $.ajax({
          // Rota Flask para obter os dados atualizados
        url: '/update_data?filterType=' + filterType + '&filterLocation=' + filterLocation + '&filterSide=' + filterSide + '&filterRegion=' + filterRegion + '&filterDate=' + filterDate,
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            var tableBody = $('#table-body');
            tableBody.empty();  // Limpa o conteúdo atual da tabela

            // Preenche a tabela com os novos dados
            response.data.forEach(function(row) {
                var newRow = $('<tr class="table-dark"></tr>');
                newRow.append('<td class="table-dark text-center">' + row[0] + '</td>');
                newRow.append('<td class="table-dark text-center">' + row[1] + '</td>');
                newRow.append('<td class="table-dark text-center">' + row[2] + '</td>');
                newRow.append('<td class="table-dark text-center">' + row[3] + '</td>');
                newRow.append('<td class="table-dark text-center">' + row[4] + '</td>');
                newRow.append('<td class="table-dark text-center">' + row[5] + '</td>');
                newRow.append('<td class="table-dark text-center">' + row[6] + '</td>');
                newRow.append('<td class="table-dark text-center"><button type="button" class="btn btn-danger delete-button" data-id="'+row[0]+'">X</button></td>');
                tableBody.append(newRow);
            });
        },
        error: function(error) {
            console.log('AJAX request error: ' + error);
        }
    });
}


// Chama a função de atualizar a tabela quando a página carregar
$(document).ready(function() {
    updateTable();
});

// Função para atualizar a tabela quando o botão for clicado
function go_btn() {
    updateTable();
}

