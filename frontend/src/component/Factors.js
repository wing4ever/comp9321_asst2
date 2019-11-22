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
            base64Icon : null,
            image : null
        };
    }

    handleChange=(value)=>{
        console.log(`selected ${value}`);
        fetch('http://127.0.0.1:5000/home/factors/', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "user_token":this.state.user_token
          },
          body: JSON.stringify({
            value 
          })
        })
        .then((response) =>{
            this.setState({base64Icon : `data:image/png;base64,${response}`});
            console.log(this.state.base64Icon);
          })
        
    }

    render() {
        let image;
        if (this.state.base64Icon != null){
        image = <image style={{width: 50, height: 50}} source={{uri: this.state.base64Icon}}/>;
        }
        // the factors in the sate store all our options
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
        {image}
        </div>
        );
    }
}

export default Factors;
