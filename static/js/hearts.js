// Checking whether username exists

$(".btn-heart").on("click", function(event) {

   let recipe_id = $(this).attr("recipe_id");

   let username = $("#usernameInput"+recipe_id).val();
   let recipe_name = $("#recipe_nameInput"+recipe_id).val();
   let cooked = $(".cookedInput"+recipe_id).text();
   let currentPage = $(".active").text();

   $.ajax({
      data: {
         username: username,
         recipe_name: recipe_name,
         cooked: cooked,
         current_page: currentPage
      },
      type: "POST",
      url: "/main_page/cooked"
   })
   .done(function(data) {
      $("#name"+username).html(data);
   });

event.preventDefault();
});