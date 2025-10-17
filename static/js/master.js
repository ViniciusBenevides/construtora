try {

    function mostrarFormulario() {
        var formulario = document.getElementById("formularioLogin");
        var btnGoogle = document.getElementById("googleLog");
        var btnFace = document.getElementById("faceLog");
        var btnMail = document.getElementById("mailLog");
        var cadastra = document.querySelector(".cadastra");
        var esqueci = document.querySelector(".esqueci");

        esqueci.style.display = "flex";
        formulario.style.display = "block";
        btnGoogle.style.display = "none";
        btnFace.style.display = "none";
        btnMail.style.display = "none";
        cadastra.classList.add("d-none");
        cadastra.classList.remove("d-flex");
    }

    function esqueceu() {
        var formEsqueceu = document.getElementById("formEsqueceu");
        var formLogin = document.getElementById("formularioLogin");
        var formCadastro = document.getElementById("formCadastro");
        var cad = document.getElementById("cadastra");
        var btnGoogle = document.getElementById("googleLog");
        var btnFace = document.getElementById("faceLog");
        var btnMail = document.getElementById("mailLog");
        var esqueci = document.querySelector(".esqueci");
        var cadastra = document.querySelector(".cadastra");
        var tilt = document.querySelector(".someTilt");

        formEsqueceu.style.display = "block";
        formLogin.style.display = "none";
        formCadastro.style.display = "none";
        cad.style.display = "none";
        btnGoogle.style.display = "none";
        btnFace.style.display = "none";
        btnMail.style.display = "none";
        esqueci.style.display = "none";
        tilt.style.display = "none";
        cadastra.classList.add("d-none");
        cadastra.classList.remove("d-flex");
    }

    function mostrarCadastro() {
        var formLogin = document.getElementById("formularioLogin");
        var formCadastro = document.getElementById("formCadastro");
        var cad = document.getElementById("cadastra");
        var btnGoogle = document.getElementById("googleLog");
        var btnFace = document.getElementById("faceLog");
        var btnMail = document.getElementById("mailLog");
        var esqueci = document.querySelector(".esqueci");
        var cadastra = document.querySelector(".cadastra");

        formLogin.style.display = "none";
        formCadastro.style.display = "block";
        cad.style.display = "none";
        btnGoogle.style.display = "none";
        btnFace.style.display = "none";
        btnMail.style.display = "none";
        esqueci.style.display = "none";
        cadastra.classList.add("d-none");
        cadastra.classList.remove("d-flex");
    }


    function reverterAlteracoes() {
        var formEsqueceu = document.getElementById("formEsqueceu");
        var formulario = document.getElementById("formularioLogin");
        var formCadastro = document.getElementById("formCadastro");
        var cad = document.getElementById("cadastra");
        var btnGoogle = document.getElementById("googleLog");
        var btnFace = document.getElementById("faceLog");
        var btnMail = document.getElementById("mailLog");
        var esqueci = document.querySelector(".esqueci");
        var cadastra = document.querySelector(".cadastra");
        var tilt = document.querySelector(".someTilt");

        formulario.style.display = "none";
        formEsqueceu.style.display = "none";
        formCadastro.style.display = "none";
        cad.style.display = "block";
        btnGoogle.style.display = "block";
        btnFace.style.display = "block";
        btnMail.style.display = "block";
        esqueci.style.display = "none";
        tilt.style.display = "flex";
        cadastra.classList.add("d-flex");
        cadastra.classList.remove("d-none");
    }
    function fecharModal() {

        document.getElementById('modal').style.display = 'none';
    }

    $(document).ready(function () {
        const modal = document.getElementById('modal');
        const closeButton = document.getElementById('close');
        const linkToAccess = document.querySelectorAll('.abreModal');

        if (linkToAccess != null) {
            linkToAccess.forEach((e) => {
                e.addEventListener('click', function (event) {
                    event.preventDefault();
                    modal.style.display = 'flex';
                });

            });
        }

        if (modal != null && closeButton != null) {
            closeButton.addEventListener('click', function () {
                modal.style.display = 'none';
            });


            window.addEventListener('click', function (event) {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }
    });




} catch (e) {

}

