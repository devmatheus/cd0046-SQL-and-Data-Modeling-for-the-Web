window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

window.addEventListener('DOMContentLoaded', function () {
  $('#phone').mask('000-000-0000');

  $('#genres').select2();

  $(document).on('change', '#state', function () {
    let stateCode = $(this).val();
    $.ajax({
      url: "/cities",
      data: {state_code: stateCode},
      success: function (data) {
        let cityField = $("#city");
        cityField.empty();
        $.each(data, function (key, value) {
          cityField.append("<option value='" + key + "'>" + value + "</option>");
        });
      }
    });
  });

  $('#state').trigger('change');
  
  $(document).on('click', '.delete-venue', function () {
    let id = $(this).data('id');
    $.ajax({
      url: '/venues/' + id,
      type: 'DELETE',
      success: function (result) {
        if (result.success) {
          window.location.href = '/';
        } else {
          window.location.reload();
        }
      }
    });
  });
});
