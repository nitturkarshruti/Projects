import React, {Component} from "react";

export default class Main extends Component{
    state={pageTitle:"Customers", 
        customerCount:5,
    customers:[{id: 1, name: "abc"},
        {id: 2, name: "xyz"},
        {id: 3, name: "def"},
        {id: 4, name: "ghi"},
        {id:5, name: "jkl"}
    ]};
    render(){
        return (<div>
                <h4 className="border-bottom m-1 p-1">
                    {this.state.pageTitle}  
                    <span className="badge bg-secondary m-2">{this.state.customerCount}</span>
                    <button className="btn btn-info" onClick={this.onRefreshClick}>Refresh</button>
                </h4>
                <table className="table">
                    <thead>
                    <tr>
                        <th>Id</th>
                        <th>Name</th>
                    </tr>
                    </thead>
                    <tbody>
                        {
                            this.state.customers.map((cust)=>{return(
                                <tr key={cust.id}>
                                    <td>{cust.id}</td>
                                    <td>{cust.name}</td>
                                </tr>

                            );

                            })
                        }
                    </tbody>
                </table>
            </div>
        );    
    }
    //Executes when the user clicks on Refresh button
    onRefreshClick=()=>{
        //console.log("Refresh clicked")
        this.setState({customerCount:7 });
    }
}