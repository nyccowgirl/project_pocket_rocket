/*jslint node: true */
'use strict';

$(document).ready(() => {

// modifies styling of navbar items for current page


  $('.nav-item').on('click', (function() {
    $('.nav-item .active').removeClass('active');
    if (!$(this).hasClass('active')) {
      $(this).addClass('active');
    };
  });


  let $like = $('.like');

// process like buttons on reviews

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