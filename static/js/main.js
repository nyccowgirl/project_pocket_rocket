/*jslint node: true */
'use strict';

$(document).ready(() => {

// modifies styling of navbar items for current page

  $('a[href="' + this.location.pathname + '"]').parent().addClass('active');

// processes log-in and password reset modal

  function checkEmail(result) {
    if (result === False) {
      msgChange($('#div-lost-msg'), $('#icon-lost-msg'), $('#text-lost-msg'), 'error', 'glyphicon-remove', 'User name or email does not exist. Please check your input or register.');
    } else if (result === True) {
      msgChange($('#div-lost-msg'), $('#icon-lost-msg'), $('#text-lost-msg'), 'success', 'glyphicon-ok', 'A link has been sent to your email to reset your password.');
    } else {
      alert('Please try again.')
    };
  }

  function sendEmail(evt) {
    // evt.preventDefault();
    let formInputs = {
      'user-input': $('#lost_email').val()
      // FIXME
    };
    $.get('/pword-reset', checkEmail);
    // TO DO: send link to email to reset password
  }

  function displayMsg(results) {
    // alert();
    // console.log(results);
    // if (results.code === 'error') {
    //     msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), 'error', 'glyphicon-remove', results.msg);
    // } else {
    //     msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), 'success', 'glyphicon-ok', results.msg);
    // };
    location.reload('/');
  }

  function logIn(evt) {
    // evt.preventDefault();
    let formInputs = {
      'user-input': $('#login_username').val(),
      'pword': $('#login_password').val()
    };
    $.post('/login', formInputs, displayMsg);
  }


  $(function() {
    let $formLogin = $('#login-form');
    let $formLost = $('#lost-form');
    // let $formRegister = $('#register-form');
    let $divForms = $('#div-forms');
    let $modalAnimateTime = 300;
    let $msgAnimateTime = 150;
    let $msgShowTime = 2000;

    $('form').on('submit', function (evt) {
      evt.preventDefault();

        switch(this.id) {
            case 'login-form':
                // evt.preventDefault();

                logIn(evt);

                // return false;
                break;
            case "lost-form":
                if (!$('#lost_email')) {
                  msgChange($('#div-lost-msg'), $('#icon-lost-msg'), $('#text-lost-msg'), 'error', 'glyphicon-remove', 'Please input a user name or email.');
                  break;
                };
                sendEmail(evt);

                // return false;
                break;
            default:
                // return false;
        }
        // return false;
    });

  // $('#login-form').on('submit', logIn);
  $('#login_lost_btn').on('click', function () { modalAnimate($formLogin, $formLost); });
  $('#lost_login_btn').on('click', function () { modalAnimate($formLost, $formLogin); });

  function modalAnimate ($oldForm, $newForm) {
      var $oldH = $oldForm.height();
      var $newH = $newForm.height();
      $divForms.css("height",$oldH);
      $oldForm.fadeToggle($modalAnimateTime, function(){
          $divForms.animate({height: $newH}, $modalAnimateTime, function(){
              $newForm.fadeToggle($modalAnimateTime);
          });
      });
  }

  function msgFade ($msgId, $msgText) {
      $msgId.fadeOut($msgAnimateTime, function() {
          $(this).text($msgText).fadeIn($msgAnimateTime);
      });
  }

  function msgChange($divTag, $iconTag, $textTag, $divClass, $iconClass, $msgText) {
      var $msgOld = $divTag.text();
      msgFade($textTag, $msgText);
      $divTag.addClass($divClass);
      $iconTag.removeClass("glyphicon-chevron-right");
      $iconTag.addClass($iconClass + " " + $divClass);
      setTimeout(function() {
          msgFade($textTag, $msgOld);
          $divTag.removeClass($divClass);
          $iconTag.addClass("glyphicon-chevron-right");
          $iconTag.removeClass($iconClass + " " + $divClass);
    }, $msgShowTime);
  }
});

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