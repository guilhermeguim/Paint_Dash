$(document).ready(function () {
  var currentType, currentLocation, currentRegion, currentSide;

  // Capturar evento de clique nos botões
  $('.failure-button').click(function () {
    currentType = $(this).data('type');
    currentSide = $(this).data('side');
    currentLocation = $(this).data('location');
    currentRegion = $(this).data('region');
    $('#failureModal').modal('show');
  });

  // Capturar evento de clique no botão de confirmação do modal
  $('#confirmFailureBtn').click(function () {
    var vinCode = $('#vinCode').val();

        // Enviar os dados do botão + popup para o servidor
        $.ajax({
          url: '/input_data',
          type: 'POST',
          data: {
            type: currentType,
            side: currentSide,
            location: currentLocation,
            region: currentRegion,
            vinCode: vinCode
          },
          success: function (response) {
            // Executar ações após o registro ser enviado com sucesso
            console.log('Failure Registered on DB');
            $('#failureModal').modal('hide');
          },
          error: function (xhr) {
            // Executar ações em caso de erro
            console.error('Error: Failure not Registered on DB', xhr.responseText);
            $('#failureModal').modal('hide');
          }
        });

  });
});