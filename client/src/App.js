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
  const [scanStep, setScanStep] = useState(false)
  const [scanComplete, setScanComplete] = useState(false)
  const [scanStepName, setScanStepName] = useState(false)
  const [scanSingleDomain, setScanSingleDomain] = useState(true);
  const [selectedFqdns, setSelectedFqdns] = useState([]);
  const [coreModule, setCoreModule] = useState("N/a")
  const [scanDomain, setScanDomain] = useState("N/a")
  
  const getCurrentDateTime = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    return `${year}_${month}_${day}_${hours}-${minutes}-${seconds}`;
  };

  const [fileName, setFileName] = useState(getCurrentDateTime());
  
  useEffect(()=>{
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/status');
        const result = await response.json();
        setScanRunning(result['scan_running']);
        setScanStep(result['scan_step']);
        setScanStepName(result['scan_step_name']);
        setScanComplete(result['scan_complete']);
        setCoreModule(result['core_module']);
        setScanDomain(result['scan_target']);
      } catch (error) {
        console.error('Error fetching data: ', error);
      }
    };

    fetchData()

    axios.post('http://localhost:8000/api/fqdn/all', {})
      .then(res=>{
        console.log(res.data);
        setFqdns(res.data);
        if (res.data.length > 0) {
          setNoFqdns(false);
        }
        setLoaded(true);
      })
      .catch(err=>console.log(err))
    
    const interval = setInterval(() => {
          fetchData();
        }, 500);
      
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

  const exportData = () => {
    const jsonData = JSON.stringify(fqdns, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const a = document.createElement('a');
    a.download = `${fileName}.json`;
    a.href = window.URL.createObjectURL(blob);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleFileUpload = (file) => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedData = JSON.parse(e.target.result);
          importedData.forEach((importedFqdn) => {
            const existingIndex = fqdns.findIndex(
              (existingFqdn) => existingFqdn.fqdn === importedFqdn.fqdn
            );
            if (existingIndex === -1) {
              setFqdns((prevData) => [...prevData, importedFqdn]);
              axios.post("http://localhost:8000/api/fqdn/new",importedFqdn)
            } else {
              setFqdns((prevData) => {
                const newData = [...prevData];
                newData[existingIndex] = importedFqdn;
                return newData;
              });
              axios.post("http://localhost:8000/api/fqdn/update",importedFqdn)
            }
          });
        } catch (error) {
          console.error('Error parsing JSON file:', error);
        }
      };
      reader.readAsText(file);
    }
  };

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
  
  const handleUnloadButtonClick = () => {
    document.getElementById('fileInput').value = '';
  };

  const runWildfire = () => {
    const selectedFqdn = fqdns[activeTab].fqdn;
    console.log("runWildfire: " + selectedFqdn)

    if (!scanSingleDomain){
      const payload = {
        fireStarter: fireStarter,
        fireCloud: fireCloud,
        fireScanner: fireScanner,
        fqdn: selectedFqdn,
        scanSingleDomain: scanSingleDomain,
        domainCount: fqdns.length
      };
      axios.post('http://localhost:5000/wildfire', payload)
      .then(res => {
        setScanRunning(true);
        console.log("Wildfire Running Against All Domains...");
      })
      .catch(err => console.log(err));
    } else {
      const payload = {
        fireStarter: fireStarter,
        fireCloud: fireCloud,
        fireScanner: fireScanner,
        fqdn: selectedFqdn,
        scanSingleDomain: scanSingleDomain,
        domainCount: 1
      };
      axios.post('http://localhost:5000/wildfire', payload)
      .then(res => {
        setScanRunning(true);
        console.log("Wildfire Running Against Single Domain...");
      })
      .catch(err => console.log(err));
    }
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

  const handleButtonClick = () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (file) {
      handleFileUpload(file);
      document.getElementById('fileInput').value = '';
    }
  };

  const handleCollectScreenshotsButton = () => {
    axios.post('http://localhost:5000/collect_sceenshots',{})
      .then(res => {
        console.log("Collecting Screenshots...");
      })
  }

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
                      margin: 'auto',
                      backgroundColor: '#ECF0F1'
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
            <li className="nav-item ml-5">
            <h3 style={{ color: 'white' }}>Data Export</h3>
            <div class="form-group">
            <label style={{ color: 'white' }}>
              File Name:
              <input
                className="ml-2" 
                type="text"
                value={fileName}
                onChange={(e) => setFileName(e.target.value)}
              />
            </label>
            <button className="border border-info btn btn-primary text-secondary ml-2" onClick={exportData}>Export Data</button>
            </div>
            </li>
            <li className="nav-item ml-5">
            <div>
              <label style={{ color: 'white' }}>
                <h3 style={{ color: 'white' }}>Data Import</h3>
                <input class="form-control" type="file" accept=".json" id="fileInput" />
              </label>
              <button className="border border-info btn btn-primary text-secondary ml-2" onClick={handleButtonClick}>Process</button>
              <button className="border border-info btn btn-primary text-secondary ml-2" onClick={handleUnloadButtonClick}>Unload</button>
            </div>
            </li>
            <li>
              <button className="border border-info btn btn-primary text-secondary m-4 p-3 ml-5" onClick={handleCollectScreenshotsButton}>Collect Screenshots</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>




    <div className="pl-3 p-2 navbar navbar-expand-lg bg-dark" style={{ overflow: 'auto', whiteSpace: 'nowrap' }}>
      <span style={{ display: 'block', padding: '15px', color: '#D9D9D9', width: '250px'}}>
          Core Module: {coreModule}<br></br>
          Target Domain: {scanDomain}
      </span>
      <span style={{ display: 'block', padding: '15px', color: '#D9D9D9', width: '350px'}}>
          Scan Step: {scanStep} / {scanComplete}<br></br>
          Current Step: {scanStepName}
      </span>
      <select
                className="form-select dropdown-select mr-2"
                value="wildfire"
                onChange={handleDropdownChange}
                aria-label="Select Scan"
              >
                <option value="wildfire">Wildfire.py</option>
                <option value="slowburn" disabled>Slowburn.py</option>
                <option value="scorched-earth" disabled>ScorchedEarth.py</option>
      </select>
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
      {
        scanRunning ?
        <button  style={{width: '100px', marginLeft: '15px'}} className="border border-info nav-link btn btn-primary text-secondary" type="submit" disabled>Cancel</button> :
        <button  style={{width: '75px', marginLeft: '15px'}} className="border border-info nav-link btn btn-primary text-secondary" type="submit" onClick={runWildfire}>Scan</button>
      }
      <button  style={{width: '75px', marginLeft: '15px'}} className="border border-info nav-link btn btn-primary text-secondary" type="submit" disabled>Pause</button>
    </div>
    {noFqdns === false && fqdns.length > 0 && loaded && <Fqdn index={activeTab} thisFqdn={fqdns[activeTab]} buttonFunction={deleteFqdn} setActiveTab={setActiveTab} />}
    </div>
  );
}

export default App;
