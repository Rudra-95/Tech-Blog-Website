from flask import Flask, render_template
app = Flask(__name__)

@app.route("/blog")
def home_page():
    return render_template('tech_blog.html')

@app.route("/about")
def about_page():
    return render_template('about_tb.html')

@app.route("/contact")
def contact_page():
    return render_template('contact_tb.html')

@app.route("/post")
def post_page():
    return render_template('post_tb.html')

app.run(debug=True)

'''Here, I have made a complete website by making following each-&-every things..
  1) files :- tech_blog.html , about_tb.html , contact_tb.html , post_tb.html on SublimeText 
  2) writing code that redirect all the buttons to different web-pages
'''
''' using Flask with Jinja-templating..'''