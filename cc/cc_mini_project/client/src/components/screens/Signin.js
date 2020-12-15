import React,{useState,useContext} from 'react'
import {Link,useHistory} from 'react-router-dom'
import M from 'materialize-css'
import {UserContext} from '../../App'

const Signin = ()=>{
    const {state,dispatch} = useContext(UserContext)
    const history = useHistory()
    const [password,setPassword] = useState("")
    const [email,setEmail] = useState("")

    const PostData = ()=>{
        if(!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)){
           M.toast({html:"invalid email",classes:"#ef5350 red lighten-1"})
            return
        }

        fetch("/signin",{
            method:"post",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                password,
                email
            })
        }).then(res=>res.json())
        .then(data=>{
            if(data.error){
                M.toast({html:data.error,classes:"#ef5350 red lighten-1"})
                
            }else{
                localStorage.setItem("jwt",data.token)
                localStorage.setItem("user",JSON.stringify(data.user))
                dispatch({type:"USER",payload:data.user})
                M.toast({html:"signedin successfully", classes:"#66bb6a green lighten-1"})
                console.log(data)
                history.push('/')
            }
        }).catch(err=>{
            console.log(err)
        })
    
    }

    return(
        <div className="mycard">
            <div className="card auth-card">
            <h2>Instagram</h2>
            <input 
            type="text"
            placeholder="email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
            />
            <input
            type="password"
            placeholder="password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
            />
            <button className="btn waves-effect waves-light" onClick={()=>PostData()} >Login
             </button>
            </div>
        </div>
    )
}

export default Signin