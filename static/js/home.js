$(document).ready(function () {
    try {
        if (document.querySelector('.anunciaHome') != null) {

            $(".anunciaHome").click(function () {
                $(".anunciaHome").removeClass("active");
                $(this).addClass("active");

            });
        }
    } catch (e) {

    }
    $(".opBusca").click(function () {
        $(".opBusca").removeClass("active");
        $(this).addClass("active");
    });
});

document.querySelectorAll('.cliqueEvento').forEach(item => {
    item.addEventListener('click', event => {
        document.querySelector('.alertaEvento').style.display = 'block';
        setTimeout(() => {
            document.querySelector('.alertaEvento').style.display = 'none';
        }, 4000); // 4 segundos
    });
});

