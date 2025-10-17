
function verificarAluga(tipo) {
    var valor = document.getElementById("kt_slider_basic_valor");
    var area = document.getElementById("kt_slider_basic_area");
    if (tipo == "aluguel") {

        if (area != null) {
            area.classList.add("d-none");
        }

        if (valor != null) {
            valor.classList.add("d-none");
        }
    } else {
        if (area != null) {
            area.classList.remove("d-none");
        }

        if (valor != null) {
            valor.classList.remove("d-none");
        }
    }
}



function limparSlideArea() {
    document.querySelector("#kt_slider_basic_area").noUiSlider.set([0, 5000]);
}

function limparSlideValor() {


    document.querySelector("#kt_slider_basic_valor").noUiSlider.set([0, 10000000]);
}

function limparSlideCondo() {
    document.querySelector("#kt_slider_basic_cond").noUiSlider.set([0, 10000]);
}


function mostrarAbaBranca() {
    var overlay = document.getElementById("overlayy");
    var abaBranca = document.getElementById("ababranca");
    overlay.style.display = "block";
    abaBranca.classList.add("mostrar-aba");
    document.body.style.overflow = "hidden";
}

function fecharAbaBranca() {
    var overlay = document.getElementById("overlayy");
    var abaBranca = document.getElementById("ababranca");
    overlay.style.display = "none";
    abaBranca.classList.remove("mostrar-aba");
    document.body.style.overflow = "visible";
}

