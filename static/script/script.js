async function verifyUserAddress(evt) {
  evt.preventDefault();
  if ($('#submit-form')) {
    $('#submit-form').remove();
  }
  if ($('#cancel-verify')) {
    $('#cancel-verify').remove();
  }
  $('#verify-user-address').html('');
  formData = {
    street_address: $('#street_address').val(),
    city: $('#city').val(),
    state_id: $('#state_id').val(),
    zip_code: $('#zip_code').val(),
  };
  res = await axios.post('/verify-address', formData);
  data = res.data;

  if (data.errors.error) {
    $('#verify-user-address').html(
      '<div class="d-flex flex-column align-items-center"><span class="text-danger">Invalid Address - Please try again.</span></div>'
    );
  } else {
    const verifiedStreetAddress = data.response.verified_street_address;
    const verifiedCity = data.response.verified_city;
    const verifiedState = data.response.verified_state;
    const verifiedZipCode = data.response.verified_zip_code;
    $('#verify-btn').html('');
    $('#street_address').val(verifiedStreetAddress);
    $('#city').val(verifiedCity);
    $(`#state_id option[value="${verifiedState}"]`).attr(
      'selected',
      'selected'
    );
    $('#zip_code').val(verifiedZipCode);
    $('#street_address').attr('readonly', 'readonly');
    $('#city').attr('readonly', 'readonly');
    $('#state_id').prop('disabled', true);
    $('#zip_code').attr('readonly', 'readonly');
    $('#verify-user-address').html(
      `<div class="d-flex flex-column align-items-center text-center"><b><span class="text-primary">Please confirm that verified address in form is correct</span></b><div class="mt-1">Street Address: ${verifiedStreetAddress}<br>City: ${verifiedCity} State: ${verifiedState} Zip: ${verifiedZipCode}</div>`
    );
    $('#verify-btn').html(
      '<div class="d-flex flex-column align-items-center"><button id="submit-form" class="btn btn-success btn-large mt-2">Confirm and Submit</button><a class="btn btn-danger btn-large mt-2" id="cancel-verify">Cancel and Make Changes</a></div>'
    );
    $('#cancel-verify').on('click', cancelVerify);
  }
}

// Address Data from https://github.com/EthanRBrown/rrad
async function generateRandomAddress() {
  const origStreetAddress = $('#street_address').val();
  const origCity = $('#city').val();
  const origStateId = $('#state_id').val();
  const origZipCode = $('#zip_code').val();
  const addresses = randAddressData.addresses;
  const randomAddress = addresses[Math.floor(Math.random() * addresses.length)];
  const res = await axios.post('/verify-random-address', {
    street1: randomAddress.address1,
    city: randomAddress.city,
    state: randomAddress.state,
    zip: randomAddress.postalCode,
  });
  data = res.data;
  if (data.errors.error) {
    $('#verify-user-address').html(
      '<div class="d-flex flex-column align-items-center"><span class="text-danger">Invalid Address - Please try again.</span></div>'
    );
  } else {
    const verifiedStreetAddress = data.response.verified_street_address;
    const verifiedCity = data.response.verified_city;
    const verifiedState = data.response.verified_state;
    const verifiedZipCode = data.response.verified_zip_code;
    $('#verify-btn').html('');
    $('#street_address').val(verifiedStreetAddress);
    $('#city').val(verifiedCity);
    $(`#state_id option[value="${verifiedState}"]`).attr(
      'selected',
      'selected'
    );
    $('#zip_code').val(verifiedZipCode);
    $('#street_address').attr('readonly', 'readonly');
    $('#city').attr('readonly', 'readonly');
    $('#state_id').prop('disabled', true);
    $('#zip_code').attr('readonly', 'readonly');
    $('#verify-user-address').html(
      `<div class="d-flex flex-column align-items-center text-center"><b><span class="text-primary">Please confirm that verified address in form is correct</span></b><div class="mt-1">Street Address: ${verifiedStreetAddress}<br>City: ${verifiedCity} State: ${verifiedState} Zip: ${verifiedZipCode}</div>`
    );
    $('#verify-btn').html(
      '<div class="d-flex flex-column align-items-center"><button id="submit-form" class="btn btn-success btn-large mt-2">Confirm and Submit</button><a class="btn btn-danger btn-large mt-2" id="cancel-verify">Cancel and Make Changes</a></div>'
    );
    $('#cancel-verify').on('click', () => {
      cancelVerify(origStreetAddress, origCity, origStateId, origZipCode);
    });
  }
}

function cancelVerify(origStreetAddress, origCity, origStateId, origZipCode) {
  $('#submit-form').remove();
  $('#street_address').prop('readonly', false);
  $('#city').prop('readonly', false);
  $('#state_id').prop('disabled', false);
  $('#zip_code').prop('readonly', false);
  $('#street_address').val(origStreetAddress);
  $('#city').val(origCity);
  $('#state_id').val(origStateId);
  $('#zip_code').val(origZipCode);
  $('#cancel-verify').remove();
  $('#verify-user-address').html('');
  $('#verify-btn').html(
    '<div class="d-flex flex-column align-items-center"><a class="btn btn-primary btn-large mt-2" id="verify-user">Verify Address</a><a class="btn btn-success btn-large mt-2" id="random-address">Generate Random Address</a></div>'
  );
}

$('body').on('click', '#random-address', generateRandomAddress);
$('body').on('click', '#verify-user', verifyUserAddress);

$('#user-form').on('submit', function () {
  $('input, select').prop('disabled', false);
});

function confirmDelete() {
  $('#user-buttons').html(
    '<div class="d-flex flex-column align-items-center text-center"><b><span class="text-danger">Are you sure? If so, please click confirm to delete</span></b></div><div class="mt-1"><button class="btn btn-success mx-1 btn-lg" id="confirm-delete">Confirm</button></a><button class="btn btn-danger mx-1 btn-lg" id="cancel-delete">Cancel</button></div>'
  );
}

function deleteUser() {
  $('#delete-form').submit();
}

function cancelDelete() {
  const username = $('#username').text();
  $('#user-buttons').html(
    `<a href="/users/${username}/edit"><button class="btn btn-primary mx-1 btn-lg">Edit</button></a><button class="btn btn-danger mt-2 btn-lg d-inline" id="delete-btn">Delete</button>`
  );
}

$('body').on('click', '#delete-btn', confirmDelete);
$('body').on('click', '#confirm-delete', deleteUser);
$('body').on('click', '#cancel-delete', cancelDelete);
$('body').on('click', '#submit-form', () => {
  $('#user-form').submit();
});