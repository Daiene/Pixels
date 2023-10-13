
window.onload = function() {
    let botao = document.getElementById('perfil_nome');
    
    botao.addEventListener('click', () => {
        let escuro = document.getElementById('fundo-escuro');
        let opcoes = document.getElementsByClassName('tela_perfil_nome')[0];
        if (opcoes.style.display === 'none' || opcoes.style.display === '') {
            opcoes.style.display = 'block';
            escuro.style.display = 'block';
        } else {
            opcoes.style.display = 'none';
            escuro.style.display = 'none';
        }
    });
    };
