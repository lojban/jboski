
// Stolen from https://stackoverflow.com/questions/32388869/limit-the-number-of-times-an-ajax-request-on-keyup-fires
//
// func       callback function
// wait       throttle time in ms
// immediate  bool, should callback be called on first event
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};

(function($) {

var ajaxRequest = null;

$(document).ready(function() {
  
  let refresh = function() {
    if (ajaxRequest) ajaxRequest.abort();

    var jboText = $("#input").val();
    var mode = $("#mode").val();
    let params;
    if (jboText) {
      params = { mode: mode, text: jboText, json: true };
    } else {
      params = { mode: mode, json: true };
    }
    ajaxRequest = $.getJSON("", params, function(json) {
      $("#output").html(json.html);
      
      if (json.grammatical) {
        $("#input").removeClass("ungrammatical");
        $("#input").addClass("grammatical");

        if (typeof(window.history) !== "undefined") {
          var link = $("<a/>")[0];
          link.href = window.location.href;
          if (jboText) {
            link.search = "?mode=" + escape(mode) + "&text=" + escape(jboText);
          } else {
            link.search = "?mode=" + escape(mode);
          }

          var title = jboText + " -- jboski";
          history.replaceState(null, title, link.href);
        }
      } else {
        $("#input").addClass("ungrammatical");
        $("#input").removeClass("grammatical");
      }
    });
  };

  $("#input").keyup(debounce(refresh, 500, false));
  $("#mode").change(refresh);
});

})(jQuery);