function iniciarComandos(param) {


    var btnFiltros = document.getElementById("btnfiltros");

    if (btnFiltros != null) {
        btnFiltros.addEventListener("click", mostrarAbaBranca);
    }



    var iconeFechar = document.getElementById("fechar-icone");
    if (iconeFechar != null) {
        iconeFechar.addEventListener("click", fecharAbaBranca);
    }



    var overlay = document.getElementById("overlayy");

    if (overlay != null) {
        overlay.addEventListener("click", function (event) {
            if (event.target === overlay) {
                fecharAbaBranca();
            }
        });
    }








    try {
        $('.select2me').select2();
        $('.select2me').on('change', function (e) {
            const selectedValue = $(this).val();

            switch (e.target.id.toLowerCase()) {
                case "ddlcidade":
                    $('#cidadeInput').val(selectedValue).trigger('change.select2');

                    param.invokeMethodAsync("UpdateDDL", selectedValue, "cidade");
                    break;
                case "cidadeinput":
                    $('#ddlCidade').val(selectedValue).trigger('change.select2');
                    param.invokeMethodAsync("UpdateDDL", selectedValue, "cidade");
                    break;

                case "ddlbairro":
                    param.invokeMethodAsync("UpdateDDL", $('#ddlBairro').val(), "bairro");
                    break;

                case "ddlempreendimento":
                    param.invokeMethodAsync("UpdateDDL", $('#ddlEmpreendimento').val(), "empreendimento");
                    break;

                case "ddlconstrutora":
                    param.invokeMethodAsync("UpdateDDL", $('#ddlConstrutora').val(), "incorporador");
                    break;
            }
        });



    } catch (e) {

    }



    try {

        var sliderArea = document.querySelector("#kt_slider_basic_area");
        var sliderValor = document.querySelector("#kt_slider_basic_valor");
        var sliderValorCond = document.querySelector("#kt_slider_basic_cond");

        var inputValorMin = document.getElementById('vValorMin');
        var inputValorMax = document.getElementById('vValorMax');

        var inputValorMinCond = document.getElementById('vValorMinCond');
        var inputValorMaxCond = document.getElementById('vValorMaxCond');

        var inputAreaMin = document.getElementById('vAreaMin');
        var inputAreaMax = document.getElementById('vAreaMax');


        if (sliderValor != null) {
            noUiSlider.create(sliderValor, {
                start: [0, 10000000],
                connect: true,
                range: {
                    "min": 0,
                    "max": 10000000
                }
            });

            sliderValor.noUiSlider.on("update", function (values, handle) {
                if (handle) {
                    inputValorMax.value = parseFloat(values[handle]);

                    if (!inputValorMax.value.includes('.')) {
                        inputValorMax.value += ',00'
                    }

                    formatCurrency(inputValorMax, inputValorMax.value.replace(/\./g, ','));

                } else {
                    inputValorMin.value = parseFloat(values[handle]);
                    if (!inputValorMin.value.includes('.')) {
                        inputValorMin.value += ',00'
                    }
                    formatCurrency(inputValorMin, inputValorMin.value.replace(/\./g, ','));



                }

                //param.invokeMethodAsync("UpdateRange", inputValorMin.value, inputValorMax.value, "valor");

            });

            inputValorMax.addEventListener('change', function () {
                this.value = this.value.replace('R$', '').replace(/\./g, '').replace(',', ".")
                sliderValor.noUiSlider.set([null, this.value]);
            });

            inputValorMin.addEventListener('change', function () {
                this.value = this.value.replace('R$', '').replace(/\./g, '').replace(',', ".")

                sliderValor.noUiSlider.set([this.value, null]);

            });



        }


        if (sliderArea != null) {
            noUiSlider.create(sliderArea, {
                start: [0, 5000],
                connect: true,
                range: {
                    "min": 0,
                    "max": 5000
                }
            });

            sliderArea.noUiSlider.on("update", function (values, handle) {

                if (handle) {
                    inputAreaMax.value = parseFloat(values[handle])

                    if (!inputAreaMax.value.includes('.')) {
                        inputAreaMax.value += ',00'
                    }
                    formatCurrency(inputAreaMax, inputAreaMax.value.replace(/\./g, ','), 'area');
                } else {
                    inputAreaMin.value = parseFloat(values[handle])

                    if (!inputAreaMin.value.includes('.')) {
                        inputAreaMin.value += ',00'
                    }
                    formatCurrency(inputAreaMin, inputAreaMin.value.replace(/\./g, ','), 'area');
                }

                //param.invokeMethodAsync("UpdateRange", inputAreaMin.value, inputAreaMax.value, 'area');

            });

            inputAreaMax.addEventListener('change', function () {
                this.value = this.value.substring(0, this.value.length - 2).replace(/\./g, '').replace(',', ".")
                sliderArea.noUiSlider.set([null, this.value]);
            });

            inputAreaMin.addEventListener('change', function () {
                this.value = this.value.substring(0, this.value.length - 2).replace(/\./g, '').replace(',', ".")
                sliderArea.noUiSlider.set([this.value, null]);
            });
        }



        if (sliderValorCond != null) {
            noUiSlider.create(sliderValorCond, {
                start: [0, 10000],
                connect: true,
                range: {
                    "min": 0,
                    "max": 10000
                }
            });

            sliderValorCond.noUiSlider.on("update", function (values, handle) {

                if (handle) {
                    inputValorMaxCond.value = parseFloat(values[handle])

                    if (!inputValorMaxCond.value.includes('.')) {
                        inputValorMaxCond.value += ',00'
                    }
                    formatCurrency(inputValorMaxCond, inputValorMaxCond.value.replace(/\./g, ','));
                } else {
                    inputValorMinCond.value = parseFloat(values[handle])
                    if (!inputValorMinCond.value.includes('.')) {
                        inputValorMinCond.value += ',00'
                    }
                    formatCurrency(inputValorMinCond, inputValorMinCond.value.replace(/\./g, ','));
                }

                //param.invokeMethodAsync("UpdateRange", inputValorMinCond.value, inputValorMaxCond.value, 'condominio');

            });

            inputValorMaxCond.addEventListener('change', function () {
                this.value = this.value.replace('R$', '').replace(/\./g, '').replace(',', ".")
                sliderValorCond.noUiSlider.set([null, this.value]);
            });

            inputValorMinCond.addEventListener('change', function () {
                this.value = this.value.replace('R$', '').replace(/\./g, '').replace(',', ".")
                sliderValorCond.noUiSlider.set([this.value, null]);
            });
        }


    } catch (e) {

    }


    try {

        var sliderArea = document.querySelector("#kt_slider_basic_area");
        var sliderValor = document.querySelector("#kt_slider_basic_valor");
        var sliderValorCond = document.querySelector("#kt_slider_basic_cond");

        var inputValorMin = document.getElementById('vValorMin');
        var inputValorMax = document.getElementById('vValorMax');

        var inputValorMinCond = document.getElementById('vValorMinCond');
        var inputValorMaxCond = document.getElementById('vValorMaxCond');

        var inputAreaMin = document.getElementById('vAreaMin');
        var inputAreaMax = document.getElementById('vAreaMax');


        if (sliderValor != null) {
            noUiSlider.create(sliderValor, {
                start: [0, 10000000],
                connect: true,
                range: {
                    "min": 0,
                    "max": 10000000
                }
            });

            sliderValor.noUiSlider.on("update", function (values, handle) {
                if (handle) {
                    inputValorMax.value = parseFloat(values[handle]);

                    if (!inputValorMax.value.includes('.')) {
                        inputValorMax.value += ',00'
                    }

                    formatCurrency(inputValorMax, inputValorMax.value.replace(/\./g, ','));

                } else {
                    inputValorMin.value = parseFloat(values[handle]);
                    if (!inputValorMin.value.includes('.')) {
                        inputValorMin.value += ',00'
                    }
                    formatCurrency(inputValorMin, inputValorMin.value.replace(/\./g, ','));



                }

                //param.invokeMethodAsync("UpdateRange", inputValorMin.value, inputValorMax.value, "valor");

            });

            inputValorMax.addEventListener('change', function () {
                this.value = this.value.replace('R$', '').replace(/\./g, '').replace(',', ".")
                sliderValor.noUiSlider.set([null, this.value]);
            });

            inputValorMin.addEventListener('change', function () {
                this.value = this.value.replace('R$', '').replace(/\./g, '').replace(',', ".")

                sliderValor.noUiSlider.set([this.value, null]);

            });



        }


        if (sliderArea != null) {
            noUiSlider.create(sliderArea, {
                start: [0, 5000],
                connect: true,
                range: {
                    "min": 0,
                    "max": 5000
                }
            });

            sliderArea.noUiSlider.on("update", function (values, handle) {

                if (handle) {
                    inputAreaMax.value = parseFloat(values[handle])

                    if (!inputAreaMax.value.includes('.')) {
                        inputAreaMax.value += ',00'
                    }
                    formatCurrency(inputAreaMax, inputAreaMax.value.replace(/\./g, ','), 'area');
                } else {
                    inputAreaMin.value = parseFloat(values[handle])

                    if (!inputAreaMin.value.includes('.')) {
                        inputAreaMin.value += ',00'
                    }
                    formatCurrency(inputAreaMin, inputAreaMin.value.replace(/\./g, ','), 'area');
                }

                //param.invokeMethodAsync("UpdateRange", inputAreaMin.value, inputAreaMax.value, 'area');

            });

            inputAreaMax.addEventListener('change', function () {
                this.value = this.value.substring(0, this.value.length - 2).replace(/\./g, '').replace(',', ".")
                sliderArea.noUiSlider.set([null, this.value]);
            });

            inputAreaMin.addEventListener('change', function () {
                this.value = this.value.substring(0, this.value.length - 2).replace(/\./g, '').replace(',', ".")
                sliderArea.noUiSlider.set([this.value, null]);
            });
        }



        if (sliderValorCond != null) {
            noUiSlider.create(sliderValorCond, {
                start: [0, 10000],
                connect: true,
                range: {
                    "min": 0,
                    "max": 10000
                }
            });

            sliderValorCond.noUiSlider.on("update", function (values, handle) {

                if (handle) {
                    inputValorMaxCond.value = parseFloat(values[handle])

                    if (!inputValorMaxCond.value.includes('.')) {
                        inputValorMaxCond.value += ',00'
                    }
                    formatCurrency(inputValorMaxCond, inputValorMaxCond.value.replace(/\./g, ','));
                } else {
                    inputValorMinCond.value = parseFloat(values[handle])
                    if (!inputValorMinCond.value.includes('.')) {
                        inputValorMinCond.value += ',00'
                    }
                    formatCurrency(inputValorMinCond, inputValorMinCond.value.replace(/\./g, ','));
                }

                //param.invokeMethodAsync("UpdateRange", inputValorMinCond.value, inputValorMaxCond.value, 'condominio');

            });

            inputValorMaxCond.addEventListener('change', function () {
                this.value = this.value.replace('R$', '').replace(/\./g, '').replace(',', ".")
                sliderValorCond.noUiSlider.set([null, this.value]);
            });

            inputValorMinCond.addEventListener('change', function () {
                this.value = this.value.replace('R$', '').replace(/\./g, '').replace(',', ".")
                sliderValorCond.noUiSlider.set([this.value, null]);
            });
        }


    } catch (e) {

    }
}

