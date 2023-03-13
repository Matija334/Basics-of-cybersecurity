# Description
Create a database for storing user names and passwords. You may use any database management system. Then, develop a web application that connects to the database, allowing users to register with a username and password, and login to the website (with password verification against the stored password in the database). If the login credentials are incorrect (non-existent username or incorrect password), the application should display a corresponding warning to the user.

To store the password securely, use one of the following functions: SHA256/Bcrypt/Scrypt/Argon2. A salt must also be used. Secure password storage can be performed in SQL or in the application that connects to the database.
