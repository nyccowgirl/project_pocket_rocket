/*jslint node: true */
'use strict';

$(document).ready(() => {

// modifies styling of navbar items for current page

  $('a[href="' + this.location.pathname + '"]').parent().addClass('active');

// processes log-in modal

  function displayMsg(results) {
    alert();

    if (results.code === 'error') {
        let text = $('#order-error');
        text.css('color', 'red');
    };
    location.reload('/');
  }

  function logIn(evt) {
    evt.preventDefault();
    let formInputs = {
      'user-input': $('#login_username').val(),
      'pword': $('$login_password'.val(),
    };
    $.post('/login', formInputs, displayMsg)
  }

  $('#login-form').on('submit', logIn);

// Resets password
  // <!-- FIXME: Not sure if the prior two lines are needed. -->

  function checkEmail(result) {
    if (!$('.user-input').val()) {
        alert('Please input a user name or email');
    } else if (result == False) {
        alert('User name or email does not exist. Please check your input or register.');
    };
  }

  function sendEmail(evt) {
    evt.preventDefault();
    checkEmail();
    let result = $.get('/pword-reset',checkEmail);
    // TO DO: send link to email to reset password
    };
  }

  $('#resetBtn').on('click', sendEmail)


// processes like buttons on reviews

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