try {
    var btnMapa = document.getElementById("btnMapa");
    var imoveisSection = document.getElementById("imoveis");

    if (btnMapa != null) {



        btnMapa.addEventListener('click', () => {
            var lista = document.getElementById("lista");
            var mapa = document.getElementById("mapa");
            var gridContainer = document.querySelector(".grid-container");


            if (window.innerWidth <= 992) {
                // Largura da tela menor ou igual a 992px
                if (lista.classList.contains("d-none")) {
                    lista.classList.remove("d-none");
                    lista.classList.add("d-flex");
                    mapa.classList.add("d-none");
                    btnMapa.textContent = "mostrar mapa";
                } else {
                    lista.classList.add("d-none");
                    lista.classList.remove("d-flex");
                    mapa.classList.remove("d-none");
                    btnMapa.textContent = "mostrar lista";
                }
            } else {



                if (lista.classList.contains("col-lg-12")) {
                    lista.classList.remove("col-lg-12");

                    lista.classList.add("col-lg-6");
                    gridContainer.style.gridTemplateColumns = "repeat(1, 1fr)";
                    mapa.classList.remove("d-none");
                    btnMapa.textContent = "mostrar lista";
                } else {

                    lista.classList.remove("col-lg-6");
                    lista.classList.add("col-lg-12");
                    gridContainer.style.gridTemplateColumns = "repeat(2, 1fr)";
                    mapa.classList.add("d-none");
                    btnMapa.textContent = "mostrar mapa";

                }


            }
        });


        function TratarCard() {
            var btnMapa = document.getElementById("btnMapa");

            if (btnMapa != null) {

                var mapaVerificar = document.getElementById("mapa");
                var mdcol = document.querySelectorAll(".mdcol");
                var descri = document.querySelectorAll(".descri");
                var mbsin = document.querySelectorAll(".mbsin");

                if (mapaVerificar.classList.contains('d-none')) {

                    mbsin.forEach(function (e) {
                        e.classList.remove("mb-3");
                    });

                    descri.forEach(function (e) {
                        e.classList.remove("d-none");
                    });


                    mdcol.forEach(function (e) {
                        e.classList.add("col-lg-6");
                        e.classList.remove("col-lg-12");
                    });
                } else {
                    mbsin.forEach(function (e) {
                        e.classList.add("mb-3");
                    });

                    descri.forEach(function (e) {
                        e.classList.add("d-none");
                    });

                    mdcol.forEach(function (e) {
                        e.classList.remove("col-lg-6");
                        e.classList.add("col-lg-12");
                    });
                }




            }

        }


        // Adicionar um ouvinte de evento para rolagem da p�gina
        window.addEventListener("scroll", function () {
            if (window.innerWidth <= 992) {
                // Largura da tela menor ou igual a 992px
                var imoveisSectionTop = imoveisSection.getBoundingClientRect().top;
                if (imoveisSectionTop < window.innerHeight) {
                    // Parte superior da se��o imoveis vis�vel na janela
                    btnMapa.style.display = "block";
                } else {
                    btnMapa.style.display = "none";
                }
            }
        });
    }
} catch (e) {

}