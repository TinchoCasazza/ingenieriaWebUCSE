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

// Cambio de Avatar
$("#iFoto").click(function () {
    $("input[type='file']").trigger('click');
  });
  
  $('input[type="file"]').on('change', function() {
    var file = $(this)[0].files[0];
    var formData = new FormData();
    formData.append('file', $(this)[0].files[0]);
  
    console.log(formData);
    $.ajax({
        type: 'POST',
        url: '/fotoPerfil/', //direccion a donde hace las requets
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log("Upload exitoso ");
            window.location.reload();
        },
        error: function(data) {
        }
      });
  })
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

function MostrarSuscripciones(){
    $.ajax({
        type: 'GET',
        url: '/api_v1/suscripcion/', //direccion a donde hace las requets
        success: function (data) {
            ArmarDesplegable(data);
        },
        error: function(data) {
        }
    });
}
    
function ArmarDesplegable(json){
    var cantidad = 0;

    for (var i in json) {
        console.log(json[i]);
        
        cantidad++; 
    }

    cantidad++;
    console.log($("#cSuscripciones"));
    $("#cSuscripciones").html(cantidad);
    
    if (cantidad == 0){
        $("#mensajeSuscripcion").html("No tiene solicitudes de Grupos")
    }

    if (cantidad == 1){
        $("#mensajeSuscripcion").html("Tiene " + cantidad + " solicitud nueva de Grupos")
    }

    if (cantidad > 1){
        $("#mensajeSuscripcion").html("Tiene " + cantidad + " solicitudes nuevas de Grupos")
    }

    console.log(cantidad);
}

setInterval(MostrarSuscripciones, 6000);

//--------------------------------//
