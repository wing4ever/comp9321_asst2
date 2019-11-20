import React, { Component } from 'react';
import { Form, Select, Input, Button, Radio } from 'antd';

const { Option } = Select;



class Prediction extends Component {
  constructor(props) {
    super(props);

    this.state = {
        result : null
    };
  }
  handleSubmit = e => {
    console.log("start")
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log(values)
        fetch('http://127.0.0.1:5000/home/prediction/', {
          method: 'POST',
          headers: {
            
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "user_token":this.state.user_token
          },
          body: JSON.stringify(
            values
          ),
          credentials: "same-origin"
        })
        .then(response => response.json())
        .then((response) =>{
          console.log("response")
          let val = response.values.Bed_type
          console.log(val);
          this.setState({result: val})
        })
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    if (this.state.result != null){
      this.content = <h3>popularity: {this.state.result} </h3>
    }else{
      this.content = <h3>popularity: </h3>
    }
    return (
      <div>
      <Form labelCol={{ span: 2 }} wrapperCol={{ span: 6 }} onSubmit={this.handleSubmit}>
        <Form.Item label="log_price">
          {getFieldDecorator('log_price', {
            rules: [{ required: true, message: 'Please input your log_price!' }],
          })(<Input />)}
        </Form.Item>
        <Form.Item label="property_type">
          {getFieldDecorator('property_type', {
            rules: [{ required: false, message: 'Please select your property_type!' }],
          })(
            <Select
              placeholder="Select a property_type "
            >
              <Option value="1">  Loft    </Option>
              <Option value="2">  House   </Option>
              <Option value="3"> Apartment</Option>
              <Option value="4">Condominium</Option>
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="cancellation_policy">
          {getFieldDecorator('cancellation_policy', {
            rules: [{ required: false, message: 'Please select your cancellation_policy!' }],
          })(
            <Select
              placeholder="Select a cancellation_policy "
            >
              <Option value="1">  strict   </Option>
              <Option value="2">  flexible   </Option>
              <Option value="3"> moderate</Option>
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="accommodates">
          {getFieldDecorator('accommodates', {
            rules: [{ required: false, message: 'Please select your accommodates!' }],
          })(
            <Select
              placeholder="Select a cancellation_policy "
            >
              <Option value="1">  1   </Option>
              <Option value="2">  2   </Option>
              <Option value="3"> 3</Option>
              <Option value="4">4 </Option>
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="bathrooms">
          {getFieldDecorator('bathrooms', {
            rules: [{ required: false, message: 'Please select your bathrooms!' }],
          })(
            <Select
              placeholder="Select a bathrooms "
            >
              <Option value="1">  1   </Option>
              <Option value="2">  2   </Option>
              <Option value="3"> 3</Option>
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="host_response_rate">
          {getFieldDecorator('host_response_rate', {
            rules: [{ required: false, message: 'Please select your host_response_rate!' }],
          })(
            <Select
              placeholder="Select a host_response_rate "
            >
              <Option value="1">  50%   </Option>
              <Option value="2">  75%   </Option>
              <Option value="3"> 100%</Option>
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="number_of_reviews">
          {getFieldDecorator('number_of_reviews', {
            rules: [{ required: false, message: 'Please select your number_of_reviews!' }],
          })(
            <Select
              placeholder="Select a number_of_reviews "
            >
              <Option value="1">  10   </Option>
              <Option value="2">  50   </Option>
              <Option value="3"> 100 </Option>
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="bedrooms">
          {getFieldDecorator('bedrooms', {
            rules: [{ required: false, message: 'Please select your bedrooms!' }],
          })(
            <Select
              placeholder="Select a bedrooms "
            >
              <Option value="1">  1   </Option>
              <Option value="2">  2   </Option>
              <Option value="3"> 3 </Option>
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="beds">
          {getFieldDecorator('beds', {
            rules: [{ required: false, message: 'Please select your beds!' }],
          })(
            <Select
              placeholder="Select a beds "
            >
              <Option value="1">  1   </Option>
              <Option value="2">  2   </Option>
              <Option value="3"> 3 </Option>
            </Select>,
          )}
        </Form.Item>
        <Form.Item label="bed_type">
          {getFieldDecorator('bed_type', {
            rules: [{ required: false, message: 'Please select your bed_type!' }],
          })(
            <div>
            <Radio.Group defaultValue="a" buttonStyle="solid" >
              <Radio.Button value="1">RealBed</Radio.Button>
              <Radio.Button value="2">Futon</Radio.Button>
            </Radio.Group>
             </div>
          )}
        </Form.Item>
        <Form.Item label="room_type">
          {getFieldDecorator('room_type', {
            rules: [{ required: false, message: 'Please select your room_type!' }],
          })(
            <div>
            <Radio.Group defaultValue="a" buttonStyle="solid" >
              <Radio.Button value="1">Entire home/apt</Radio.Button>
              <Radio.Button value="2">Private room</Radio.Button>
            </Radio.Group>
             </div>
          )}
        </Form.Item>
        <Form.Item label="cleaning_fee">
          {getFieldDecorator('cleaning_fee', {
            rules: [{ required: false, message: 'Please select your cleaning_fee!' }],
          })(
            <div>
            <Radio.Group defaultValue="a" buttonStyle="solid" >
              <Radio.Button value="1">TRUE</Radio.Button>
              <Radio.Button value="2">FALSE</Radio.Button>
            </Radio.Group>
             </div>
          )}
        </Form.Item>
        <Form.Item label="instant_bookable">
          {getFieldDecorator('instant_bookable', {
            rules: [{ required: false, message: 'Please select your instant_bookable!' }],
          })(
            <div>
            <Radio.Group defaultValue="a" buttonStyle="solid" >
              <Radio.Button value="1">TRUE</Radio.Button>
              <Radio.Button value="2">FALSE</Radio.Button>
            </Radio.Group>
             </div>
          )}
        </Form.Item>
        <Form.Item wrapperCol={{ span: 12, offset: 4 }}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
        <div>
        
        </div>
      </Form> 
      {this.content}
      </div>      
    );
  }
}

const ContatoForm = Form.create({})(Prediction);

export {ContatoForm};
export default ContatoForm;
