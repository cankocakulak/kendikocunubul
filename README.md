This little Web App approach is constructed via Flask, Python, JavaScript

The overall structure:

-User answers the following questions which pop are seen on the screeen:
  *Question answers are picked from a list. Some of the questions have integer values, on the other hand, some have string values

-Backend part:
  There is an "Option" Class in the backend part in order to keep the data of the options and match them with user preferences. In this web app, the options are "Consultants" and
  their answers to the given questions are already stored. (Currently there are 3 option but it will increase)
  The options have a variable named 'score', which is set to 0 in the beginning.
  *For the integer and string questions, code checks for every option's answer to that specific question and according to a condition and performs an addition to the score if the condition is met.
  In the end, the option with the most score is shown to the user via another html template page
  Along with the option itself, also the matching parts are shown to the user.

-Considerations:
  *Options which are out of stock wont be shown to the user at all
  *"Suggest me another" button shows second best option 
  *First string question is cruical, meaning that the user and the option answer should match, otherwise the option wont be shown to the user.
  
