import axios from 'axios';
import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const Subfinder = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.subfinder;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.subfinder)
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

    const addSubfinderData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.subfinder = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.subfinder)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteSubfinderData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.subfinder = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.subfinder)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-1">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>Subfinder is a subdomain discovery tool that discovers valid subdomains for websites by using passive online sources. It has a simple modular architecture and is optimized for speed. subfinder is built for doing one thing only - passive subdomain enumeration, and it does that very well.</p>
                    <p><b>GOAL: </b>Identify valid sub-domains of the current FQDN to help build a complete picture of the application.</p>
                    <p><b>DOWNLOAD: </b><span onClick={copyToClipboard}>GO111MODULE=on go get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder</span></p>
                    <p><b>INSTALL: </b>Subfinder will work after using the installation instructions however to configure Subfinder to work with certain services, you will need to have setup API keys.  Theses values are stored in the $HOME/.config/subfinder/config.yaml file which will be created when you run the tool for the first time. The configuration file uses the YAML format. Multiple API keys can be specified for each of these services from which one of them will be used for enumeration.  For sources that require multiple keys, namely Censys, Passivetotal, they can be added by separating them via a colon (:).</p>
                    <p><b>RUN: </b><span onClick={copyToClipboard}>./subfinder -d {props.thisFqdn.fqdn} -o subfinder.{props.thisFqdn.fqdn}.txt; cat subfinder.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="subfinder" formFunction={addSubfinderData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteSubfinderData} subdomainList={subdomainList} thisScanner="subfinder"/>
                }
            </div>
        </div>
    )
}

export default Subfinder;