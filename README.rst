Everything is Trainable
=======================
Trainable is a open source web application for targeted Training control
with focus on cyclists.

Trainable let you define custom trainings goals for which a trainingplan
can be created.
Trainable will stay in the background and anaylse your workout data to give
feedback about your progress on the way to the training goal.

Targeted Training
-----------------
The core of the goal-oriented training is to help the athlete achieve his or
her goals.

Therefor trainable provides some tools for the performanance diagnostics find
the athlets weakness to identify the worthy points where the athlete can
improve. Once the goals are defined trainable let you define your training
plan planning training units in detail. While tracking your workouts you can
link those workouts to the trainingunit and see how well you achieve the
objectives of training unit.

Performanance diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^
Currently Planned:

* Critical Power Tests (CP)
* Aerobic endurance (Steptests to find your heartrate/power at lactate threshold)
* Nice graphics and diagrams

Trainingplan with goals
^^^^^^^^^^^^^^^^^^^^^^^
Currently Planned:

* Google calender integration
* Predefined and custum training units

Workout tracking
^^^^^^^^^^^^^^^^
Trainable uses Strava as its main source for training data. So athlets can
continue to use their favorite tracking software. However trainable provides
some additional fields to get a better option to use trainable as your logbook
for your workouts.

* Distance
* Duration
* Time
* RPE (Borg15)
* Average Hearrate
* Description
* Athlets bio data like rest heartrate,weight or sleep
* External circumstances like weather, wind etc.

Statistics/Evaluation
^^^^^^^^^^^^^^^^^^^^^
Trainable will focus on the analysis of your training plan. Analysis of your
workout is left to strava and other third pary tools. They are very goog at :)
However trainable will give you a good overview of your progress in your
training plan:

Currently Planned:

* Pensum (Duration*Intensity)
* Trainingours (Weekly, Monthly)
* Training focus


Getting Started
---------------

- cd <directory containing this file>

- $venv/bin/python setup.py develop

- $venv/bin/trainable-admin db init

- $venv/bin/pserve development.ini
