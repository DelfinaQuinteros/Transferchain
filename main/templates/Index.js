import React from "react";
import ReactDOM from "react-dom";
import SignInSide from "./SignInSide";
import SignUpSide from "./SignUpSide";
import { BrowserRouter as Router, Route } from "react-router-dom";

import "./styles.css";

function App() {
  return (
    <Router>
      <div className="App">
        <Route path="/" exact component={SignIn} />
        <Route exact path="/signup" component={SignUp} />
      </div>
    </Router>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
