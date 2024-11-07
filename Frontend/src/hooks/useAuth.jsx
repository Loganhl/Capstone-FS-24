import React,{useState,useEffect,useRef} from "react";
import client from "./kclient";

const useAuth =  ()=>{
    const isRun  = useRef(false);
    const [isLogin,setLogin] = useState(false);
    const [token,setToken] = useState(null);
    useEffect(()=>{
        if (isRun.current) return;
        
        isRun.current = true;
        client.init({
            "onLoad":"login-required","enableLogging":true
        }).then((res)=>{
            setLogin(res);
            setToken(client.token);
        })
    },[])
    return [isLogin,token,client];
}
export default useAuth;