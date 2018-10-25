// Funciones al Cargar el Dom

$( document ).ready(function() {
    RecargarSuscripciones();
});


// Token Ajax
$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                        }
                    }
                }
                return cookieValue;
            }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//--------------------------------//

// Modal Plan de Estudio
var doc = new jsPDF();
var specialElementHandlers = {
  '#exampleModal': function (element, renderer) {
      return true;
  }
};
$('#generarPDF').click(function () {   
    // Carga los elementos del PDF
    var contenido = window.document.getElementById("modalBody");
    var imgData =  new Image();
    imgData.src = '../static/images/plan_ingenieria.jpeg';
    var imgData2 =  new Image();
    imgData2.src = '../static/images/plan_ingenieria2.jpeg';
    doc.fromHTML(contenido, 15, 15, {
        'width': 170,
        'elementHandlers': specialElementHandlers
    });
    console.log(imgData);
    // Seteo de los parametros del PDF
    doc.addImage(imgData, 'JPEG',0,10, 210, 210);
    doc.addPage();
    doc.addImage(imgData2, 'JPEG',0,10, 200, 210);
    doc.save('sample-file.pdf');
});

$('#carrera').text( "Plan de estudio de " + $('#selectCarrera option:selected').html());
$('#selectCarrera').change(function(){
  var seleccion = $('#selectCarrera option:selected').html();
  $('#carrera').text( "Plan de estudio de " + seleccion);
  console.log(seleccion);
});
//--------------------------------//

// Cambio de Skin
$('#skin').on('click touchstart','li', function() {
  var bodyColor = $("#bodyColor");
  
  bodyColor.removeClass();
  bodyColor.addClass("hold-transition");
  bodyColor.addClass("sidebar-mini");
  bodyColor.addClass($(this).attr('data'));
  CambiarSkin($(this).attr('data'));
});

function CambiarSkin(skin){
    console.log("Post " + skin); 
    $.ajax({
      type: 'POST',
      url: '/cambiarSkin/', //direccion a donde hace las requets
      data: {skin: skin},
      success: function (data) {
          console.log("Cambio exitoso a " + skin);
      },
      error: function(data) {
      }
    });
};

//--------------------------------//


// Crear Grupos
function CrearGrupo(){
    var nombreGrupo = $("#id_NombreGrupo").val();
    var nivelAcceso = $('#id_NivelAcceso option:selected').text();
    console.log(nivelAcceso);
    $.ajax({
      type: 'POST',
      url: '/grupos/crear_grupo/', //direccion a donde hace las requets
      data: {nombreGrupo: nombreGrupo, nivelAcceso : nivelAcceso},
      success: function (data) {
            console.log("Grupo creado "+ nombreGrupo + " con exito ");
            location.href ="/grupos/";
      },
      error: function(data) {
      }
    });
};

//--------------------------------//

// Suscribirse
function Suscribirse(comp){

    var grupoId = comp.id;
    var id = grupoId.substr(5);
    console.log(id);
    $("#" + grupoId).hide();

    $.ajax({
        type: 'POST',
        url: '/grupos/suscribirse/', //direccion a donde hace las requets
        data: { id: id },
        success: function (data) {
              console.log("Suscripcion al Grupo "+ id  + " con exito ");
              location.href ="/grupos/";
        },
        error: function(data) {
        }
      });

}

setInterval(RecargarSuscripciones, 60000);

//--------------------------------//

// Publicaciones

function Publicar(){
    var contenidoPublicacion = $("#contenidoPublicacion").val();
    console.log(contenidoPublicacion)
    $.ajax({
      type: 'POST',
      url: '/publicar/', //direccion a donde hace las requets
      data: {contenidoPublicacion: contenidoPublicacion},
      success: function (data) {
      },
      error: function(data) {
      }
    });
};

function borrarPublicacion(comp){
  // Recibe como "COMP" el ID de la publicacion a ELIMINAR
  let publicacionId = comp.id;
  var pkPublicacion = publicacionId.substr(9);
  // Se parcea el ID , y se realiza el POST a la URL 
  $.ajax({
      type: 'POST',
      url: '/publicar/borrar/', //direccion a donde hace las requets
      data: {publicacionId: pkPublicacion},
      success: function (data) {
          console.log("Borrado exitosamente ");
      },
      error: function(data) {
          console.log(data);
          console.log("Accion no permitida ");
      }
  });
}
function modificarPublicacion(comp){
  let publicacionId = comp.id;
  var pkPublicacion = publicacionId.substr(12);
  $("#" + publicacionId).hide();
  var selector = "#publicacion" + pkPublicacion;
  var contenidoPublicacion = $(selector).text();
  $(selector).html('<textarea id="contenidoModifacion' + pkPublicacion + '" class="col-xs-12" cols="40" style="resize: none;"></textarea><div class="pull-right" style="margin-top:5px;"><button type="button" id="btnGuardar'+ pkPublicacion +'" class="btn btn-success btn-sm" onclick="guardarPublicacion(this)">Guardar</button></div>');
  $("#contenidoModifacion" + pkPublicacion).val(contenidoPublicacion);
};

function guardarPublicacion(comp){
  let publicacionId = comp.id;
  var pkPublicacion = publicacionId.substr(10);
  
  console.log(publicacionId);
  $("#btnModificar" + pkPublicacion).show();
  var contenido = $("#contenidoModifacion" + pkPublicacion).val();
  // Se parcea el ID , y se realiza el POST a la URL 
  $.ajax({
      type: 'POST',
      url: '/publicar/guardar/', //direccion a donde hace las requets
      data: {publicacionId: pkPublicacion , contenido: contenido},
      success: function (data) {
          var selector = "#publicacion" + pkPublicacion;
          $(selector).html(contenido);
          console.log("Modificado exitosamente ");
      },
      error: function(data) {
          console.log("Accion no permitida ");
      }
  });
}
function validarEnter(e,pk){
    if (e.keyCode === 13 && !e.shiftKey) {
        e.preventDefault();
        publicarComentario(pk);
    }
}
function publicarComentario(pk){
  
  var contenido = $("#contenidoComentario" + pk).val();
  // Se parcea el ID , y se realiza el POST a la URL 
  $.ajax({
      type: 'POST',
      url: '/publicar/comentar/', //direccion a donde hace las requets
      data: {publicacionId: pk , contenido: contenido},
      success: function (data) {
          console.log("Comentado exitosamente ");
          $("#contenidoComentario" + pk).val("");
          location.reload(); 
            
      },
      error: function(data) {
          console.log("Accion no permitida ");
      }
  });
}


//--------------------------------//

function RecargarSuscripciones(){
    $("#mensajeSuscripcion").load(" #mensajeSuscripcion"); 
};

// Denunciar

function denunciarPublicacion(comp){

    var publicacionId = comp.id;
    var id = publicacionId.substr(12);
    console.log(id);

    $.ajax({
        type: 'POST',
        url: '/publicar/denunciar/', //direccion a donde hace las requets
        data: { id: id },
        success: function (data) {
              console.log(data);
              $("#divPublicacion").load(" #divPublicacion"); 
        },
        error: function(data) {
        }
      });

}

//--------------------------------//
