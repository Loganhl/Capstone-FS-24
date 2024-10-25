import React,{useState,useEffect,useRef} from "react";
import keycloak from 'keycloak-js';


const client = new keycloak({
    "realm":"biovault",
    "clientId":"biovault-site",
    "url":"http://localhost"
})

const useAuth =  ()=>{
    const isRun  = useRef(false);
    const [isLogin,setLogin] = useState(false);
    const [token,setToken] = useState(null);
    useEffect(()=>{
        if (isRun.current) return;
        isRun.current = true;
        client.init({
            "onLoad":"check-sso"
        }).then((res)=>{
            setLogin(res);
            setToken(client.token);
        })
    },[])
    return [isLogin,token];
}
export default useAuth;