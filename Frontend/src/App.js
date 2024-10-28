import logo from './logo.svg';
// import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import userMetrics from './components/Metrics/Keyspersec';
import useAuth from './hooks/useAuth';
import ActiveUsers from './components/activeusers';
import Usermetrics from './components/Metrics/Keyspersec';
import { Button } from 'react-bootstrap';
import client from './hooks/kclient';
// import UserStats from './components/userMetrics';

const Apps = ({token})=>{
  ChartJS.register(ArcElement, Tooltip, Legend);
  const datab = {
    labels:['TouchDowns','Yards per Carry','Yards per Game'],
    data:[4,7,30],
    backgroundColor:[
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    ],
    borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
    ],
    borderWidth: 1,
}
  return(<div className='App'>
    <header className='App-header'></header>
      <div>
        <Button variant='dark' onClick={()=>{
          client.logout()
        }}>Logout</Button>
      </div>
      <Usermetrics/>
      <ActiveUsers token={token}></ActiveUsers>
  
  </div>)
}
function App() {
  const [isLogin,token] = useAuth();
  if (isLogin == true) {
    return(<Apps token={token}></Apps>)
  }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
