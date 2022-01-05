# Pet Events

#### Video Demo: https://youtu.be/etCtZlfmrfU

#### Description:

This project was originally designed to be a way of registering all the events any pet attend in a certain day care
center for pets.

The place my dog usually goes every weekend and some weekdays too is a place where many dogs gather and play all day
long.

The problem is that they have no control whatsoever on what day each dog went there.

My idea was to create a system for this place, so they can register what dog attended what event at what date.

This idea came up the day I requested them the days my dog went there in order to know if what they were charging me was
te correct value.

The "control" they provided me was embarrassing :)

It was a piece of paper with the name of the tutors and any time a dog went there, they would make a mark in front of
the name of the tutor.

But no date, no idea what was the event, nothing.

Given this introduction, I present to you, my project:

The project was divided into 4 parts:

- The customer;
- The pets;
- The events;
- Possible errors.

Starting by the last part implemented, the errors, they are simple layouts handling 3 possible errors:

- In case the user tries to perform something they can't, then this error shall be presented (403);
- In case the user tries to access a page that doesn't exist, then this error shall be presented (404);
- Finally, in the case of an error on server side, then this error shall be presented (500).

For that, it was created a python package inside the project (namely errors), and the __init__.py file is empty.

There is also another file (handlers.py) and in this file those errors are handled. The idea is just to render a
specific template for each case. This way there is always the links available to return home, or any other place in the
system. I show that in the video.

This was the only separated package it was created.

All the other routes in this project is being handled in the file "routes.py". It could also be split into 3 separated
packages, but it wasn't that big to perform the split. In this case I decided to maintain one single file for that.

On "models.py" file there are the classes that represent the tables used for this project. Those classes were necessary
for the pagination. With so many events being listed on home page, I came up with the idea of dividing it into pages, so
it doesn't get tedious scrolling all the way down.

On "helpers.py" file, there are a few scripts that was being repeated on routes file. I decided to create this file to
put there some helper scripts.

On the "__init__.py" file inside the "petevent" folder we have the initial config for this system, such as the variable
that access the database, the import of the routes, and the necessary config for the flask to run.

Inside the templates folder, there are all the pages available on this system. The page that handles customer
registration there is a script that once the user provides the zipcode from the new customer, it automatically fills all
the fields possible, such as the location, the district, the State and the City this person lives.

This script is working for Brazilian addresses only.

The original script for that is available at:
https://viacep.com.br/exemplo/javascript/

So this part of the code I didn't implement myself.

Also, still on the very same template, there are masks implemented on some fields, such as the phone format, or the zip
code format.

The mask implementation was thanks to Igor Escobar:
https://igorescobar.github.io/jQuery-Mask-Plugin/#examples

I downloaded the scripts he provided online and adapted for my project.

Another interesting template is the "event/all_events.html". This is when the user wants all the events to be presented
in one single page. In this case, there is a filter so the user can check the events that were attended by a certain
client (dog), or the events that was given in a certain month.

All the other templates were only html/jinja scripts, and the css part was almost 100% bootstrap.

Everything starts at "run.py" file at the root of the project.
It only imports the app from the "petevent" package and runs the app.

So, to run the app, all you need to do is run the command:

$ python run.py