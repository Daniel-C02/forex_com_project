//////////////////////////////
///////Hamburger Button///////
//////////////////////////////
$(document).ready(function () {
  var trigger = $('.hamburger'),
      overlay = $('.overlay'),
     isClosed = false;

    trigger.click(function () {
      hamburger_cross();      
    });

    function hamburger_cross() {

      if (isClosed == true) {          
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        isClosed = false;
      } else {   
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        isClosed = true;
      }
  }
  
  $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
  });  
});


//////////////////////////////
/////////Search Bar/////////
//////////////////////////////

$(function(){
  $('.searchTerm').on("focus blur", function(){   
    $(this).parent().toggleClass("expanded collapsed");
     $(this).siblings('.suggestionBox').toggle();
    });
});


//////////////////////////////
/////////Date Function/////////
//////////////////////////////

function fullyear() {
  var date = new Date();
  var year = date.getFullYear();
  return year;
};  
document.getElementById("date").innerHTML = fullyear();
document.getElementById("date1").innerHTML = fullyear();



//////////////////////////////
/////////footer Function/////////
//////////////////////////////
function footer() {
  // $("#nav_Footer").css("top", (window.innerHeight-40)+"px");
  // $("#nav_Footer").css("bottom", "auto");
  document.getElementById("nav_Footer").style.top = (window.innerHeight-40)+"px";
  document.getElementById("nav_Footer").style.bottom = "auto";
};  
