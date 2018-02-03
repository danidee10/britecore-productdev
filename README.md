# britecore-productdev
This implementation uses Flask and PostgreSQL so make sure you have PostgreSQL installed before you proceed

The Frontend is an SPA built with `Vue.js` and `vue-router` for navigation.

## Setup the frontend app

First install the dependencies from npm with:

```bash
npm install
```

Bundle the Vue app all it's dependencies with

```bash
npm run build
```

This creates a new folder containing the `index.html` page and all the assets that would be served from flask.

If you need to make changes to the code, you can start the webpack development server with:

```bash
npm run dev
```

and build it again when you're done.

On the Flask API server CORS is already enabled so you shouldn't have problems making request to it

## Setup the Flask Server

Install the python requirements with:

```bash
pip install -r requirements.txt
```

set the flask app to app.py with

```bash
export FLASK_APP=app.py
```

Create the database with (Note that this creates a database named britcore if it doesn't exist ***If it exists, it would be destoryed and recreated***):

```bash
flask createdb
```

Finally start the flask development server with

```bash
flask run
```

Navigate to `http://localhost:5000` and you should see the Vue SPA rendered (If you've built the `vue` app with `webpack` from the previous section)

### API endpoints

- ***risks*** -> Returns a list of all risks in the database

- ***risks/<risk_id>*** Returns a risk with all it's id's.

### Rationale

![Schema](./schema.png)

I created two tables to manage the Risks namely `risk_template` and `risk_client`. A risk template is the base template for a Risk type, it only contains custom fields and their default values. The `risk_client` table stores information for each client an Insurer wants to manage.

Each `RiskClient` is related to a `RiskTemplate` where it was created from, Updates to the `RiskTemplates` (Such as addition of new fields) can be propagated to all existing `RiskClients` if desired.

The `insurer` table contains information about an insurer.

My approach uses JSON (Specifically `JSONB` columns in `PostgreSQL`, `MySQL` and `SQLite` also support `JSON` fields) to overcome the problem of user defined columns, another approach that could be used is The [Entity Value Approach (EAV)](https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model) which comes with it's own downsides (Lot's of Empty columns or unnecessary joins for the metadata table and the fields table).

With the JSON approach each custom field is stored as JSON along it's with metadata and any custom information about the field you want to store.

This an example of a response returned from the `risk/<id>` endpoint.

```JavaScript
{
  "fields": [
    {
      "dataType": "text",
      "name": "Customer Name",
      "value": ""
    },
    {
      "dataType": "enum",
      "name": "Type",
      "options": [
        "Car",
        "MotorCycle",
        "Truck"
      ],
      "value": ""
    },
    {
      "dataType": "integer",
      "name": "Accidents",
      "value": "0"
    },
    {
      "dataType": "currency",
      "name": "Value",
      "value": 0
    },
    {
      "dataType": "date",
      "name": "Last Renewed",
      "value": "2018-01-01"
    }
  ],
  "id": 1,
  "name": "Automobile"
}
```

This makes it easy to even set default values for each field with the "value" key and for Integer fields we could even do some fancy things like setting max and min values which can be used on the Vue frontend for client side validation e.g on a numeric field`<input type="number" :min="risk.minValue" :max="risk.maxValue">`.

It also makes it ridiculously simple to update field values and even their structure, We just need to replace the existing JSON with the new structure and values we want.

It also makes it easy to build the API since we're mostly returning existing `JSON` from the database.

On the performance side, `JSON` fields in postgres can be queried like normal columns, they can be searched, sorted, filtered, grouped etc. They can also be indexed to speed up the queries.

In conclusion, using `JSON` fields gives us the flexibility of `NoSQL` databases without losing the benefits of a Relational Database.

### Admin interface

I also provided an admin interface (thanks to Flask-admin) to view and change the structure of a risk.

it can be accessed by navigation to `/admin/`


### Unit tests

Does this code actually work? Yes it does.
The tests are written and run with the standard `unittest` module You can run the tests with:

```bash
python tests.py
```
