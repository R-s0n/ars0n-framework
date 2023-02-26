import axios from 'axios';
import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';

const NucleiScans = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [vulnList, setVulnList] = useState([]);
    const [loaded, setLoaded] = useState(false);
    const [currentVuln, setCurrentVuln] = useState(0);

    const {addToast} = useToasts()

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.vulns;
                    if (tempArr.length > 0){
                        setVulnList(res.data.vulns)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props])

    const deleteVuln = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.sublist3r = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setVulnList(res.data.recon.subdomains.sublist3r)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-3 pl-0 ml-0">
            <div className="row" style={{width:'1400px'}}>
                <div className="col-3" style={{height:'750px', overflowY:'scroll'}}>
                    <ul>
                    {
                        vulnList.map((vuln, i)=>{
                            return (
                                vuln.info.severity !== "info" ? <li key={i} style={{listStyleType:"none", color:"red"}} onClick={(e)=>setCurrentVuln(i)}>{vuln.info.name}</li> 
                                : <li key={i} style={{listStyleType:"none"}} onClick={(e)=>setCurrentVuln(i)}>{vuln.info.name}</li>
                            )
                        })
                    }
                    </ul>
                </div>
                <div className="col-9" style={{height:'750px', overflowY:'scroll'}}>
                    <ul>
                    {
                        vulnList.filter(vuln => vulnList.indexOf(vuln) === currentVuln).map(filteredVuln => (
                            <>
                            <p><b>Name:</b> {filteredVuln.info.name}</p>
                            <p><b>Template ID:</b> {filteredVuln['template-id']}</p>
                            <p><b>Tags:</b> {filteredVuln.info.tags?.length > 0 ? filteredVuln.info.tags.map((tag) => <>{tag}&nbsp;&nbsp;</>) : <>No Tags</>}</p>
                            <p><b>Severity:</b> {filteredVuln.info.severity}</p>
                            <p><b>Description:</b> {filteredVuln.info.description}</p>
                            <p><b>Host:</b> <a href={filteredVuln.host}  target="_blank" rel="noreferrer">{filteredVuln.host}</a></p>
                            <p><b>Matched:</b> <a href={filteredVuln['matched-at']}  target="_blank" rel="noreferrer">{filteredVuln['matched-at']}</a></p>
                            <p><b>Match Type:</b> {filteredVuln['matcher-name']}</p>
                            <p><b>IP:</b> {filteredVuln.ip}</p>
                            <p><b>Extracted Results:</b> 
                            <ul>
                            {
                                filteredVuln['extracted-results'] && filteredVuln['extracted-results'].length > 0 ? filteredVuln['extracted-results'].map((result, i)=>{
                                    return (
                                        <li key={i} style={{listStyleType:"none"}}>{result}</li>
                                    )
                                }) : <p>No Extracted Results</p>
                            }
                            </ul>   
                            </p>
                            <p><b>References:</b> 
                            <ul>
                            {
                                filteredVuln.info.reference && filteredVuln.info.reference.length > 0 ? filteredVuln.info.reference.map((reference, i)=>{
                                    return (
                                        <li key={i} style={{listStyleType:"none"}}><a href={reference}  target="_blank" rel="noreferrer">{reference}</a></li>
                                    )
                                }) : <p>No References</p>
                            }
                            </ul>   
                            </p>
                            <p><b>Curl Command:</b> {filteredVuln['curl-command']}</p>
                            <p><b>Discovered:</b> {filteredVuln.timestamp}</p>
                            </>
                        ))
                    }
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default NucleiScans;