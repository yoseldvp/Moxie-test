# Welcome to my not-so-beautiful API Backend for Medspa Management Solution

If you are reading this, you have the terrible fortune to be evaluating my black-hole API solution to administrate Medspas. Here I tried to capture all the passed requirements into a almost simplistic solution of a RESTFull API Endpoint.

The selected stack is FastAPI and SQLModel to create this application. I decided to use FastAPI to silently support and highlight a fellow Colmbian developer, which created both frameworks. **Boy, I was wrong!!!**. It might be tempting to get a lot of things for free, but the documentation of a project is key to succeed. So i found myself going over and over and over again the docs to find solutions to the questions I had.

FastAPI has gotten a lot of attention lately. It has great features, like the almost-free documentation of the API methods and the testing ground. But it requires experience to be able to master it. My first mistake of this test was choosing a tool that seemed cool, but I had 0 experience with it. The result is a lot of tears and wasted hours.

In complete honesty, it took me way more than 4 hours to complete the test. However, I'm happy with the process. I learned some new things, and coded for a good amount of time, which is always going to be entertaining.

Enough chit-chat. Lets get to the goods.

## How to run the app

As mentioned before, this app is created using Python 3.13 and FastAPI. So make sure to have the proper python version installed.

0. Checkout this code and go to the root of the repo. :)

1. First create a virtual environment:

```python3 -m venv .env```

2. Activate your virtual env:

```source .env/bin/activate```

3. Install all the dependencies:

```pip3 install -r requirements.txt```

4. Install postgres and/or create a schema for the app.

5. Copy the `.env.example.` file to `.env` and fill it with your DB details.

6. Create the base schema: I created a cli tool to create/drop the base schema. I started wanting to show-off. Also, I have a fixation with CLI tools. That said, I created a "Production Ready" version of the schema. **So please use the `schema.sql` to create the app data model instead.**

7. Import the base data: Open up any SQL Tool of your choice. Run `data.sql` to load all the base Service hierarchy data. I also wanted to add this step to the CLI tool, but _ain't nobody got time for that_
![ain't nobody got time for that](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXo2OGZrb203eWhhNnpndm5tYnFrbTBrZ2d2ZW55bWd5cmxwY3V1ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bWM2eWYfN3r20/giphy.gif)

8. Run the API:

```fastapi dev main.py```

9. Go to `http://127.0.0.1:8000/docs` and have some fun. You initially will have to create a new Medspa and associate some services with it. Remember that to associate services, you must have to specify the price and the duration for each association.
