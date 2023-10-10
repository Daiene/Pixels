const botao = document.getElementById('perfil_nome');
const opcoes = document.getElementsByClassName('tela_perfil_nome');

botao.addEventListener('click', (e) => {
    e.preventDefault(); // Evita que o link siga para "#" (URL vazia)

    if (opcoes.style.display === 'none' || opcoes.style.display === '') {
        opcoes.style.display = 'block';
    } else {
        opcoes.style.display = 'none';
    }
});