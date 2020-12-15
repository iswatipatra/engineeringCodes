const express = require('express')
const mongoose = require('mongoose')
const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken')
const {JWT_SECRET} = require('../config/keys')
const requireLogin = require('../middleware/requireLogin')

const router = express.Router()
const User = mongoose.model("User")

router.get('/protected',requireLogin,(req,res)=>{
    res.send('Hello user')
})

router.post('/signup', (req, res)=> {
    const {name,email,password,pic} = req.body
    if(!email || !password || !name){
        return res.status(422).json({error:"Please enter all fields"})
    }

    User.findOne({email:email}).then((saveduser)=>{
        if(saveduser){
            return res.status(422).json({error:"user with this email id already present"})
        }
        bcrypt.hash(password,12)
            .then(hashedpassword => {
                const user = new User({
                    email,
                    name,
                    password: hashedpassword,
                    pic
        
                })
        
                user.save()
                .then(user=>{
                    res.json({message:"saved successfully"})
                })
                .catch((err)=>{
                    console.log(err)
                })
            }) 
        
    })
    .catch(err =>{
        console.log(err)
    }) 
})


router.post('/signin',(req,res) =>{
    const {email,password} = req.body
    if(!email || !password){
        res.status(422).json('please give email and password!!')
    }
    
    User.findOne({email: email})
    .then(savedUser =>{
        if(!savedUser){
            return res.status(422).json({error:"invalid email or password!!"})
        }
        bcrypt.compare(password, savedUser.password)
        .then(doMatch => {
            if(doMatch){
                //res.json({message:"successfully signed in!!"})
                const token = jwt.sign({_id: savedUser._id},JWT_SECRET)
                const {_id,name,email,followers,following,pic} = savedUser
                res.json({token, user:{_id,name,email,followers,following,pic}})
            }else{
                return res.status(422).json({error:"invalid email or password!!"})
            }
        })
        .catch(err =>{
            console.log(err)
        })
    })
})
module.exports = router