
function checkPasswordMatch() {
    let password = $("#password").val();
    let confirmPassword = $("#confirm_password").val();

    $(':button[type="submit"]').prop('disabled', false);

    if (password !== confirmPassword) {
        $("#message").html("Hasła nie pasują do siebie!").css('color', 'red');
        $(':button[type="submit"]').prop('disabled', true);
    }
    else
        $("#message").html("Hasła się zgadzają.").css('color', 'green');

}

$(document).ready(function () {
   $("#password, #confirm_password").keyup(checkPasswordMatch);


});