/*jslint node: true */
'use strict';

$(document).ready(() => {

// modifies styling of navbar items for current page

  $('a[href="' + this.location.pathname + '"]').parent().addClass('active');

// processes log-in and password reset modal

  // function checkEmail(result) {
  //   if (result === False) {
  //     alert('User name or email does not exist. Please check your input or register.');
  //   } else if (result === True) {
  //     alert('A link has been sent to your email to reset your password.');
  //     location.reload('/pword-reset');
      // FIXME: send url to email to click to take to password reset form
  //   } else {
  //     alert('Please try again.');
  //   }
  // }

  // function sendEmail(evt) {
  //   let formInputs = {
  //     'user-input': $('#email-lost').val()
  //   };
  //   $.get('/email-check', checkEmail);
    // TO DO: send link to email to reset password
  // }

  // function register(evt) {
  //   let formInputs = {
  //     'fname': $('#fname').val(),
  //     'lname': $('#lname').val(),
  //     'username': $('#username').val(),
  //     'email': $('#email-reg').val(),
  //     'pword': $('#pword-reg').val(),
  //     'bday': $('#bday').val(),
  //     'biz': $('biz').val(),
  //     'pic': $('#user-pic').files
  //   };
  //   $.post('/register'), formInputs, displayMsg);
  // }

  // function displayMsg(results) {
  //   if (results.code === 'error') {
  //       alert(results.msg);
  //   } else {
  //       alert(results.msg);
  //   }
  //   location.reload('/');
  // }

  // function logIn(evt) {
  //   let formInputs = {
  //     'user-input': $('#user-input').val(),
  //     'pword': $('#pword').val()
  //   };
  //   $.post('/login', formInputs, displayMsg);
  // }


  // $(function() {
  //   let $formLogin = $('#login-form');
  //   let $formLost = $('#lost-form');
  //   let $divForms = $('#div-forms');
  //   let $modalAnimateTime = 300;
  //   let $msgAnimateTime = 150;
  //   let $msgShowTime = 2000;

  //   $('form').on('submit', function (evt) {
  //     evt.preventDefault();
  //       switch(this.id) {
  //           case 'login-form':

  //               logIn(evt);

  //               break;
  //           case "lost-form":
  //               if (!$('#lost_email')) {
  //                 alert('Please input a user name or email.');
  //                 break;
  //               };
  //               sendEmail(evt);

  //               break;
  //           default:
  //       }
  //   });
  // });

  // $('#login_lost_btn').on('click', function () { modalAnimate($formLogin, $formLost); });
  // $('#lost_login_btn').on('click', function () { modalAnimate($formLost, $formLogin); });

  // function modalAnimate ($oldForm, $newForm) {
  //     var $oldH = $oldForm.height();
  //     var $newH = $newForm.height();
  //     $divForms.css("height",$oldH);
  //     $oldForm.fadeToggle($modalAnimateTime, function(){
  //         $divForms.animate({height: $newH}, $modalAnimateTime, function(){
  //             $newForm.fadeToggle($modalAnimateTime);
  //         });
  //     });
  // }

  // function msgFade ($msgId, $msgText) {
  //     $msgId.fadeOut($msgAnimateTime, function() {
  //         $(this).text($msgText).fadeIn($msgAnimateTime);
  //     });
  // }

  // function processForm(evt) {
  //   $('#modalLRForm .nav-link').button('toggle').addClass('active');
  //   $('form').on('submit', function(evt) {
  //     evt.preventDefault();
  //     console.log(evt);
  //     debugger;
  //   let formInputs = new formData(this);
  //     console.log(formInputs);
  //     switch(this.id) {
  //       case 'login':
  //         // logIn(evt);
  //         $.post('/login', formInputs, displayMsg);
  //         break;
  //       case 'registration':
  //         if $('#pword-reg').val() != $('#pword-rep').val()) {
  //             alert('The password does not match. Try again.')
  //         } else {
  //         // register(evt);
  //         $.post('/register', formInputs, displayMsg);
  //         };
  //         break;
  //       case 'reset-pword':
  //         if (!$('#email-lost')) {
  //           alert('Please input a user name or email.');
  //           break;
  //         };
  //         sendEmail(evt);
  //         break;
  //       default:
  //         console.log('Something is broken. Check back later!');
  //     }
  //   });
  // }


  // $('#modalLRForm').on('click', processForm);


// $('#discountmodal').on('show.bs.modal', function () {
// http://stackoverflow.com/questions/48239/getting-the-id-of-the-element-that-fired-an-event-using-jquery
    // are we working with "home" or with "profile"?
    // alert("alert Alert");
    // var theButtonCaller = event.target.id;
    // alert("alert Alert");
//     theButtonCaller = theButtonCaller.replace("-btn", "");

//     $(".tab-pane, #myTabs li").removeClass("active");
//     $("#" + theButtonCaller).addClass("active");
//     $("#myTabs li.li-" + theButtonCaller).addClass("active");
// });


// processes like buttons on reviews

  let $like = $('.like');

  function disableLike(results) {
    alert(results);

  }

  function handleClick(evt) {
    evt.preventDefault();
    let formInputs = {
      'review_id': this.id
    };
    $.post('/like-review', formInputs, disableLike);
    $(this).prop('disabled', true);
    $(this).removeClass('.fa-heart-o');
    $(this).addClass('.fa-heart');
  }
// FIXME: Add in remove and add class for the solid heart shape - need to test

  $like.on('click', handleClick);


// processes friend request

  let $friend = $('#modalAddFriend');

  function friendMsg(results) {
    alert(results);
  }

  function sendFriend(evt) {
    evt.preventDefault();
    let formInputs = {
      'friend_email': $('#friend-email').val()
    };
    $.post('/add-friend', formInputs, friendMsg);
  }

  $friend.on('submit', sendFriend);


// processes claim of biz

  let $claim = $('.claim-biz');

  function claimMsg(results) {
    if (results.code === 'error') {
      alert(results.msg);
    } else {
      alert(results.msg);
      location.reload('/business-profile/<biz_name>');
    }
  }

  function claimBiz(evt) {
    evt.preventDefault();
    let formInputs = {
      'biz_id': this.id
    };
    $.post('/claim-biz/<biz-id>', formInputs, claimMsg);
  }

  $claim.on('click', claimBiz);


// processes user info edits

  let $userEdit = $('#modalEdit');

  function editMsg(results) {
    if (results.code === 'error') {
      alert(results.msg);
    } else {
      alert(results.msg);
      location.reload('/user-profile');
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
      alert('The password you entered does not match.');
    }
  }

  $userEdit.on('submit', editUser);

  // TO DO: Use .change to check email, etc. first b/f going to submitting


// processes check ins into biz

  let $checkIn = $('.check-in');

  function checkinMsg(results) {
    alert(results.msg);
    location.reload('/business-profile/<biz_name>');
  }

  function checkBiz(evt) {
    evt.preventDefault();
    let formInputs = {
      'biz_id': this.id
    };
    $.post('/checkin/<biz-id>', formInputs, checkinMsg);
  }

  $checkIn.on('click', checkBiz);


});