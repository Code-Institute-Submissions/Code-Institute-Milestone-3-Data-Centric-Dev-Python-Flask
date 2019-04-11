// Pagination

$(".pagination-btn").on("click", function(event) {

   let numberOfPag = $(this).text();
   let username = $(".username").attr("data-name");

   $.ajax({
      data: {
         page_number: numberOfPag
      },
      type: "POST",
      url: `/main_page/${username}`
   })
   .done(function(data) {
      $("#name"+username).html(data);
   });

   event.preventDefault();
});


// pagination forward arrow
$(".pagination-arrow-forward").on("click", function(event) {

   let numberOfPag = $(".active").text();
   numberOfPag++;
   let username = $(".username").attr("data-name");

   $.ajax({
      data: {
         page_number: numberOfPag
      },
      type: "POST",
      url: `/main_page/${username}`
   })
   .done(function(data) {
      $("#name"+username).html(data);
   });

   event.preventDefault();
});


// pagination backward arrow
$(".pagination-arrow-backward").on("click", function(event) {

   let numberOfPag = $(".active").text();
   numberOfPag--;
   let username = $(".username").attr("data-name");

   $.ajax({
      data: {
         page_number: numberOfPag
      },
      type: "POST",
      url: `/main_page/${username}`
   })
   .done(function(data) {
      $("#name"+username).html(data);
   });

   event.preventDefault();
});