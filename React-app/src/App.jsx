import React, {Component} from "react";
import NavBar from "./NavBar";
import Main from "./Main";
export default class App extends Component {
    render(){
        return <React.Fragment>
                    <NavBar/><Main/>
                </React.Fragment>;
    }
}