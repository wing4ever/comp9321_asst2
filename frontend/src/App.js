import React, { Component } from 'react';
import {Tabs,Layout} from "antd";
import Factors from './component/Factors'
import Prediction from './component/Prediction'

const { Header, Content } = Layout;

const TabPane = Tabs.TabPane;

class App extends Component {
  render() {
    return (
      <div>
        <Header style={{backgroundColor: 'rgba(79, 134, 247, 0.0)'}}>
          <h1>Team Blueberry</h1>
        </Header>
        <Content style={{ padding: '0 50px' }}>
          <Tabs defaultActiveKey="1">
            <TabPane tab="Home" key="1">Introduction to our product</TabPane>
            <TabPane tab="prediction" key="2"><Prediction/></TabPane>
            <TabPane tab="Factors" key="3"><Factors/></TabPane>
          </Tabs>
        </Content>
      </div>
    );
  }
}

export default App;
