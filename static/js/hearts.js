// Checking whether username exists

$(".heartsForm").on("submit", function(event) {

   let recipe_id = $(this).attr("recipe_id");

   let username = $("#usernameInput"+recipe_id).val();
   let recipe_name = $("#recipe_nameInput"+recipe_id).val();
   let cooked = $(".cookedInput"+recipe_id).text();

   $.ajax({
      data: {
         username: username,
         recipe_name: recipe_name,
         cooked: cooked
      },
      type: "POST",
      url: "/main_page/cooked"
   })
   .done(function(data) {
      $("#cookedNumber"+recipe_id).text(data.cooked)
   });

event.preventDefault();
});