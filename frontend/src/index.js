import React from "react";
import ReactDOM from "react-dom";
import { Redirect,Route, BrowserRouter as Router } from "react-router-dom";

import App from "./App";
import Login from "./component/Login"

import "antd/dist/antd.css";

const AuthenticatedRoute = ({ component: Component, ...rest }) => (
  <Route {...rest} render={props => (
    localStorage.getItem('API_TOKEN') ? (
      <Component {...props}/>
    ) : (
      <Redirect to={{
        pathname: '/login',
        state: { from: props.location }
      }}/>
    )
  )}/>
)
localStorage.removeItem('API_TOKEN');
ReactDOM.render(
  <Router>
    <Route path='/login' component={Login}/>
    <AuthenticatedRoute exact path='/' component={App} />
  </Router>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
