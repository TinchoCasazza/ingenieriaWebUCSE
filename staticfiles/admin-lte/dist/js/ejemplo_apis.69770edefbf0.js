function actualizar_contador() {
    $.ajax({url: "/api/cantidad_grupos/"}).done(on_nuevo_valor_contador);
}

function on_nuevo_valor_contador(data) {
    var span_contador = $('#contador-grupos');
    span_contador.html(data.cantidad_noticias);
}

function inicializar() {
    setInterval(actualizar_contador, 2000);
}
 $(inicializar);