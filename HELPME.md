Hi there 👋

This file serves to make the rest of this repository more readable for everyone and also give a basic overview
of Flask and SQLAlchemy.

As always, you can just chatGPT everything! 😎

## What does each folder/file do?

There are 3 folders:

- views
- models
- instance

### Views

We'll mainly be working in `routes.py`
This folder contains all the endpoints of our API.
Essentially, for each header in the API, `@api.route('/{smth}')` is a decorator that tells Flask to call the function below it when the API is hit at that endpoint.

Like any other function, you can have arguments that pass through. (i.e. see `@api.route('calendar/<user>)`)

APIs usually have parameters that are passed through the URL. You can access these parameters using `request.args.get('param')` or `request.args['param']`.

Normally you'd want to type check the parameters with a bunch of `if` statements.

Bringing it all together you have something like:

`http://localhost:5000/calendar?user=1`

```python
@api.route('/calendar')
def get_calendar():
    user = request.args.get('user')
    if not user:
        return jsonify({'error': 'No user provided'}), 400
    # Do something with the user
    return jsonify({'calendar': 'calendar'}), 200
```

For any return function, you will need to return a JSON object, and a status code. You can wrap any dictionary in `jsonify()` and pass in the status code as the second argument.

For each function, you'll want to interact with the database, this is where the `models` folder comes in.

### Models

This folder contains the structure of the database. As you can see, the table is initialised like a class, and each class variable is a column in the table. You can also define helper functions, and also have relationships between tables like in SQL, have a look at the SQLAlchemy documentation or chatGPT for more info.

In short, once the table is defined, the database is created and the data is stored in the db.sqlite file in the `instance` folder. Whenever you change anything in the models, make sure to delete the db.sqlite file and restart the server.

To interact with the database there are a few functions you can use:

- `session.add()`: Add a new row to the table
- `session.query()`: Query the table, you can also filter, order, and limit the query, more info in the SQLAlchemy documentation, these functions will work similarly to how React components work; they are chainable. i.e. you can do `session.query().filter().order_by().limit()` which filters based on a certain true/false condition, orders the results, and limits the number of results returned.
- `session.delete()`: Delete a row from the table
- `session.commit()`: Commit the changes to the database; just like git
