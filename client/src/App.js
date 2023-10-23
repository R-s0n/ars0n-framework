import React, {useState, useEffect} from 'react';
import axios from 'axios';import Modal from 'react-modal';
import AddFqdnModal from './Components/Modals/AddFqdnModal';
import Fqdn from './Views/Fqdn';
import './App.css'

function App() {
  const [fqdns, setFqdns] = useState([]);
  const [noFqdns, setNoFqdns] = useState(true);
  const [loaded, setLoaded] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [refreshCounter, setRefreshCounter] = useState(0);
  const [fireStarter, setFireStarter] = useState(true);
  const [fireCloud, setFireCloud] = useState(false);
  const [fireScanner, setFireScanner] = useState(false);
  const [fireSpreadder, setFireSpreadder] = useState(false);
  const [fireEnumeration, setFireEnumeration] = useState(false);

  useEffect(()=>{
    axios.post('http://localhost:8000/api/fqdn/all', {})
      .then(res=>{
        setFqdns(res.data);
        if (res.data.length > 0) {
          setNoFqdns(false);
        }
        setLoaded(true);
      })
      .catch(err=>console.log(err))
  }, [refreshCounter]);

  const addNewFqdn = () => {
    setNoFqdns(true);
  }

  const deleteFqdn = (fqdn, index) => {
    axios.post('http://localhost:8000/api/fqdn/delete', fqdn)
      .then(res=>{
        if (fqdns.length === 1){
          setNoFqdns(true);
        }
        setLoaded(false);
        console.log(refreshCounter);
        let temp = refreshCounter + 1;
        console.log(temp);
        setRefreshCounter(temp);
      })
      .catch(err=>console.log(err))
  }

  const runWildfire = () => {
    const flags = {
      fireStarter: fireStarter,
      fireCloud: fireCloud,
      fireScanner: fireScanner
    };
    axios.post('http://localhost:5000/wildfire', flags)
      .then(res=>{
        console.log("Wildfire Running...");
      })
      .catch(err=>console.log(err))
  }

  const handleStartToggle = () => {
    if (fireStarter) {
      setFireStarter(false);
    } else {
      setFireStarter(true)
    }
  }

  const handleCloudToggle = () => {
    if (fireCloud) {
      setFireCloud(false);
    } else {
      setFireCloud(true)
    }
  }

  const handleScannerToggle = () => {
    if (fireScanner) {
      setFireScanner(false);
    } else {
      setFireScanner(true)
    }
  }

  const handleSpreadToggle = () => {
    if (fireScanner) {
      setFireSpreadder(false);
    } else {
      setFireSpreadder(true)
    }
  }

  const handleEnumToggle = () => {
    if (fireScanner) {
      setFireEnumeration(false);
    } else {
      setFireEnumeration(true)
    }
  }

  Modal.setAppElement('#root');

  return (
    <div>
    { loaded && <Modal 
                  isOpen={noFqdns}
                  style={{
                    overlay: {
                      backgroundColor: 'grey'
                    },
                    content: {
                      height: '700px',
                      width: '450px',
                      margin: 'auto'
                    }
                  }}>
      <AddFqdnModal fqdns={fqdns} setFqdns={setFqdns} setNoFqdns={setNoFqdns} />
    </Modal> }
    <nav className="p-1 pt-2 pb-2 navbar navbar-expand-lg bg-dark" style={{overflow:'auto',whiteSpace:'nowrap'}} id="style-1">
      <div className="container-fluid">
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {
            fqdns.sort(function(a,b){
              return new Date(b.updatedAt) - new Date(a.updatedAt)
            }).map((fqdn, i) => {return (
              <li className="mr-3 nav-item" key={i}>
                { i === activeTab ?
                <button className="border border-info nav-link btn btn-primary text-secondary active" aria-current="page" href="#">{fqdn.fqdn}</button> :
                <button className="border border-info nav-link btn btn-primary text-secondary" onClick={()=>setActiveTab(i)}aria-current="page" href="#">{fqdn.fqdn}</button>
                }
                </li>
            )})
            }
          </ul>
          <button  style={{width: '145px'}} className="border border-info nav-link btn btn-primary text-secondary" type="submit" onClick={addNewFqdn}>Add FQDN</button>
        </div>
      </div>
    </nav>
    <div className="pl-3 p-2 navbar navbar-expand-lg bg-dark" style={{overflow:'auto',whiteSpace:'nowrap'}}>
      <button  style={{width: '145px'}} className="border border-info nav-link btn btn-primary text-secondary" type="submit" onClick={runWildfire}>Wildfire.py</button>
      <label style={{padding: '15px', color: '#D9D9D9'}} for="checkbox1">Fire-Starter</label>
      <input style={{padding: '15px'}} type="checkbox" id="firestart" name="firestart" class="checkbox" onChange={handleStartToggle} checked={fireStarter}/>
      <label style={{padding: '15px', color: '#D9D9D9', textDecoration: 'line-through'}} for="checkbox2">Fire-Cloud</label>
      <input style={{padding: '15px'}} type="checkbox" id="firecloud" name="firecloud" class="checkbox" onChange={handleCloudToggle} checked={fireCloud} disabled/>
      <label style={{padding: '15px', color: '#D9D9D9'}} for="checkbox3">Fire-Scanner</label>
      <input style={{padding: '15px'}} type="checkbox" id="firescan" name="firescan" class="checkbox" onChange={handleScannerToggle} checked={fireScanner}/>
      <label style={{padding: '15px', color: '#D9D9D9', textDecoration: 'line-through'}} for="checkbox2">Fire-Spreadder</label>
      <input style={{padding: '15px'}} type="checkbox" id="firecloud" name="firecloud" class="checkbox" onChange={handleSpreadToggle} checked={fireSpreadder} disabled/>
      <label style={{padding: '15px', color: '#D9D9D9', textDecoration: 'line-through'}} for="checkbox2">Fire-Enumeration</label>
      <input style={{padding: '15px'}} type="checkbox" id="firecloud" name="firecloud" class="checkbox" onChange={handleEnumToggle} checked={fireEnumeration} disabled/>
    </div>
    {noFqdns === false && <Fqdn index={activeTab} thisFqdn={fqdns[activeTab]} buttonFunction={deleteFqdn} setActiveTab={setActiveTab} />}
    </div>
  );
}

export default App;
