import React, { Component } from 'react';
import {Layout,Select} from "antd";

const{Header,Content} = Layout;
const { Option } = Select;

class Factors extends Component {
    constructor(props) {
        super(props);
        this.state = {
            factors : ['log_price','property_type','room_type','accommodates','bathrooms',
            'bed_type','cancellation_policy','cleaning_fee','host_response_rate','instant_bookable','number_of_reviews','bedrooms','beds'],
            src :null
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
            "user_token":localStorage.getItem('user_token'),
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
                }
                
            })
        
    }

    render() {
        const {factors} = this.state
        return (
            <div>       
                <Header style={{backgroundColor: 'rgba(255, 255, 255, 0.0)'}}>
                    Please select a factor: 
                    <Select style={{ width: 180 }} onChange={this.handleChange}>
                        {factors.map(item => (
                            <Option key={item}>{item}</Option>
                        ))}
                    </Select>
                </Header>
                <Content>
                    here should be chart of selected feature-popularity
                </Content>
                {
                    this.state.src == null
                    ? null
                    : <div><img src={this.state.src} /></div>
                }
            </div>
            );
        
    }
}

export default Factors;
