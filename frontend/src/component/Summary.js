import React, { Component } from 'react';
import {message} from "antd";

//const{Header,Content} = Layout;

class Factors extends Component {
    constructor(props) {
        super(props);
        this.state = {
            src1 : null,
            time :0
        };
    }
    //get the summary graph 
    getimage=( )=>{
        console.log(`start fetch graph`);
        fetch('http://127.0.0.1:5000/home/summary/', {
          method: 'GET',
          headers: {
            //'Content-Type': 'application/json',
            'Accept': 'application/json',
            "API_TOKEN":localStorage.getItem('API_TOKEN'),
          }
        })
        .then((response) => response.json())
        .then((response) =>{
                if(response.status === 200){
                    console.log(response.image) 
                    console.log(response)
                    this.setState({src1 : `data:image/png;base64,${response.image}`});
                    this.setState({time : 1})
                }else if(response.status===400){
                    message.error(response.error)
                }else{
                    message.error('not responding properly')
                }
                
            })
        
    }
    render() {
        return (
            <div>
                {
                    this.state.time === 0
                    ? this.getimage()
                    : null
                }
                <content>
                The basic usage statistics shown below
                {
                    this.state.src1 === null
                    ? null
                    : <div><img src={this.state.src1} alt='usage statistics'/></div>
                }
                </content>       
            </div>
            );
        
    }
}

export default Factors;