Example Project for web3auth

This example is provided as a convenience feature to allow potential users to try the app straight from the app repo without having to create a django project.

It can also be used to develop the app in place.

To run this example, follow these instructions:

1. Clone the repository
2. Navigate to the `example` directory
3. Install the requirements for the package (probably in a virtualenv):
		
		pip install -r requirements.txt
		
4. Make and apply migrations

		python manage.py makemigrations
		
		python manage.py migrate
		
5. Run the server

		python manage.py runserver
		
6. Access from the browser at `http://127.0.0.1:8000`
