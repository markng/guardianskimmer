$(document).ready(function() {
  $("div#nav ul li a").click(function(event){
    var link = $(this).attr('href');
    $.ajax({
      url: '/s' + link,
      cache: false,
      success: function(html){
        $("div.hfeed").fadeOut(500, function(){$(this).replaceWith(html)});
      }
    });
    event.preventDefault();
  });
});
