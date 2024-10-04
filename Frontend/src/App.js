import logo from './logo.svg';
// import './App.css';
import {Button} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import react,{useEffect,useState} from 'react'
import ActiveUsers from './components/activeusers';
function LoadingButton(){
  const [loading,setloading] = useState(false)

  useEffect(()=>{
    function simulateNetworkrequest(){
      return new Promise((resolve)=> setTimeout(resolve,2000))
    }
    if (loading) {
      simulateNetworkrequest().then(()=>{
        setloading(false);

      },[loading])
    }
  })
}
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>

        <ActiveUsers>   </ActiveUsers>
        <Button variant='dark'>Grant</Button>
      </header>
    </div>
  );
}

export default App;
