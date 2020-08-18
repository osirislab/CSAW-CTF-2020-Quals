#!/usr/bin/env python3
import re
import bz2
import base64
import html
import random
import zwsp_steg

import flask
import flask_wtf
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired

app = flask.Flask(__name__, template_folder=".")
app.config["SECRET_KEY"] = "hgp12d89whd0p832DHPEUIBFP3UgrpJXBNM"

# final flag that gets returned to user
FLAG = "flag{gu3ss_u_f0und_m3}"

# password that gets encoded, compressed and encoded as zero-width characters again
STAGE_ONE_PWD = "alm0st_2_3z"
STAGE_TWO_PWD = "u_unh1d_m3!"


class EmailForm(flask_wtf.FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Sign up")


class Injector:
    def __init__(self, template_path):

        # represents the parsed out template, with no content added to it
        self.template_path = template_path

        # simply encode and append for the first stage - easy!
        encoded_pwd_one = base64.b64encode(STAGE_ONE_PWD.encode("utf-8"))
        self.stage_one_pwd = zwsp_steg.encode(str(encoded_pwd_one))

        # encode and compress, and then randomly distribute payload across corpus - harder!
        encoded_pwd_two = base64.b64encode(STAGE_TWO_PWD.encode("utf-8"))
        encoded_pwd_two = bz2.compress(encoded_pwd_two)
        self.stage_two_pwd = zwsp_steg.encode(str(encoded_pwd_two))


    def stage1(self, content) -> str:
        """
        Given raw HTML source, simply append the encoded password for the
        stage to the end of the rendered document.
        """
        form = EmailForm()
        return flask.render_template(self.template_path, body=content, form=form) + self.stage_one_pwd


    def stage2(self, content) -> str:
        """
        Given raw HTML source, identify all injectable positions in the document,
        and randomly place them in those injectable positions, while maintaining order.
        """

        form = EmailForm()
        full_html = flask.render_template(self.template_path, body=content, form=form)
        html_lst = re.split(r"(\s+)", full_html)

        # queue up all the injectable spaces we can use
        positions = []
        for pos, val in enumerate(html_lst):
            if " " in val:
                positions += [pos]

        for char, pos in zip(self.stage_two_pwd, positions):
            html_lst[pos] = " " + char

        return " ".join(html_lst)


injector = Injector("template.html")

@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html"), 404


@app.route("/", methods=["GET", "POST"])
def stage1():
    if flask.request.method == "POST":
        pwd = flask.request.form["email"]
        if pwd == STAGE_ONE_PWD:
            flask.flash("/ahsdiufghawuflkaekdhjfaldshjfvbalerhjwfvblasdnjfbldf/<pwd>")
        else:
            flask.flash("Whoops, couldn't add, sorry!")


    content = """
    <h2>About</h2>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Perferendis quas sint et nihil iusto eius nostrum sit error, repellat optio quisquam! Magnam dolore iusto cumque. Nostrum error iste neque maiores.</p>
    <h2>Skills</h2>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis in maiores autem quidem obcaecati excepturi! Cupiditate eaque itaque magni voluptatibus neque nobis est dolor? Atque sunt minus ipsa asperiores. At.</p>
    <h2>Projects</h2>
    <a href="#">Project 1</a>
    <a href="#">Project 2</a>
    <a href="#">Project 3</a>
    <a href="#">Project 4</a>
    <a href="#">Project 5</a>
    <h2>Contact</h2>
    <p>myEmail@email.com</p>"""
    return injector.stage1(content)


@app.route("/ahsdiufghawuflkaekdhjfaldshjfvbalerhjwfvblasdnjfbldf/<pwd>", methods=["GET", "POST"])
def stage2(pwd):
    if pwd != STAGE_ONE_PWD:
        return flask.render_template("404.html")

    if flask.request.method == "POST":
        pwd = flask.request.form["email"]
        if pwd == STAGE_TWO_PWD:
            flask.flash("/19s2uirdjsxbh1iwudgxnjxcbwaiquew3gdi/<pwd1>/<pwd2>")
        else:
            flask.flash("Whoops, couldn't add, sorry!")

    # TODO: change up
    content= """
    <p>Alright you almost got me!</p>
    """
    return injector.stage2(content)


@app.route("/19s2uirdjsxbh1iwudgxnjxcbwaiquew3gdi/<pwd1>/<pwd2>", methods=["GET", "POST"])
def success(pwd1, pwd2):
    if pwd1 != STAGE_ONE_PWD:
        return flask.render_template("404.html")
    if pwd2 != STAGE_TWO_PWD:
        return flask.render_template("404.html")

    return FLAG


if __name__ == "__main__":
    app.run()
