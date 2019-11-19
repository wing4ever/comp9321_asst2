import React, { Component } from 'react';
import {Input,Button,Layout,message} from "antd";

const { Header, Content } = Layout;

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username : ''
            ,password : ''
        }
    }

    changeUsername=(e)=>{
        this.setState({username:e.target.value});
    }
    changePassword=(e)=>{
        this.setState({password:e.target.value});
    }

    disableSubmit(){
        const{username,password} = this.state;
        if (username==='' || password===''){
            return true;
        }
        return false;
    }

    auth = () => {
        const{username,password} = this.state;
        // here should set up the auth with username and password sent to backend
        // backend verify and return a token if success
        const myBody = {
            "username":username,
            "password":password,
        }
        var myHeader = new Headers({
            "Content-Type":"application/json; charset=utf8",
        })
      
        fetch('http://127.0.0.1:5000/login/',{
            method:'POST',
            credentials:'include',
            headers : myHeader,
            mode : 'no-cors',
            body: JSON.stringify(myBody)
        }).then(results => {
            return results.json();
        }).then(response => {
            if (response.status===201){
                localStorage.setItem('user_token',response.token);
                message.success('login successed')
                this.props.history.push('/');              
            }else if(response.status===400){
                message.error(response.error)
            }else{
                message.error('not responding properly')
            }
        })
    }

    signup = () => {
        const{username,password} = this.state;
        // here should set up the auth with username and password sent to backend
        // backend verify and return a token if success
        const myBody = {
            "username":username,
            "password":password,
        }
        var myHeader = new Headers({
            "Content-Type":"application/json; charset=utf8",
        })
        console.log(myBody)
        
        fetch('http://127.0.0.1:5000/signup/',{
            method:'POST',
            headers : myHeader,
            mode : 'no-cors',
            body: JSON.stringify(myBody)
        }).then(results => {
            console.log(results.json());
            return results.json();
        }).then(response => {
            console.log(response)
            if (response.status===201){
                localStorage.setItem('user_token',response.token);
                message.success('login successed')
                this.props.history.push('/');              
            }else if(response.status===400){
                console.log(response.error)
                message.error(response.error)
            }else{
                message.error('not responding properly')
            }
        })
    }


    render() {
        const{username,password} = this.state;

        return (
            <div>
                <Header style={{backgroundColor: 'rgba(79, 134, 247, 0.0)'}}>
                    <h1>Blueberry Login</h1>
                </Header>
                <Content style={{ padding: '0 50px' }}> 
                    <Input placeholder='Username' value={username} onChange={this.changeUsername}/><br/>
                    <Input placeholder='Password' value={password} onChange={this.changePassword}/><br/>
                    <Button disabled={this.disableSubmit()} onClick={this.auth}>Login</Button>
                    <p>OR</p>
                    <Button disabled={this.disableSubmit()} onClick={this.signup}>Signup</Button>
                </Content>
            </div>
        );
    }
}
export default Login;
