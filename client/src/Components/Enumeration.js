import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../Component.css';

const Enumeration = props => {
    const [urls, setUrls] = useState(props.thisFqdn.recon.subdomains.httprobe)
    const [selectedUrl, setSelectedUrl] = useState(props.thisFqdn.recon.subdomains.httprobe[0])
    const [selectedScreenshot, setSelectedScreenshot] = useState("")

    const changeUrl = (e, i) => {
        setSelectedUrl(urls[i])
    }

    return (
        <div>
        <nav style={{borderBottom: '2px groove #284B63'}} className="pl-2 pt-0 navbar navbar-expand-lg bg-primary">
            <div className="container-fluid">
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
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
            <img src={"/screenshots/" + selectedUrl.replace("//","__") + ".png"} style={{width: '50%', height: '50%'}}/>
        </div>
        </div>
        </div>
        </div>
    )
}

export default Enumeration;