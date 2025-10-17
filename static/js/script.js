
(function ($) {
    'use strict';


    // Fixed header
    $(window).on('scroll', function () {
        if ($(window).scrollTop() > 70) {
            $('.site-navigation,.trans-navigation').addClass('header-white');
            /*$('.ap-option').removeClass('d-none');*/
        } else {
            $('.site-navigation,.trans-navigation').removeClass('header-white');
            /*$('.ap-option').addClass('d-none');*/
        }
    });


    // navbarDropdown
    if ($(window).width() < 992) {
        $('.navbar-collapse .dropdown-toggle').on('click', function () {
            $(this).siblings('.dropdown-menu').animate({
                height: 'toggle'
            }, 300);
        });
    }


    // counter
    // counter
    // counter
    function counter() {
        var oTop;
        if ($('.counter').length !== 0) {
            oTop = $('.counter').offset().top - window.innerHeight;
        }
        if ($(window).scrollTop() > oTop) {
            $('.counter').each(function () {
                var $this = $(this),
                    countTo = parseFloat($this.attr('data-count'));

                $({
                    countNum: parseFloat($this.text()) || 0
                }).animate({
                    countNum: countTo
                }, {
                    duration: 500,
                    easing: 'swing',
                    step: function () {
                        $this.text(this.countNum % 1 === 0 ? this.countNum.toFixed(0) : this.countNum.toFixed(1));
                    },
                    complete: function () {
                        $this.text(this.countNum % 1 === 0 ? this.countNum.toFixed(0) : this.countNum.toFixed(1));
                    }
                });
            });
        }
    }


    $(window).on('scroll', function () {
        counter();
    });

    // Smooth Scroll
    $('a.nav-link').click(function (e) {
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                e.preventDefault();
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000, function () {
                    var $target = $(target);
                    $target.focus();
                    if ($target.is(':focus')) {
                        return false;
                    } else {
                        $target.attr('tabindex', '-1');
                        $target.focus();
                    }
                });
            }
        }
    });
    $('.navbar-collapse .navbar-nav a').on('click', function () {
        $('.navbar-toggler:visible').click();
    });


})(jQuery);