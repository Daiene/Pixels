window.onload = function() {
    let botao = document.getElementById('perfil_nome');
    let botao_es = document.getElementById('click_escuro');
    let escuro = document.getElementById('fundo-escuro');
    let opcoes = document.getElementsByClassName('tela_perfil_nome')[0];

    botao.addEventListener('click', () => {
        if (opcoes.style.display === 'none' || opcoes.style.display === '') {
            opcoes.style.display = 'block';
            escuro.style.display = 'block';
        } else {
            opcoes.style.display = 'none';
            escuro.style.display = 'none';
        }
    });

    botao_es.addEventListener('click', () => {
        opcoes.style.display = 'none';
        escuro.style.display = 'none';
    });
};

// mensagem de sucesso!
setTimeout(function() {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'none';
    }
}, 2000);



// consulta de cep

function consultarCep() {
    // Obtém o valor atual do campo CEP
    const cep = $('#cep').val();

    // Realiza a consulta na API de CEP
    $.ajax({
        type: 'GET',
        url: `https://viacep.com.br/ws/${cep}/json/`,
        success: function(data) {
            if (!data.erro) {
                // Se não houver erro na consulta, preenche os campos de logradouro e estado
                $('#cidade').val(data.localidade);
                $('#logradouro').val(data.logradouro);
                $('#estado').val(data.uf);
            } else {
                // Se houver erro, limpa os campos de logradouro e estado
                $('#cidade').val('')
                $('#logradouro').val('');
                $('#estado').val('');
                alert('CEP não encontrado');
            }
        },
        error: function(error) {
            console.error(error);
            console.log('Erro na consulta do CEP');
            //alert('Erro na consulta do CEP');
        }
    });
}