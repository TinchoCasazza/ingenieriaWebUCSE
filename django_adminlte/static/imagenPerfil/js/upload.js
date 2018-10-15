var feedback = function(res) {
    if (res.success === true) {
        var get_link = res.data.link.replace(/^http:\/\//i, 'https://');
        document.querySelector('.status').classList.add('bg-success');
        document.querySelector('.status').innerHTML =
            'Image : ' + '<br><input id="urlImg" style=" visibility: hidden;" class="image-url" value=\"' + get_link + '\"/>';

		$(".status").css("visibility", "hidden");
		
		var imagen = $("#urlImg").val();
		console.log(imagen);
        $.ajax({
	      type: 'POST',
	      url: '/fotoPerfil/', //direccion a donde hace las requets
	      data: {imagen: imagen},
	      success: function (data) {
			$('#imagenModal').modal('toggle'); 
		    location.href = "/";
	      },
	      error: function(data) {
	      }
	    });
	    }
};

new Imgur({
    clientid: '6cafa06aa177ec7', //You can change this ClientID
    callback: feedback
});
