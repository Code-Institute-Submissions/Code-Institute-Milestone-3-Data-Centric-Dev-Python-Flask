# Project 3 - Creating cookbook
This project is built for [Code Institute](https://codeinstitute.net/) as a part of _Full Stack Software Development Diploma course_. Project was focused on using semantic HTML5, SASS along with Materialize, Python (Flask), AJAX using jQuery as well as working with noSQL database MongoDB Atlas.

## UX
This is aiming at people who are passionate about cooking and they'd love to create own cookbook.

### User Stories

* As a user I want sing up so that I have own account
* As a user I want to login so that I can see my stuff
* As a user I want to logout so that I can close my app.  
* As a user I want to see my main page as first so that I can easily see my recipies
* As a user I want to modify, remove and add cards to my cookbook app
* As a user I want to see how many times I cook certain meal (assign by hearts)

### Wireframes:  
The following wireframes were created in order to provide a starting point for the website skeleton:

* [mobile device](wireframes/Cookbook_desktop.xd)
* [desktop device](wireframes/Cookbook_mobile.xd)

# Features
The features were used as follow:
* Landing page:
   * Scrolldown to sign up section after clicking on Sign Up button
   * Login button to move you to login section page
   * hamburger menu for mobile screen

* Main page
   * Sort button
   * Add card
   * Cookcards which contains upvote (hearts), edit, remove button and recipe after clicking on image, recipe name or recipe button
   * Paginaition in case when there are more then 5 cookcards

* add/edit page
   * Contain image upload
   * Change name of recipe or cuisine
   * Modifying recipe section by using rich editor

## Technologies Used
I used following technologies for this particular project:
* HTML5
* CSS3
  * [Materialize](https://materializecss.com/)
  * [BEM](http://getbem.com/) - used for cleaner style sheet
* [Python](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* Javascript ([jQuery](https://jquery.com/)) for AJAX
* [CKEditor](https://ckeditor.com/)
* [Adobe Xd](https://www.adobe.com/cz/products/xd.html)
* [VS Studio Code](https://visualstudio.microsoft.com/cs/?rr=https%3A%2F%2Fwww.google.ie%2F)
* [GIMP](https://www.gimp.org/)

## Testing

I tested my website manually and I also executed automated testing.

### Manual Testing

The manual testing was accomplished mainly by using following technologies/tools:

* [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/) - Chrome DevTools is a set of web developer tools built directly into the Google Chrome browser. DevTools can help you edit pages on-the-fly and diagnose problems quickly, which ultimately helps you build better websites, faster.

* Web browers such as:
  * Chrome
  * Opera
  * Mozilla
  * Microsoft Edge
  * Safari

* Devices
  * Desktop
  * Mobile Phone

#### Manual Testing Bugs


* Microsoft Edge:
  * Advanced button lost the darker gray color and looks the same as background
    * fixing: added background color #dddddd
  * `<option value="Prague">The Czech Republic</option>` does not show Prague, but only The Czech Republic.

* Mozilla:
  * Advanced button lost the darker gray color and looks the same as background
    * fixing: added background color #dddddd
  * `<option value="Prague">The Czech Republic</option>` does not show The Czech Republic, but only Prague. 


## Automated Testing
The automate testing was executed by the following tools:

* Chrome Lighthouse

The Lighthouse is an open-source automated tool that audits website for performance, progresssive Web app, accessibility, best practices & SEO. The website current score as follows:

```
> Performance at 82
> Progresssive Web app at 58
> Accessibility at 83
> Best practices at 87
> SEO at 100

the highest score is 100
```

* HTML & CSS validator
  * [HTML validator result](https://validator.w3.org) found one error from line 20 as the pipe key is illegal character in query.
  * [CSS validator result](https://codebeautify.org/cssvalidate) did not find any major error.

## Deployment
The website was deployed on github.
Live version of the website can be found [here](https://tomas-kaiser.github.io/Code-Institute-Milestone-2-Interactive-Frontend-Development/)

## Credits
* Smooth scrolldown effect JS [w3schools](https://www.w3schools.com/howto/howto_css_smooth_scroll.asp#section1)

## Contributing
This repository is a part of project for Code Institute of a Full Stack Software Development course. Therefore, I will most likely not accept pull requests.