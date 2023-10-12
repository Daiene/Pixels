
window.onload = function() {
    let botao = document.getElementById('perfil_nome');
    
    botao.addEventListener('click', () => {
        let opcoes = document.getElementsByClassName('tela_perfil_nome')[0];
        if (opcoes.style.display === 'none' || opcoes.style.display === '') {
            opcoes.style.display = 'block';
        } else {
            opcoes.style.display = 'none';
        }
    });
    };
