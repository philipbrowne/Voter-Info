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
  console.log(data);

  if (data.errors.error) {
    $('#verify-user-address').html(
      '<span class="text-danger">Invalid Address - Please try again.</span>'
    );
  } else {
    const verifiedStreetAddress = data.response.verified_street_address;
    const verifiedCity = data.response.verified_city;
    const verifiedState = data.response.verified_state;
    const verifiedZipCode = data.response.verified_zip_code;
    $('#verify-btn').html('');
    $('#street_address').val(verifiedStreetAddress);
    $('#city').val(verifiedCity);
    $(`#state_id option[value="${verifiedState}"]`).attr('selected', 'selected');
    $('#zip_code').val(verifiedZipCode);
    $('#street_address').attr('readonly', 'readonly');
    $('#city').attr('readonly', 'readonly');
    $('#state_id').prop('disabled', true);
    $('#zip_code').attr('readonly', 'readonly');
    $('#verify-user-address').html(
      `<b><span class="text-primary">Please confirm if verified address in form is correct</span></b><div class="mt-1">Street Address: ${verifiedStreetAddress}<br>City: ${verifiedCity} State: ${verifiedState} Zip: ${verifiedZipCode}`
    );
    $('#verify-btn').html(
      '<button id="submit-form" class="btn btn-success btn-large mt-2">Confirm and Submit</button><br><a class="btn btn-danger btn-large mt-2" id="cancel-verify">Cancel and Make Changes</a>'
    );
    $('#cancel-verify').on('click', cancelVerify);
  }
}

// https://github.com/EthanRBrown/rrad
async function generateRandomAddress() {
  const addresses = randAddressData.addresses;
  const randomAddress = addresses[Math.floor(Math.random() * addresses.length)];
  const fullAddress = `${randomAddress.address1} ${randomAddress.city} ${randomAddress.state} ${randomAddress.postalCode}`;
  const res = await axios.post('/verify-random-address', {
    full_address: fullAddress,
  });
  data = res.data;
  if (data.errors.error) {
    $('#verify-user-address').html(
      '<span class="text-danger">Invalid Address - Please try again.</span>'
    );
  } else {
    const verifiedStreetAddress = data.response.verified_street_address;
    const verifiedCity = data.response.verified_city;
    const verifiedState = data.response.verified_state;
    const verifiedZipCode = data.response.verified_zip_code;
    $('#verify-btn').html('');
    $('#street_address').val(verifiedStreetAddress);
    $('#city').val(verifiedCity);
    $(`#state_id option[value="${verifiedState}"]`).attr('selected', 'selected');
    $('#zip_code').val(verifiedZipCode);
    $('#street_address').attr('readonly', 'readonly');
    $('#city').attr('readonly', 'readonly');
    $('#state_id').prop('disabled', true);
    $('#zip_code').attr('readonly', 'readonly');
    $('#verify-user-address').html(
      `<b><span class="text-primary">Please confirm if verified address in form is correct</span></b><div class="mt-1">Street Address: ${verifiedStreetAddress}<br>City: ${verifiedCity} State: ${verifiedState} Zip: ${verifiedZipCode}`
    );
    $('#verify-btn').html(
      '<button id="submit-form" class="btn btn-success btn-large mt-2">Confirm and Submit</button><br><a class="btn btn-danger btn-large mt-2" id="cancel-verify">Cancel and Make Changes</a>'
    );
    $('#cancel-verify').on('click', cancelVerify);
  }
}

function cancelVerify() {
  $('#submit-form').remove();
  $('#street_address').prop('readonly', false);
  $('#city').prop('readonly', false);
  $('#state_id').prop('disabled', false);
  $('#zip_code').prop('readonly', false);
  $('#cancel-verify').remove();
  $('#verify-user-address').html('');
  $('#verify-btn').html(
    '<a class="btn btn-primary btn-large mt-2" id="verify-user">Verify Address</a><a class="btn btn-success btn-large mt-2 mx-2" id="random-address">Generate Random Address</a>'
  );
}

$('body').on('click', '#random-address', generateRandomAddress);
$('body').on('click', '#verify-user', verifyUserAddress);

$('#user-form').on('submit', function () {
  $('input, select').prop('disabled', false);
});
