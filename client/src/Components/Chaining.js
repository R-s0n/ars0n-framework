import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../Component.css';

const Chaining = props => {
    const [urls, setUrls] = useState(props.thisFqdn.targetUrls)
    const [activeEndpointTab, setActiveEndpointTab] = useState(0);
    const [urlData, setUrlData] = useState({});
    const [loaded, setLoaded] = useState(false);

    useEffect(()=>{
        setLoaded(false);
        axios.post('http://localhost:8000/api/url/auto', {url:props.thisFqdn.targetUrls[activeEndpointTab]})
        .then(res=>{
            if (res.data){
                setUrlData(res.data);
            } else {
                setUrlData({
                    "endpoints": []
                })
            }
            setLoaded(true);
        })
        .catch(err=>console.log(err))
    }, [activeEndpointTab]);

    return (
        <>
        <nav style={{borderBottom: '2px groove #284B63'}} className="pl-2 pt-0 navbar navbar-expand-lg bg-primary">
            <div className="container-fluid">
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <h5 className="text-secondary ml-4 pt-0 mb-0">Target URL : &nbsp;&nbsp;<a className="text-secondary" target="_blank" rel="noreferrer" href={urls[0]}>{urls[0]}</a></h5>
                </div>
            </div>
        </nav>
        <div className="bg-secondary checklistStyle ml-4">
            <ul>
                <li>Reflected Input</li>
                <ul>
                    <li>Cross-Site Scripting (XSS)</li>
                    <ul>
                        <li>CORS Bypass</li>
                        <li>Session Riding</li>
                    </ul>
                </ul>
                <li>Open Redirect</li>
                <ul>
                    <li>Different Paths</li>
                    <li>Different Subdomains</li>
                    <li>Different FQDN</li>
                </ul>    
            </ul>
        </div>
        <div className="bg-secondary workTableStyle">
        </div>
        </>
    )
}

export default Chaining;