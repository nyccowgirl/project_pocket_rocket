/*jslint node: true */
'use strict';

$(document).ready(() => {

// modifies styling of navbar items for current page

  $('a[href="' + this.location.pathname + '"]').parent().addClass('active');

// processes log-in and password reset modal

  function checkEmail(result) {
    if (result === False) {
      toaster.error('User name or email does not exist. Please check your input or register.', 'BUDdy warning');
    } else if (result === True) {
      toaster['unique']('A link has been sent to your email to reset your password.');
    } else {
      toaster['unique']('Please try again.');
    }
  }

  function sendEmail(evt) {
    let formInputs = {
      'user-input': $('#lost_email').val()
    };
    $.get('/pword-reset', checkEmail);
    // TO DO: send link to email to reset password
  }

  function displayMsg(results) {
    if (results.code === 'error') {
        toaster.error(results.msg, 'BUDdy warning');
    } else {
        toaster.success(results.msg, 'Welcome back!');
    };
    location.reload('/');
  }

  function logIn(evt) {
    let formInputs = {
      'user-input': $('#login_username').val(),
      'pword': $('#login_password').val()
    };
    $.post('/login', formInputs, displayMsg);
  }


  $(function() {
    let $formLogin = $('#login-form');
    let $formLost = $('#lost-form');
    let $divForms = $('#div-forms');
    let $modalAnimateTime = 300;
    let $msgAnimateTime = 150;
    let $msgShowTime = 2000;

    $('form').on('submit', function (evt) {
      evt.preventDefault();
        switch(this.id) {
            case 'login-form':

                logIn(evt);

                break;
            case "lost-form":
                if (!$('#lost_email')) {
                  toaster.error('Please input a user name or email.', 'Did you forget something?');
                  break;
                };
                sendEmail(evt);

                break;
            default:
        }
    });
  });

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

// processes like buttons on reviews

  let $like = $('.like');

  function disableLike(results) {
    toaster['unique'](results);
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


// processes friend request

  let $friend = $('#modalAddFriend');

  function friendMsg(results) {
    toaster['unique'](results);
  }

  function sendFriend(evt) {
    evt.preventDefault();
    debugger;
    console.log($('#friend-email').val());
    let formInputs = {
      'friend_email': $('#friend-email').val()
    };
    $.post('/add-friend', formInputs, friendMsg);
  }

  $friend.on('submit', sendFriend);

// processes user info edits

  let $userEdit = $('#modalEdit');

  function editMsg(results) {
    if (results.code === 'error') {
      toaster.error(results.msg);
    } else {
      toaster.success(results.msg);
    }
  }

  function editUser(evt) {
    evt.preventDefault();
    let pword = $('#form18').val();
    let dupPword = $('#form19').val();
    if (pword == dupPword) {
      let formInputs = {
        'fname': $('#form15').val(),
        'lname': $('#form16').val(),
        'email': $('#form17').val(),
        'pword': $('#form18').val(),
        'user_pic': $('#form20').val(),
        'biz_acct': $('#form8').val()
      };
      $.post('/edit-user', formInputs, editMsg);
    } else {
      toaster.error('The password you entered does not match.');
    }
  }

  $userEdit.on('submit', editUser);


// flipcard on user's friend page
  $('.flip-card').on('click', function() {
    $(this).classList.toggle('flipped');
  });

  // $('#myCard').bind({
  //   click: function() {
  //       $('.flip-card .flip-container .flipper').toggleClass('flip');
  //   },
  //   mouseleave: function() {
  //       $('.flip-card .flip-container .flipper').toggleClass('flip');
  //   }
  // });

});