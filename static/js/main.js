/*jslint node: true */
'use strict';

$(document).ready(() => {

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

    $like.on('click', handleClick)

});