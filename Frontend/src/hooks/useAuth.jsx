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
        })
    },[])

    return [isLogin,token];
}
export default useAuth;