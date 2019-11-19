import React, { Component} from 'react';
import {Tabs,Layout, Button,message} from "antd";
import Factors from './component/Factors'
import Prediction from './component/Prediction'

const { Header, Content, Footer} = Layout;

const TabPane = Tabs.TabPane;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
        'user_token' : localStorage.getItem('user_token')
        ,'username' : ''
    }
  }


  componentDidMount(){
    window.onbeforeunload = function (e) {
      window.onunload = function () {
        window.localStorage.isMySessionActive = "false";
      }
      return undefined;
    };
  
    window.onload = function () {
      window.localStorage.isMySessionActive = "true";
    };
    
    var myHeader = new Headers({
      "Content-Type":"application/json; charset=utf8",
      "user_token" : this.state.user_token
    });
    console.log(this.state.user_token)
    fetch('http://127.0.0.1:5000/home/user/',{
      method:'GET',
      headers : myHeader
    }).then(results => {
      console.log(results);
      return results.json();
    }).then(data => {
      console.log(data)
      if (data.status === 200){
        this.setState({'username':data.username})
      }else{
        //should have error message
        console.log(data)
        message.error(data.error)
      }
    });
  };

  logout = () =>{
    localStorage.removeItem('user_token')
    this.props.history.push('/');
  };

  render() {
    const {username} = this.state;
    return (
      <div>
        <Header style={{backgroundColor: 'rgba(79, 134, 247, 0.0)'}}>
          <h1>Hi {username}, Welcome to Blueberry</h1>          
        </Header>
        <Content style={{ padding: '0 50px' }}>
          <Tabs defaultActiveKey="1">
            <TabPane tab="Home" key="1">
              <h1>Introduction to Blueberry AirBnB analytic tool</h1><br/>
              <p>
                Our service help AirBnB hosts in major U.S. cities to analyse the populatity of their property.<br/>
                We mainly provide 2 services to help hosts to make decisions. Firstly, we have perdiciton basing on 
                input features given by user. Secondly, we have factor vs popularity which shows data visualisation for 
                how selected factors affects popularity. Both service are aim to help user make better decisions.
              </p>
            </TabPane>
            <TabPane tab="prediction" key="2"><Prediction/></TabPane>
            <TabPane tab="Factors" key="3"><Factors/></TabPane>
          </Tabs>
        </Content>
        <Footer style={{ position: 'fixed', width: '100%', backgroundColor: 'rgba(79, 134, 247, 0.0)' }}>
          <Button onClick={this.logout}>Logout</Button>
        </Footer>
      </div>
    );
  }
}

export default App;
