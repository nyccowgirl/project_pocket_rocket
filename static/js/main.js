/*jslint node: true */
'use strict';

$(document).ready(() => {

// modifies styling of navbar items for current page

  $('a[href="' + this.location.pathname + '"]').parent().addClass('active');


// $('#discountmodal').on('show.bs.modal', function () {
// http://stackoverflow.com/questions/48239/getting-the-id-of-the-element-that-fired-an-event-using-jquery
//     are we working with "home" or with "profile"?
//     alert("alert Alert");
//     var theButtonCaller = event.target.id;
//     alert("alert Alert");
//     theButtonCaller = theButtonCaller.replace("-btn", "");

//     $(".tab-pane, #myTabs li").removeClass("active");
//     $("#" + theButtonCaller).addClass("active");
//     $("#myTabs li.li-" + theButtonCaller).addClass("active");
// });


// processes like buttons on reviews

  let $like = $('.like');

  function disableLike(results) {
    alert(results);
    location.reload(true);
  }

  function handleClick(evt) {
    evt.preventDefault();
    let formInputs = {
      'review_id': this.id
    };
    $(this).removeClass('.fa-heart-o');
    $(this).addClass('.fa-heart');
    $(this).prop('disabled', true);
    $.post('/like-review', formInputs, disableLike);
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
      location.reload(true);
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
      location.reload(true);
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
    location.reload(true);
  }

  function checkBiz(evt) {
    evt.preventDefault();
    let formInputs = {
      'biz_id': this.id
    };
    $.post('/checkin/<biz-id>', formInputs, checkinMsg);
  }

  $checkIn.on('click', checkBiz);


// search feature on tables in user promotions and redemptions

  $('#myInputAvail').on('keyup', function() {
    var value = $(this).val().toLowerCase();
    $('#myTable tr').filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  $('#myInputRed').on('keyup', function() {
    var value = $(this).val().toLowerCase();
    $('#myTableRed tr').filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  // character count for reviews

  // $('input#input-review').characterCounter();
  // });


});