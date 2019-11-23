import React, { Component } from 'react';
import {Layout,Select,message} from "antd";

const{Content} = Layout;
const { Option } = Select;

class Factors extends Component {
    constructor(props) {
        super(props);
        this.state = {
            factors : ['log_price','property_type','room_type','accommodates','bathrooms',
            'bed_type','cancellation_policy','cleaning_fee','host_response_rate','instant_bookable','number_of_reviews','bedrooms','beds'],
            src :null,
            src1 :null,
            time :0
        };
    }
    // click will result in onChange which will send http request with user selected value 
    handleChange=(value)=>{
        console.log(`selected ${value}`);
        fetch('http://127.0.0.1:5000/home/factors/', {
          method: 'POST',
          headers: {
            //'Content-Type': 'application/json',
            'Accept': 'application/json',
            "API_TOKEN":localStorage.getItem('API_TOKEN'),
          },
          body: JSON.stringify({
            "factor":value 
          })
        })
        .then((response) => response.json())
        .then((response) =>{
                if(response.status === 201){
                    console.log(response.image) 
                    console.log(response)
                    this.setState({src : `data:image/png;base64,${response.image}`});
                }else if(response.status===400){
                    message.error(response.error)
                }else{
                    message.error('not responding properly')
                }
                
            })
        
    }
    //get the graph shows the relationships between top eight features and popularity
    getimage=( )=>{
        console.log(`start fetch graph`);
        fetch('http://127.0.0.1:5000/home/factors/', {
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
                }else if(response.status===400){
                    message.error(response.error)
                }else{
                    message.error('not responding properly')
                }
                
            })
        
    }
    render() {
        const {factors} = this.state
        return (
            <div>
                {
                    this.state.time === 0
                    ? (this.getimage(),
                     this.setState({time : 1}))
                    : null
                }
                <content>
                The relationships between top eight features and popularity
                {
                    this.state.src1 === null
                    ? null
                    : <div><img src={this.state.src1} alt='top eight features vs popularity'/></div>
                }
                </content>       
                <Content style={{backgroundColor: 'rgba(255, 255, 255, 0.0)'}}>
                    Please select a factor: 
                    <Select style={{ width: 180 }} onChange={this.handleChange}>
                        {factors.map(item => (
                            <Option key={item}>{item}</Option>
                        ))}
                    </Select>
                </Content>
                <Content>
                    The below graph will show the relationship between selected feature and popularity
                </Content>
                {
                    this.state.src === null
                    ? null
                    : <div><img src={this.state.src} alt='feature vs popularity'/></div>
                }
            </div>
            );
        
    }
}

export default Factors;
