import axios from 'axios';
import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const Sublist3r = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.sublist3r;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.sublist3r)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props])
    
    const copyToClipboard = e => {
        navigator.clipboard.writeText(e.target.innerText)
        addToast(`Copied "${e.target.innerText}" to Clipboard`, {appearance:'info',autoDismiss:true});
    }

    const addSublist3rData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.sublist3r = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.sublist3r)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteSublist3rData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.sublist3r = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.sublist3r)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b> Sublist3r is a python tool designed to enumerate subdomains of websites using OSINT. It helps penetration testers and bug hunters collect and gather subdomains for the domain they are targeting. Sublist3r enumerates subdomains using many search engines such as Google, Yahoo, Bing, Baidu and Ask. Sublist3r also enumerates subdomains using Netcraft, Virustotal, ThreatCrowd, DNSdumpster and ReverseDNS.</p>
                    <p><b>GOAL: </b>Identify valid sub-domains of the current FQDN to help build a complete picture of the application.</p>
                    <p><b>DOWNLOAD: </b><span onClick={copyToClipboard}>sudo git clone https://github.com/aboul3la/Sublist3r.git</span></p>
                    <p><b>INSTALL: </b><span onClick={copyToClipboard}>sudo pip install -r requirements.txt</span></p>
                    <p><b>RUN: </b><span onClick={copyToClipboard}>sudo python3 sublist3r.py -d {props.thisFqdn.fqdn} -t 50 -o sublist3r.{props.thisFqdn.fqdn}.txt -v; cat sublist3r.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="sublist3r" formFunction={addSublist3rData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteSublist3rData} subdomainList={subdomainList} thisScanner="sublist3r"/>
                }
            </div>
        </div>
    )
}

export default Sublist3r;