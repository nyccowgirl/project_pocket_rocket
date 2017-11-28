/*jslint node: true */
'use strict';

$(document).ready(() => {

  // $('#modalLRForm .nav-link').button('toggle').addClass('active');

  $(function() {

    let $formLogin = $('#login-form');
    let $formLost = $('#lost-form');
    let $formRegister = $('#register-form');
    let $divForms = $('#div-forms');
    let $modalAnimateTime = 300;
    let $msgAnimateTime = 150;
    let $msgShowTime = 2000;

    $('form').on('submit', function(evt) {
      evt.preventDefault();
      let test = {};
      let formInputs = new FormData(this);
      for (var [key, value] of formInputs.entries()) {
        test[key] = value;
      };
      // may be same as formInputs.serialize()
      switch(this.id) {
        case 'biz-search':

        case 'login-form':
          $.post('/login', test, displayMsg);
          break;
        case 'lost-form':
          if (!$('#email-lost')) {
            alert('Please input your email.');
          }
          $.get('/email-check', test, checkEmail);
          break;
        case 'register-form':
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
              success: displayMsg,
              error: displayMsg
            });
            // $.post('/register', test, displayMsg);
          };
          break;
        default:
          alert('Something is broken. Check back later!');
      }
    });


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

    function displayMsg(results) {
      if (results.code === 'error') {
        alert(results.msg);
      } else {
        alert(results.msg);
      }
      location.reload('/');
    }

    function checkEmail(results) {
      if (results === 'False') {
        alert('Email does not exist. Please check your input or register.');
      } else if (results === 'True') {
        alert('A link has been sent to your email to reset your password.');
        location.reload('/pword-reset');
      } else {
        alert('Please try again.');
      }
    }

  });


});