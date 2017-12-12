/*jslint node: true */
'use strict';

$(document).ready(() => {

// modifies styling of navbar items for current page

  $('a[href="' + this.location.pathname + '"]').parent().addClass('active');


  function msgReload(results) {
    if (results.code === 'danger') {
      alert(results.msg);
    } else {
      alert(results.msg);

    }
    location.reload('/');
  }

  function displayMsg(results) {
    alert(results.msg);
  }

  // function msgReloadError(results) {
  //   if (results.code === 'error') {
  //     alert(results.msg);
  //   } else {
  //     alert(results.msg);
  //     location.reload(true);
  //   }
  // }


// processes like buttons on reviews

  let $like = $('.like');

  function handleClick(evt) {
    evt.preventDefault();
    let formInputs = {
      'review_id': this.id
    };
    $(this).removeClass('.fa-heart-o');
    $(this).addClass('.fa-heart');
    $(this).attr('style', 'color:#880e4f');
    $(this).prop('disabled', true);
    $.post('/like-review', formInputs, msgReload);
  }

  $like.on('click', handleClick);


// processes friend request

  let $friend = $('#modalAddFriend');

  function sendFriend(evt) {
    evt.preventDefault();
    let formInputs = {
      'friend_email': $('#friend-email').val()
    };
    $.post('/add-friend', formInputs, displayMsg);
  }

  $friend.on('submit', sendFriend);


// processes claim of biz

  let $claim = $('.claim-biz');

  function claimBiz(evt) {
    evt.preventDefault();
    let formInputs = {
      'biz_id': this.id
    };
    $.post('/claim-biz/<biz-id>', formInputs, msgReload);
  }

  $claim.on('click', claimBiz);


// processes user info edits

  let $userEdit = $('#modalEdit');

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
      $.post('/edit-user', formInputs, msgReload);
    } else {
      alert('The password you entered does not match.');
    }
  }

  $userEdit.on('submit', editUser);

  // TO DO: Use .change to check email, etc. first b/f going to submitting


// processes check ins into biz

  let $checkIn = $('.check-in');

  function checkBiz(evt) {
    evt.preventDefault();
    let formInputs = {
      'biz_id': this.id
    };
    $(this).prop('disabled', true);
    $.post('/checkin/<biz-id>', formInputs, displayMsg);
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


// redeem promotions

  let $redPromo = $('.redeem')
  let $redPromoNew = $('.redeem-new')

  function redeemPromo(evt) {
    evt.preventDefault();
    let formInputs = {
      'userpromo_id': this.id
    };
    $(this).prop('disabled', true);
    $.post('/red-userpromo', formInputs, msgReload);
  }

  $redPromo.on('click', redeemPromo);

  function redeemPromoNew(evt) {
    evt.preventDefault();
    let formInputs = {
      'promo_id': this.id
    };
    $(this).prop('disabled', true);
    $.post('/red-promo', formInputs, msgReload);
  }

  $redPromoNew.on('click', redeemPromoNew);

});