import React from "react";
import ReactDOM from "react-dom/client";
import "jquery";
import "popper.js/dist/umd/popper";
import "bootstrap/dist/js/bootstrap";
import "bootstrap/dist/css/bootstrap.css";
//import {NavBar} from "./App"; //when export is not default
import NavBar from "./App";
//const element = <button class="btn btn-danger">Hello World</button>;
import "./index.css";
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<NavBar/>);

//console.log(element);
