// Checking whether username exists

$("#singUpForm").on("submit", function(event) {
   $.ajax({
      data: {
         username: $("#username").val(),
         password: $("#password").val()
      },
      type: "POST",
      url: "/landing_page"
   })
   .done(function(data) {
      if (data.error) {
         $("#password").text(data.error).show();
         $("#password").val("");
      }
      else {
         $("#errorAlert").text(data.error).hide();
         window.location.href = "/login";
      }
   });

event.preventDefault();
});