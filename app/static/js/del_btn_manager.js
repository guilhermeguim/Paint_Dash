$(document).ready(function () {
    var currentID;
    // Capturar evento de clique nos botões
    $('table').on('click', '.delete-button', function () {
      currentID = $(this).data('id');
      $('#deleteModal').modal('show');
    });
  
    // Capturar evento de clique no botão de confirmação do modal
    $('#confirmDeleteBtn').click(function () {

          // Enviar os dados do botão + popup para o servidor
          $.ajax({
            url: '/delete_data',
            type: 'POST',
            data: {
              id: currentID,
            },
            success: function (response) {
              // Executar ações após o registro ser enviado com sucesso
              console.log('delete Registered on DB');
              $('#deleteModal').modal('hide');
            },
            error: function (xhr) {
              // Executar ações em caso de erro
              console.error('Error: delete not Registered on DB', xhr.responseText);
              $('#deleteModal').modal('hide');
            }
          });


    });
  });