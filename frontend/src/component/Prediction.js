import React, { Component } from 'react';
import { Form, Select,Button,InputNumber,message,Row, Col } from 'antd';

const { Option } = Select;



class Prediction extends Component {
  constructor(props) {
    super(props);

    this.state = {
        result : null,
        property_type :[
          'Bungalow', 'Casa particular', 'Dorm', 'Treehouse', 'Cave', 'House',
          'Castle', 'Boutique hotel', 'Guest suite', 'Hostel', 'Lighthouse',
          'Villa', 'Townhouse', 'Timeshare', 'Chalet', 'Parking Space', 'Tipi',
          'Tent', 'Loft', 'Bed & Breakfast', 'Other', 'Earth House', 'Camper/RV',
          'Boat', 'Serviced apartment', 'In-law', 'Yurt', 'Hut', 'Train', 'Vacation home',
          'Condominium', 'Cabin', 'Guesthouse', 'Island', 'Apartment'
        ],
        room_type :['Private room', 'Entire home/apt', 'Shared room'],
        bed_type :['Futon', 'Couch', 'Airbed', 'Real Bed', 'Pull-out Sofa' ],
        cancellation_policy :['super_strict_30', 'super_strict_60', 'strict','moderate' , 'flexible' ],
        city :['LA', 'NYC', 'Boston', 'DC', 'SF', 'Chicago' ],
    };
  }
  handleSubmit = e => {
    console.log("start");
    console.log(localStorage.getItem('API_TOKEN'))
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log(JSON.stringify(
          values
        ))
        console.log(values);
        fetch('http://127.0.0.1:5000/home/prediction/', {
          method: 'POST',
          headers: {
            
            "Content-Type":"application/json",
            'Accept': 'application/json',
            "API_TOKEN":localStorage.getItem('API_TOKEN'),
          },
          body: JSON.stringify(
            values
          ),
          credentials: "same-origin"
        })
        .then(response => response.json())
        .then((response) =>{
          if (response.status === 201){
            console.log(this.state.API_TOKEN)
            console.log(localStorage.getItem('API_TOKEN'))
            console.log(response)
            this.setState({result: response.prediction_result})
          }else if(response.status===400){
                message.error(response.error)
            }else{
                message.error('not responding properly')
            }
          
        })
      }
    });
  };

  render() {
    const {property_type,room_type,bed_type,cancellation_policy,city} = this.state
    const { getFieldDecorator } = this.props.form;
    if (this.state.result != null){
      this.content = <h3>popularity: {this.state.result} </h3>
    }else{
      this.content = <h3>popularity: </h3>
    }
    return (
      <div>
      <Form labelCol={{ span: 2 }} wrapperCol={{ span: 6 }} onSubmit={this.handleSubmit}>
        {getFieldDecorator('log_price', {
              initialValue: 4.03123423
            })}
        {/* <Col offset={6}> */}
        <Form.Item label="Property Type" labelCol = {{span:5} } labelAlign = 'left'>
          {getFieldDecorator('property_type', {
            rules: [{ required: true, message: 'Please select your property type!' }],
          })(
            <Select
              placeholder="Select a property type "
            >
              {property_type.map(item => (
                            <Option value={item}>{item}</Option>
              ))}
            </Select>,
          )}
        </Form.Item>
        {/* </Col> */}
        <Form.Item label="Room Type" labelCol = {{span:5} } labelAlign = 'left'>
          {getFieldDecorator('room_type', {
            rules: [{ required: true, message: 'Please select your room type!' }],
          })(
            <Select
              placeholder="Select a room type "
            >
              {room_type.map(item => (
                            <Option value={item}>{item}</Option>
              ))}
            </Select>,
          )}
        </Form.Item>
        {getFieldDecorator('accommodates', {
              initialValue: 4
            })}
        {getFieldDecorator('bathrooms', {
              initialValue: 2
            })}
        <Form.Item label="Bed Type" labelCol = {{span:5} } labelAlign = 'left'>
          {getFieldDecorator('bed_type', {
            rules: [{ required: true, message: 'Please select your bed type!' }],
          })(
            <Select
              placeholder="Select a bed type "
            >
              {bed_type.map(item => (
                            <Option value={item}>{item}</Option>
              ))}
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="Cancellation Policy" labelCol = {{span:5} } labelAlign = 'left'>
          {getFieldDecorator('cancellation_policy', {
            rules: [{ required: true, message: 'Please select your cancellation policy!' }],
          })(
            <Select
              placeholder="Select a cancellation policy "
            >
              {cancellation_policy.map(item => (
                            <Option value={item}>{item}</Option>
              ))}
            </Select>,
          )}
        </Form.Item>
        {getFieldDecorator('cleaning_fee', {
              initialValue: 1
            })}
        <Form.Item label="City" labelCol = {{span:5} } labelAlign = 'left'>
          {getFieldDecorator('city', {
            rules: [{ required: true, message: 'Please select your city!' }],
          })(
            <Select
              placeholder="Select your city "
            >
              {city.map(item => (
                            <Option value={item}>{item}</Option>
              ))}
            </Select>,
          )}
        </Form.Item>
        {getFieldDecorator('host_has_profile_pic', {
              initialValue: 'f'
            })}
        {getFieldDecorator('host_identity_verified', {
              initialValue: 'f'
            })}
        <Form.Item label="Host Response Rate(%)" labelCol = {{span:5} } labelAlign = 'left'>
          {getFieldDecorator('host_response_rate', {
            rules: [{pattern: /^[0-9]+$/,message: 'Please input positive integer'},{ required: true, message: 'Please input your host response rate!' }],
          })(<InputNumber min={0} max={100}/>)}
        </Form.Item>
        {getFieldDecorator('instant_bookable', {
              initialValue: 'f'
            })}
        <Form.Item label="Number Of Reviews" labelCol = {{span:5} } labelAlign = 'left'>
          {getFieldDecorator('number_of_reviews', {
            rules: [ {pattern: /^[0-9]+$/,message: 'Please input positive integer'},{ required: true,message: 'Please input the number of reviews!' }],
          })(<InputNumber min={0}/>)}
        </Form.Item>
        <Form.Item label="Number of Bedrooms" labelCol = {{span:5} } labelAlign = 'left'>
          {getFieldDecorator('bedrooms', {
            rules: [ {pattern: /^[0-9]+$/,message: 'Please input positive integer'},{ required: true, message: 'Please input the number of bedrooms!' }],
          })(<InputNumber min={0}/>)}
        </Form.Item >
        {getFieldDecorator('beds', {
              initialValue: 2
            })}
          <Row >
          <Col xs={{ span: 5, offset: 1 }} lg={{ span: 6, offset: 2 }}>
          <Form.Item >
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
          </Form.Item>
          </Col>
          <Col xs={{ span: 11, offset: 1 }} lg={{ span: 6, offset: 2 }}>
          {this.content}
          </Col>
          
          </Row>
        
      </Form> 
      

      
      </div>      
    );
  }
}

const ContatoForm = Form.create({})(Prediction);

export {ContatoForm};
export default ContatoForm;
