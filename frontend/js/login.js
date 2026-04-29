import { mostrarAlerta } from './utils.js';

const loginForm = document.getElementById('login-form');

if (loginForm) {
    loginForm.addEventListener('submit', event => {
        event.preventDefault();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!email || !password) {
            mostrarAlerta('Por favor, informe e-mail e senha.', 'warning');
            return;
        }

        // Simulação de login para a versão inicial do frontend.
        window.location.href = 'index.html';
    });
}
