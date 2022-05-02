## SNAP & SELL PROJECT. A online marketplace for camera enthusiasts

A online marketplace for selling and buying camera related products such as DSLR, tripod, lens and many more. This E-commerce website provides a online marketplace to sell your camera for cash or buy a camera that you are searching based on their specification, price. This project is built with Django framework in back end and HTML, CSS and Javascript framework for the front end.

Key features:
1. CRUD model
2. Query posts
3. Pie chart post statistics
4. Django admin control

## Getting Started
1. clone the repository from Github
2. pip install -r requirement.txt 
3. cd SnapAndSell
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py runserver

(Account)

Back-end:
- A class model of user profile for user account
- 5 views: Sign up view, Login view, Edit profile view, My post view, Change password view, Profile page view
- 3 forms classes: Sign up form, Edit profile form and Change password form

Front end:
- Change_password.html: display page for user to change password
- Edit_profile.html: display the page for user to edit profile
- login.html: display login page
- my_posts.html: display user's posts page
- profile.html: display user's profile page
- signup.html: display user's sign up form page

(Post)

Back-end:
- 3 classes model: AssestType, Post and PostPicture
- PostAPI for query posts
- IndexView for featuring posts
- CreateView for creating post
- DetailView for displaying each post
- EditPostView for editing post
- delete_view for deleting post
- 2 forms: Post form and Post picture form

Front-end:
- Create.html: display page for user to create post
- detail.html: display each post page
- edit_post.html: display the page for user to edit post
- index.html: display the homepage

(Other)
- style.css: colour and layout
- index_script.js: create user and post card with details
- base_layout.html: display structure of header and footer

