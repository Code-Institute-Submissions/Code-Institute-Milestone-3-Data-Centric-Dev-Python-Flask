// Pagination

$(".pagination-btn").on("click", function(event) {

   let numberOfPag = $(this).text();
   let username = $(".username").attr("data-name");

   console.log("Id username: " + username);
   console.log("number of clicked: " + numberOfPag);

   $.ajax({
      data: {
         page_number: numberOfPag
      },
      type: "POST",
      url: `/main_page/${username}`
   })
   .done(function(data) {
      $("#name"+username).html(data);

      console.log("Data returned here:")
      console.log(data);
   });

   event.preventDefault();
});


// pagination forward arrow
$(".pagination-arrow-forward").on("click", function(event) {

   let numberOfPag = $(".active").text();
   numberOfPag++;
   let username = $(".username").attr("data-name");

   console.log("number of clicked: " + numberOfPag);  
   console.log("Id username: " + username);

   $.ajax({
      data: {
         page_number: numberOfPag
      },
      type: "POST",
      url: `/main_page/${username}`
   })
   .done(function(data) {
      $("#name"+username).html(data);

      console.log("Data returned here:")
     // console.log(data);
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