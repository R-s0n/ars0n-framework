import React, {useState, useEffect} from 'react';
import axios from 'axios';
import Modal from 'react-modal';
import AddFqdnModal from './Components/Modals/AddFqdnModal';
import Fqdn from './Views/Fqdn';
import './App.css'

function App() {
  const [fqdns, setFqdns] = useState([]);
  const [noFqdns, setNoFqdns] = useState(true);
  const [loaded, setLoaded] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [refreshCounter, setRefreshCounter] = useState(0);

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
            fqdns.map((fqdn, i) => {return (
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
    {noFqdns === false && <Fqdn index={activeTab} thisFqdn={fqdns[activeTab]} buttonFunction={deleteFqdn} setActiveTab={setActiveTab} />}
    </div>
  );
}

export default App;
