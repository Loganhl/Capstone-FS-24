// import Router, { Route, Routes } from 'react-router'
import Home from './pages/home'
import Dashboard from './pages/dashboard'
import NotFound from './pages/notfound'
//import client from './hooks/kclient'
//import useAuth from './hooks/useAuth'
import {BrowserRouter as  Router,Route,Routes} from  'react-router-dom'
// const Routing = ()=>{
//     const [isLogin,token] = useAuth();
//     return(
//     <Router>
//     <Routes>
//         <Route path='/'>
//             <Route index element={<Home/>}/>
//             <Route path='dashboard' element={<Dashboard token={token} client={client}/>}/>
//             <Route path='*' element={<NotFound/>}/>

//         </Route>
//     </Routes>
//     </Router>
// )}

const AppRouter = ({ token, client, theme })=>{
    return(
        <Router>
            <Routes>
                <Route exact path='/' element={<Home theme={theme}/>}/>
                <Route path='/dashboard' element={<Dashboard/>}/>
                <Route path='/notfound' element={<NotFound/>}/>
            </Routes>
        </Router>
    )
}
export default AppRouter;