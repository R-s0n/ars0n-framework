import React, {useState, useEffect} from 'react';
import axios from 'axios';import Modal from 'react-modal';
import AddFqdnModal from './Components/Modals/AddFqdnModal';
import Fqdn from './Views/Fqdn';
import './App.css'

function App() {
  useEffect(()=>setActiveTab(0), [App.index]);
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
  const [scanRunning, setScanRunning] = useState(false)
  const [scanSingleDomain, setScanSingleDomain] = useState(true);
  const [selectedFqdns, setSelectedFqdns] = useState([]);
  
  useEffect(()=>{
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/status');
        const result = await response.json();
        setScanRunning(result['scan_running']);
      } catch (error) {
        console.error('Error fetching data: ', error);
      }
    };

    fetchData()

    axios.post('http://localhost:8000/api/fqdn/all', {})
      .then(res=>{
        setFqdns(res.data);
        if (res.data.length > 0) {
          setNoFqdns(false);
        }
        setLoaded(true);
      })
      .catch(err=>console.log(err))
    
    const interval = setInterval(() => {
          fetchData();
        }, 5000);
      
    return () => clearInterval(interval);
  }, [refreshCounter]);

  // Debugging: Log the selected FQDN whenever the activeTab changes
  useEffect(() => {
    if (fqdns.length > 0 && activeTab < fqdns.length) {
      console.log("Selected FQDN in App.js:", fqdns[activeTab]);
    }
  }, [activeTab, fqdns]);

  const addNewFqdn = () => {
    setNoFqdns(true);
  }

  const deleteFqdn = () => {
    const fqdnToDelete = fqdns[activeTab];
  
    axios.post('http://localhost:8000/api/fqdn/delete', fqdnToDelete)
      .then(res => {
        // Remove the deleted FQDN from the state
        const updatedFqdns = fqdns.filter((_, index) => index !== activeTab);
        setFqdns(updatedFqdns);
        if (updatedFqdns.length === 0) {
          setNoFqdns(true);
        } else {
          // Set the active tab to the first FQDN if available
          setActiveTab(0);
        }
      })
      .catch(err => console.log(err));
  }
  

  const runWildfire = () => {
    // Extract the selected FQDN
    const selectedFqdn = fqdns[activeTab].fqdn;
    console.log("runWildfire: " + selectedFqdn)
    // Prepare the request payload
    const payload = {
      fireStarter: fireStarter,
      fireCloud: fireCloud,
      fireScanner: fireScanner,
      fqdn: selectedFqdn,
      scanSingleDomain: scanSingleDomain,
    };
  
    // Call the API
    axios.post('http://localhost:5000/wildfire', payload)
      .then(res => {
        setScanRunning(true);
        console.log("Wildfire Running...");
      })
      .catch(err => console.log(err));
  }  

  // Dropdown change handler
  const handleDropdownChange = (e) => {
    setActiveTab(parseInt(e.target.value));
  }

  const handleScanSingleDomainChange = (e) => {
    setScanSingleDomain(e.target.checked);
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

  const deleteMultipleFqdn = () => {
    // Logic to delete selected FQDNs
    // Example: axios.post('your-api-endpoint', { fqdnsToDelete: selectedFqdns });
    console.log('Deleting FQDNs:', selectedFqdns);
    // After deletion, clear the selected FQDNs
    setSelectedFqdns([]);
  };

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

    <nav className="p-1 pt-2 pb-2 navbar navbar-expand-lg bg-dark" style={{ overflow: 'auto', whiteSpace: 'nowrap' }} id="style-1">
      <div className="container-fluid">
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              {/* Dropdown for selecting FQDN */}
              <select
                className="form-select dropdown-select mr-2"
                value={activeTab}
                onChange={handleDropdownChange}
                aria-label="Select FQDN"
              >
                {fqdns.map((fqdn, index) => (
                  <option key={index} value={index}>{fqdn.fqdn}</option>
                ))}
              </select>
              {/* Add and Delete FQDN buttons */}
              <button className="btn btn-success mr-2" onClick={addNewFqdn}>Add FQDN</button>
              <button className="btn btn-danger" onClick={deleteFqdn}>Delete FQDN</button>
              <div style={{ display: 'flex', alignItems: 'center', marginTop: '10px' }}>
                <input 
                  type="checkbox" 
                  checked={scanSingleDomain} 
                  onChange={handleScanSingleDomainChange} 
                  style={{ width: '20px', height: '20px', marginRight: '10px' }}
                />
                <span style={{ color: 'white' }}>Scan only selected domain</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>




    <div className="pl-3 p-2 navbar navbar-expand-lg bg-dark" style={{overflow:'auto',whiteSpace:'nowrap'}}>
    {
        scanRunning ?
        <span style={{padding: '15px', color: '#D9D9D9'}}>Scan Status: Running</span> :
        <span style={{padding: '15px', color: '#D9D9D9'}}>Scan Status: NOT Running</span>
      }
      <button  style={{width: '145px'}} className="border border-info nav-link btn btn-primary text-secondary" type="submit" onClick={runWildfire}>Wildfire.py</button>
      <label style={{padding: '15px', color: '#D9D9D9'}} for="checkbox1">Fire-Starter</label>
      <input style={{padding: '15px'}} type="checkbox" id="firestart" name="firestart" class="checkbox" onChange={handleStartToggle} checked={fireStarter}/>
      <label style={{padding: '15px', color: '#D9D9D9'}} for="checkbox2">Fire-Cloud</label>
      <input style={{padding: '15px'}} type="checkbox" id="firecloud" name="firecloud" class="checkbox" onChange={handleCloudToggle} checked={fireCloud}/>
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
