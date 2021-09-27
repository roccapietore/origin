from flask import Flask, request, render_template
import json

app = Flask(__name__)

with open("users.json", "r") as f:
    users_list = json.load(f)


@app.route('/')
def index():
    return render_template("index.html", users_list=users_list)


@app.route('/search/')
def search():
    search_list = []
    if request.args.get("name"):
        search_name = request.args.get("name", " ")
        for user in users_list:
            if search_name.lower() in user["name"].lower():
                search_list.append(user)
    return render_template("search.html", users_list=search_list, found_users=len(search_list))


@app.route('/add_user', methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("add_user.html", users_list=users_list)
    elif request.method == "POST":
        new_user = {
            "name": request.form["name"],
            "age": request.form["age"],
            "is_blocked": request.form["is_blocked"],
            "unblock_date": request.form["unblock_date"]
        }
        users_list.append(new_user)
        return render_template("search.html", users_list=users_list, found_users=len(users_list))

    with open("users.json", "a") as f:
        f.write(json.dumps(users_list))


if __name__ == '__main__':
    app.run()
