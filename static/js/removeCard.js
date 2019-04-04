// Checking whether username exists

$(".removeCard").on("submit", function(event) {

   let recipe_id = $(this).attr("recipe_id");

   let username = $("#usernameInput"+recipe_id).val();
   let recipe_name = $("#recipe_nameInput"+recipe_id).val();
   let img_name = $("#imgInput"+recipe_id).val();

   $.ajax({
      data: {
         username: username,
         recipe_name: recipe_name,
         img_name: img_name
      },
      type: "POST",
      url: "/main_page/remove_foodcard"
   })
   .done(function(data) {
      $("#name"+username).html(data);
      console.log("Card was removed")
   });

event.preventDefault();
});