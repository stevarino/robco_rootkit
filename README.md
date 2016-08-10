# robco_rootkit
Django project for the for the hacking of Robco terminals in the video game series Fallout by Bethesda.

# Installation
This project requires the django project to be installed. It has been tested on using Python 2 and Python 3 as well as Django 1.9 and 1.10.

# API
This project is intended as a demonstration of utilizing Django as a JSON API.  The processing is simple enough to not require an API, but I would like to see this project utilized in other mediums such as native apps.

All requests should be JSON objects posted to the /api URL. The service will respond with a response object as documented below.

## Request Object Syntax

```EBNF
request = "{" "'words'" ":" "[" [ word  { "," word } ] "]"  ["'feedback'" ":" "[" [ feedback { "," feedback  } ] "]" ]  "}" .

feedback = "{" "'word'" ":" word "," "'feedback'" ":" feedback_score "}" .
```

![EBNF Request Diagram](./website/static/website/docs/request.png)

![EBNF Request Feedback Diagram](./website/static/website/docs/feedback.png)

## Response Object Syntax

```EBNF
response = "{" "'valid'" ":" ( true | false ) ","  [ "'message'" ":" message "," ]  "'words'" ":" "[" [ word_response {"," word_response} ] "]"  "}" .

word_response = "{" "'word'" ":" word ","  "'valid'" ":" ("true" | "false") ","  "'position'" ":" position ","  [ "'score'" ":" score "," ]  [ "'feedback'" ":" feedback_score ]  "}" .
```

![EBNF Response Diagram](./website/static/website/docs/response.png)

![EBNF Word Response Diagram](./website/static/website/docs/word_response.png)
