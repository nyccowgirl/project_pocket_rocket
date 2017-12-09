/*jslint node: true */
'use strict';

$(document).ready(() => {

  // $('#modalLRForm .nav-link').button('toggle').addClass('active');

  $(function() {

    let $formLogin = $('#login-div');
    let $formLost = $('#lost-div');
    let $formRegister = $('#register-div');
    let $divForms = $('#div-forms');
    let $modalAnimateTime = 300;
    let $msgAnimateTime = 150;
    let $msgShowTime = 2000;



    $('#login_register_btn').click( function () { modalAnimate($formLogin, $formRegister) });
    $('#register_login_btn').click( function () { modalAnimate($formRegister, $formLogin); });
    $('#login_lost_btn').click( function () { modalAnimate($formLogin, $formLost); });
    $('#lost_login_btn').click( function () { modalAnimate($formLost, $formLogin); });
    $('#lost_register_btn').click( function () { modalAnimate($formLost, $formRegister); });
    $('#register_lost_btn').click( function () { modalAnimate($formRegister, $formLost); });

    function modalAnimate ($oldForm, $newForm) {
        let $oldH = $oldForm.height();
        let $newH = $newForm.height();
        $divForms.css('height',$oldH);
        $oldForm.fadeToggle($modalAnimateTime, function() {
            $divForms.animate({height: $newH}, $modalAnimateTime, function() {
                $newForm.fadeToggle($modalAnimateTime);
            });
        });
    }

    // FIXME: modalAnimate, makes form disappear but when change $formLogin to #login-div, size of pane is right but nothing appears for normal tabbing


  });

  function msgReload(results) {
    if (results.code === 'danger') {
      alert(results.msg);
    } else {
      alert(results.msg);
      location.reload('/');
    }
  }

  function checkEmail(results) {
    if (results === 'False') {
      alert('Email does not exist. Please check your input or register.');
    } else if (results === 'True') {
      alert('A link has been sent to your email to reset your password.');
      // location.reload('/pword-reset');
    } else {
      alert('Please try again.');
    }
  }

  $('#login-form').on('submit', function(evt) {
    evt.preventDefault();
    let formInputs = {
      'user-input': $('#user-input').val(),
      'pword': $('#pword').val()
    };
    $.post('/login', formInputs, msgReload);
  });

  $('#lost-form').on('submit', function(evt) {
    evt.preventDefault();
    if (!$('#email-lost')) {
      alert('Please input your email.');
    } else {
      let formInputs = {
        'email': $('#email-lost').val()
      }
      $.get('/email-check', formInputs, checkEmail);
    };
  });

  $('#register-form').on('submit', function(evt) {
    evt.preventDefault();
    let formInputs = new FormData(this);
    let pword1 = $('#pword-reg').val();
    let pword2 = $('#pword-rep').val();
    if (pword1 != pword2) {
      alert('The password does not match. Try again.');
    } else {
      $.ajax({
        type: 'POST',
        cache: false,
        url: '/register',
        enctype: 'multipart/form-data',
        data: formInputs,
        processData: false,
        contentType: false,
        success: msgReload,
        error: msgReload
      });
  }});

});