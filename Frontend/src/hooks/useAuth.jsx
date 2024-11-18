import React,{useState,useEffect,useRef} from "react";
import client from "./kclient";

const useAuth =  ()=>{
    const isRun  = useRef(false);
    const [isLogin,setLogin] = useState(false);
    const [token,setToken] = useState(null);
    // const [userinfo,setUserInfo] = useState();
    useEffect(()=>{
        if (isRun.current) return;
        
        isRun.current = true;
        client.init({
            "onLoad":"login-required","enableLogging":true,"pkceMethod":"S256"
        }).then((res)=>{
            setLogin(res);
            setToken(client.token);
            const userProfile ={
                userid:client.idTokenParsed.sub,
                username:client.idTokenParsed.preferred_username,
                firstname: client.idTokenParsed.given_name,
                lastname:client.idTokenParsed.family_name,
            };
            handleProfile(userProfile);
        })
    },[])
    const handleProfile = (userProfile)=>{
        console.log("user:",userProfile);
    }
    return [isLogin,token];
}
export default useAuth;