import axios from 'axios';import React, {useState, useEffect} from 'react';

import toast, { Toaster } from 'react-hot-toast';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const CloudRanges = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);



    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }

    useEffect(()=>{
        setFormCompleted(false);
        axios.post(`http://${process.env.REACT_APP_API_IP}:${process.env.REACT_APP_API_PORT}/api/fqdn`, {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.cloudRanges;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.cloudRanges)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props])
    


    const addCloudRangesData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.cloudRanges = list.split("\n");
        axios.post(`http://${process.env.REACT_APP_API_IP}:${process.env.REACT_APP_API_PORT}/api/fqdn/update`, tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.cloudRanges)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteCloudRangesData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.cloudRanges = [];
        axios.post(`http://${process.env.REACT_APP_API_IP}:${process.env.REACT_APP_API_PORT}/api/fqdn/update`, tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.cloudRanges)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>This tool proactively scans all of AWS's IP ranges looking for any servers running port 443.  The tool then pulls the TLS/SSL certificate from each of these servers and stores them in searchable JSON format.</p>
                    <p><b>GOAL: </b>Identify servers hosted in AWS that are in scope but are likely not intended to be found by the developer.</p>
                    <p><b>DOWNLOAD/INSTALL: </b><span onClick={notify}>https://github.com/R-s0n/Fire_Spreader.git</span></p>
                    <p><b>RUN: </b><span onClick={notify}>python3 clear_sky.py -d {props.thisFqdn.fqdn}</span></p>
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="cloudRanges" formFunction={addCloudRangesData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteCloudRangesData} subdomainList={subdomainList} thisScanner="cloudRanges"/>
                }
            </div>
        </div>
    )
}

export default CloudRanges;