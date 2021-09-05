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
    state: $('#state').val(),
    zip_code: $('#zip_code').val(),
  };
  if ($('#apartment_number').val() !== '') {
    formData['apartment_number'] = $('#apartment_number').val();
  }
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
    $(`#state option[value="${verifiedState}"]`).attr('selected', 'selected');
    $('#zip_code').val(verifiedZipCode);
    $('#street_address').attr('readonly', 'readonly');
    $('#city').attr('readonly', 'readonly');
    $('#state').prop('disabled', true);
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
  $('#state').prop('disabled', false);
  $('#zip_code').prop('readonly', false);
  $('#cancel-verify').remove();
  $('#verify-user-address').html('');
  $('#verify-btn').html(
    '<a class="btn btn-primary btn-large" id="verify-user">Verify Address</a>'
  );
}

$('body').on('click', '#verify-user', verifyUserAddress);

$('#user-form').on('submit', function () {
  $('input, select').prop('disabled', false);
});
