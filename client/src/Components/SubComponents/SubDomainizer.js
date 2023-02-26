import axios from 'axios';import React, {useState, useEffect} from 'react';

import toast, { Toaster } from 'react-hot-toast';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const SubDomainizer = props => {
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
                    const tempArr = res.data.recon.subdomains.subdomainizer;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.subdomainizer)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props])
    


    const addSubDomainizerData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.subdomainizer = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.subdomainizer)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteSubDomainizerData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.subdomainizer = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.subdomainizer)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-3">
            <div className="row">
                <div className="col-12">
                        <Toaster />
                    <p><b>DETAILS: </b>SubDomainizer is a tool designed to find hidden subdomains and secrets present is either webpage, Github, and external javascripts present in the given URL. This tool also finds S3 buckets, cloudfront URL's and more from those JS files which could be interesting like S3 bucket is open to read/write, or subdomain takeover and similar case for cloudfront. It also scans inside given folder which contains your files.</p>
                    <p><b>GOAL: </b>Identify valid sub-domains of the current FQDN to help build a complete picture of the application.</p>
                    <p><b>DOWNLOAD: </b><span onClick={notify}>git clone https://github.com/nsonaniya2010/SubDomainizer.git</span></p>
                    <p><b>INSTALL: </b><span onClick={notify}>pip3 install -r requirements.txt</span></p>
                    <p><b>RUN: </b><span onClick={notify}>python3 SubDomainizer.py -u {props.thisFqdn.fqdn} -o subdomainizer.{props.thisFqdn.fqdn}.txt; cat subdomainizer.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="subdomainizer" formFunction={addSubDomainizerData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteSubDomainizerData} subdomainList={subdomainList} thisScanner="subdomainizer"/>
                }
            </div>
        </div>
    )
}

export default SubDomainizer;