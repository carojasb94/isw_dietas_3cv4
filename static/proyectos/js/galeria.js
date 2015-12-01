$('.img-galeria').click(function () {
    $('.img-galeria').css('borderColor', '#fff');
    $(this).css('borderColor', '#009688');
    $('input[name="foto_seleccionada"]').val($(this).attr('id'));
    $('.hover-aceptar').fadeOut();
    $('#hover-aceptar'+$(this).attr('id')).fadeIn();
});

$('.hover-aceptar button').click(function () {
    $('form').submit();
});