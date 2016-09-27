$(window, document, undefined).ready(function() {

  $('input').blur(function() {
    var $this = $(this);
    if ($this.val())
      $this.addClass('used');
    else
      $this.removeClass('used');
  });

  var $ripples = $('.ripples');

  $ripples.on('click.Ripples', function(e) {

    var $this = $(this);
    var $offset = $this.parent().offset();
    var $circle = $this.find('.ripplesCircle');

    var x = e.pageX - $offset.left;
    var y = e.pageY - $offset.top;

    $circle.css({
      top: y + 'px',
      left: x + 'px'
    });

    $this.addClass('is-active');

  });

  $ripples.on('animationend webkitAnimationEnd mozAnimationEnd oanimationend MSAnimationEnd', function(e) {
  	$(this).removeClass('is-active');
  });
  
  $("body").on("input",".uppercase", function(e) {
	    if (e.which >= 97 && e.which <= 122) {
	        var newKey = e.which - 32;
	        // I have tried setting those
	        e.keyCode = newKey;
	        e.charCode = newKey;
	    }

	    $(this).val(($(this).val()).toUpperCase());
	});
  
});