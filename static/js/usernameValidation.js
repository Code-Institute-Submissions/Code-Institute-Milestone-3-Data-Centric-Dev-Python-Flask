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
         console.log("Error")
         $("#errorAlert").text(data.error).show();
         $("#password").val("");
      }
      else {
         console.log("Noooo Error")
         $("#errorAlert").text(data.error).hide();
         window.location.href = "/login";
      }
   });

event.preventDefault();
});