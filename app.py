import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from flask import redirect
from server import app, server
from flask_login import logout_user, current_user

from pages import (
    home,
    profile,
    romi,
)

from pages.auth_pages import (
    login,
    register,
    forgot_password,
    change_password,
)

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Dash Authentication App by Romina Mezher", href="/home"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink(id='user-name',href='/profile')), # TODO temporary solution
                    dbc.NavItem(dbc.NavLink("Home", href="/home")),
                    dbc.NavItem(dbc.NavLink("Romi Page", href="/romi")),
                    dbc.NavItem(dbc.NavLink('Login',id='user-action',href='Login'))
                ]
            )
        ]
    ),
    className="mb-5",
)

footer = html.Footer(children=[dbc.NavItem(dbc.NavLink("Romi Page", href="/romi"))])

app.layout = html.Div(
    [
        header,
        html.Div(
            [
                dbc.Container(
                    id='page-content'
                ),footer
            ]
        ),
        dcc.Location(id='base-url', refresh=True),
    ]
)

# Este callback se encarga de toda la redireccion
@app.callback(
    Output('page-content', 'children'),
    [Input('base-url', 'pathname')])
def router(pathname):

    print('routing to',pathname)
    
    if pathname == '/login':
        if not current_user.is_authenticated:
            return login.layout()
    elif pathname =='/register':
        if not current_user.is_authenticated:
            return register.layout()
    elif pathname == '/change':
        if not current_user.is_authenticated:
            return change_password.layout()
    elif pathname == '/forgot':
        if not current_user.is_authenticated:
            return forgot_password.layout()
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
    
    elif pathname == '/' or pathname=='/home':
        if current_user.is_authenticated:
            return home.layout()
    elif pathname == '/profile':
        if current_user.is_authenticated:
            return profile.layout()
    elif pathname == '/romi':
        if current_user.is_authenticated:
            return romi.layout()

    if current_user.is_authenticated:
        return home.layout()
    
    return login.layout()


# este callback chequea si el usuario esta loggeado o no
# si esta autenticado se muestra la info de perfil
@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def profile_link(content):
    if current_user.is_authenticated:
        return html.Div(current_user.first)
    else:
        return ''

# este callback muestra Logout si el usuario esta loggeado o Login si el usuario no se loggeo aun
@app.callback(
    [Output('user-action', 'children'),
     Output('user-action','href')],
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return 'Logout', '/logout'
    else:
        return 'Login', '/login'

if __name__ == '__main__':
    app.run_server(debug=True)
