import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../Component.css';

const Enumeration = props => {
    const [loaded, setLoaded] = useState(false)
    const [urls, setUrls] = useState(props.thisFqdn.recon.subdomains.httprobe)
    const [selectedUrl, setSelectedUrl] = useState(props.thisFqdn.recon.subdomains.httprobe[0])
    const [aRecords, setARecords] = useState([])
    const [cnameRecords, setCnameRecords] = useState([])

    useEffect(()=>{
        setARecords(props.thisFqdn.dns.arecord)
        setCnameRecords(props.thisFqdn.dns.cnamerecord)
        setLoaded(true)
    }, [props.index]);

    const populateBurp = () => {
        axios.post('http://localhost:8000/api/populate-burp', urls)
          .then(res=>{
            console.log(res);
          })
          .catch(err=>console.log(err))
      }

    return (
        <div>
        <nav style={{borderBottom: '2px groove #284B63'}} className="pl-2 pt-0 navbar navbar-expand-lg bg-primary">
            <div className="container-fluid">
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <button onClick={populateBurp} style={{width: '135px'}} className="border border-info nav-link btn btn-primary text-secondary">Populate Burp</button>
                    <h5 className="text-secondary ml-4 pt-0 mb-0">Target URL : &nbsp;&nbsp;<a className="text-secondary" target="_blank" rel="noreferrer" href="">Coming Soon...</a></h5>
                </div>
            </div>
        </nav>
                <div className="container-fluid">
                <div className="row">
        <div className="bg-secondary checklistStyle ml-4 col-3" style={{width: '1500px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
            <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
            {
                
                urls.map((url, i) => { return (
                    <li key={i} onClick={(e)=>setSelectedUrl(urls[i])}>{url}</li>
                )})
            }        
            </ul>
        </div>
        <div className="bg-secondary workTableStyle col-8">
            <h2><a href={selectedUrl}>{selectedUrl}</a></h2>
            <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
            {
                aRecords.sort().filter(record => record.split(" ")[0] === selectedUrl.split("//")[1].split(":")[0]).map((record, i) => { return (
                    <li key={i}>{record}</li>
                    )})
            }
            {
                cnameRecords.sort().filter(record => record.split(" ")[0] === selectedUrl.split("//")[1].split(":")[0]).map((record, i) => { return (
                    <li key={i}>{record}</li>
                    )})
            }
            </ul>
            <img src={"/screenshots/" + selectedUrl.replace("//","__") + ".png"} style={{width: '50%', height: '50%'}}/>
        </div>
        </div>
        </div>
        </div>
    )
}

export default Enumeration;