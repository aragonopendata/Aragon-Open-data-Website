//Función que sirve para cuando se haga over sobre una ficha de un conjunto de datos y que de más información
function recommendOver(){
	$(".recommendPackages .recommendThumbnail").hover(
		function(){
			var id = $(this).attr('id');
			$('#'+id+' .front').addClass("oculto");
			$('#'+id+' .back').removeClass("oculto");
			//console.log('Se entra en '+id);
		}, 
		function(){
			var id = $(this).attr('id');
			$('#'+id+' .front').removeClass("oculto");
			$('#'+id+' .back').addClass("oculto");
			//console.log('Se sale de '+id);
		}
	);
}

$(document).ready(function() {
	recommendOver();
} );
