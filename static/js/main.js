/*jslint node: true */
'use strict';

$(document).ready(() => {

// modifies styling of navbar items for current page

  $('a[href="' + this.location.pathname + '"]').parent().addClass('active');

// shows log-in modal

  $('#login-modal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
  })

  $(function(){
  $('#loginform').submit(function(e){
    return false;
  });

  $('#modaltrigger').leanModal({ top: 110, overlay: 0.45, closeButton: ".hidemodal" });
});

// process like buttons on reviews

  let $like = $('.like');

  function disableLike(results) {
    alert(results);
  }

  function handleClick(evt) {
    evt.preventDefault();
    let formInputs = {
      'review_id': evt.target.id,
    };
    $.post('/like-review', formInputs, disableLike);
    $(this).prop('disabled', true);
  }

  $like.on('click', handleClick);

});