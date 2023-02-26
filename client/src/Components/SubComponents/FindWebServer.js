import axios from 'axios';import React, {useState, useEffect} from 'react';

import toast, { Toaster } from 'react-hot-toast';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const FindWebServer = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);



    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.masscanLive;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.masscanLive)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props])
    


    const addFindWebServerData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.masscanLive = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.masscanLive)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteFindWebServerData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.masscanLive = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.masscanLive)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>This tool pulls the dnmasscan results from the WAPT Framework and checks each server/port combination to find any that are actively running web servers.</p>
                    <p><b>GOAL: </b>Identify hidden/obfuscated web servers that can potentially be exploited.</p>
                    <p><b>DOWNLOAD/INSTALL: </b><span onClick={notify}>git clone https://github.com/R-s0n/Fire_Spreader.git</span></p>
                    <p><b>RUN: </b><span onClick={notify}>python3 wind.py -d {props.thisFqdn.fqdn}</span></p>
                </div>
            </div>
            <div className="row mt-3">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="masscanLive" formFunction={addFindWebServerData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteFindWebServerData} subdomainList={subdomainList} thisScanner="masscanLive"/>
                }
            </div>
        </div>
    )
}

export default FindWebServer;