$(document).ready(function(){
	$('.grid').imagesLoaded()
	  .always( function( instance ) {
	    console.log('all images loaded');
	    
		
	  })
	  .done( function( instance ) {
	    console.log('all images successfully loaded');
	    $('.grid').masonry({
			initLayout: true,
		 	itemSelector: '.grid-item',
		 	columnWidth: '.grid-sizer',
		 	percentPosition: true,
		  	resize: true,
		    stagger: 30,
		 	fitWidth: true,
		 	gutter: 10
		});
	  })
	  .fail( function() {
	    console.log('all images loaded, at least one is broken');
	  })
	  .progress( function( instance, image ) {
	    var result = image.isLoaded ? 'loaded' : 'broken';
	    console.log( 'image is ' + result + ' for ' + image.img.src );
	  });
	// $('.grid').on( 'click', '.grid-item', function() {
	//   // remove clicked element
	//   $('.grid').masonry()
	//   // $('.grid').masonry( 'remove', this )
	//     // layout remaining item elements
	//     .masonry('layout');
	// });
});